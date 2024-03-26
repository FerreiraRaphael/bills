#!/bin/sh -l

uvicorn api.run:app --reload --host 0.0.0.0 --port "$@"
