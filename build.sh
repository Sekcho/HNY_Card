#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (only Chromium to save space)
playwright install chromium

# Install system dependencies for Playwright
playwright install-deps chromium

# Create necessary directories
mkdir -p static/uploads
mkdir -p static/generated
mkdir -p data
