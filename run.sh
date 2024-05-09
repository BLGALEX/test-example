#!/bin/bash
export PYTHONPATH="$PYTHONPATH:$PWD"
python db/run_migrations.py && \
mkdir -p multiproc-tmp && \
export PROMETHEUS_MULTIPROC_DIR=multiproc-tmp && \
python -m gunicorn src.app:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --workers "${NUM_WORKERS}" --keep-alive 400 --max-requests 50000
