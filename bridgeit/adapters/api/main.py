from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="BridgeIT")

# Allow the local frontend (served from a different origin than the API)
# to call this backend during development. Origins are listed explicitly
# rather than using "*", so this stays safe to tighten later for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "null",  # allows requests from pages opened directly as local files
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint: confirms the service is up and responding."""
    return {"status": "ok"}
