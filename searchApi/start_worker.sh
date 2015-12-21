#!/bin/bash
echo "Starting worker!"

celery worker -A tasks --loglevel=debug -B
