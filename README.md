# vector-databases

Weaviate exercises. Dependencies are managed with **uv** only (`pip` is not used in this repo).

## Setup

```powershell
uv sync
```

## Run

Scripts stay at the repo root:

```powershell
uv run rag.py
uv run movies.py
uv run streamlit run app.py
```

Wikipedia helper (package under `src/vector_databases/`):

```powershell
uv run wiki
```

Weaviate itself still runs with Podman:

```powershell
podman compose up -d
```
