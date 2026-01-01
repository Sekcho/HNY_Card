#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (only Chromium)
# Render has system dependencies pre-installed, so we skip deps installation
playwright install chromium

# Create necessary directories
mkdir -p static/uploads
mkdir -p static/generated
mkdir -p data
