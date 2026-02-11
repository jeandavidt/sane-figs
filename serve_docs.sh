#!/bin/bash
# Generate figures and serve MkDocs documentation

echo "Generating documentation figures..."
uv run python -m docs_scripts.generate_figures

echo "Starting MkDocs server..."
uv run mkdocs serve
