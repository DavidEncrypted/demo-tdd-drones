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
Run the following commands in a terminal window that is opened to this folder
```bash
# Install dependencies
uv sync

# Run the dashboard
uv run streamlit run app.py

# Test the demo file:
# In the dashboard open the demo .ulg file : <path_to_this_dir>/data/longflight.ulg

# Run tests
uv run pytest
```
