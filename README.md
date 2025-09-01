# TDD Demo: Drone Flight Data Analysis

A basic demonstration of Test-Driven Development using Claude Code with drone flight log analysis.

## Architecture

```
.ulog file → PX4 Reader → DuckDB → Streamlit Dashboard
```

## Components

- **Data Loading**: PX4 ULog file reader
- **Processing**: DuckDB
- **Visualization**: Streamlit dashboard with basic plotting

## Setup

```bash
# Install dependencies
uv sync --group dev

# Run the dashboard
uv run streamlit run app.py

# Run tests
uv run pytest
```
