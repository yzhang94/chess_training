# Chess Station Builder Backend

This directory contains the initial Flask backend for the Chess Station Builder MVP. It focuses on database models and application setup per `design/architecture_solution_1_simple.md`.

## Requirements

- Python 3.12
- [uv](https://github.com/astral-sh/uv)

## Getting Started (uv)

```bash
cd chess_station_builder
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Running the App

```bash
python run.py
```

## Initialize the Database

```bash
python scripts/init_db.py
```

## Tests

```bash
pytest
```
