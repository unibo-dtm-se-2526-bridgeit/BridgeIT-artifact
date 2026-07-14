"""SQLite implementation of the RequirementRepository port.

Infrastructure Layer: this module is the only place in the codebase that
knows SQLite exists. The Application and Domain layers depend only on the
RequirementRepository port (see application/ports/requirement_repository.py)
and never on this module directly.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from bridgeit.application.ports.requirement_repository import RequirementRepository
from bridgeit.domain.requirement import Requirement, RequirementStatus, RequirementText


class SQLiteRequirementRepository(RequirementRepository):
    """Persists Requirement aggregates in a local SQLite database file."""

    def __init__(self, db_path: str | Path) -> None:
        self._db_path = str(db_path)
        self._create_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _create_schema(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS requirements (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    status TEXT NOT NULL
                )
                """
            )

    def save(self, requirement_id: str, requirement: Requirement) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO requirements (id, text, status)
                VALUES (:id, :text, :status)
                ON CONFLICT(id) DO UPDATE SET text = :text, status = :status
                """,
                {
                    "id": requirement_id,
                    "text": requirement.text.content,
                    "status": requirement.status.value,
                },
            )

    def get_by_id(self, requirement_id: str) -> Requirement | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT id, text, status FROM requirements WHERE id = ?",
                (requirement_id,),
            ).fetchone()
        if row is None:
            return None
        return self._row_to_requirement(row)

    @staticmethod
    def _row_to_requirement(row: tuple[str, str, str]) -> Requirement:
        # NOTE: reconstructing a Requirement from storage requires setting its
        # status directly, bypassing the state-machine transitions (the data
        # already satisfied those rules when it was originally saved -- we are
        # rehydrating known-valid state, not creating new state). Requirement
        # does not currently expose a public "rehydrate" factory for this, so
        # this touches its internal attribute directly. Worth raising with
        # @nikytresca as a possible follow-up (e.g. a package-private
        # `Requirement._from_storage(...)` classmethod), similar to the
        # Any->Requirement tech debt tracked earlier.
        requirement_id, text, status = row
        requirement = Requirement(
            requirement_id=requirement_id, text=RequirementText(text)
        )
        requirement._status = RequirementStatus(status)  # noqa: SLF001
        return requirement
