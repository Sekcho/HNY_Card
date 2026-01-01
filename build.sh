#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers (only Chromium to save space)
# Note: Render has pre-installed system dependencies for browsers
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0 playwright install chromium --with-deps

# Create necessary directories
mkdir -p static/uploads
mkdir -p static/generated
mkdir -p data
