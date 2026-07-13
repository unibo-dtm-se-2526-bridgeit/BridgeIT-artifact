from fastapi import FastAPI

app = FastAPI(title="BridgeIT")


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint: confirms the service is up and responding."""
    return {"status": "ok"}
