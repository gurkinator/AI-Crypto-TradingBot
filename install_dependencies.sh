#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

echo "Installing dependencies for Gurks Advanced AI Trading Bot"
echo "Folder: $(pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 was not found. Install Python 3.11+ first."
  exit 1
fi

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo
echo "Done. Start with:"
echo "  source venv/bin/activate"
echo "  streamlit run bot.py --server.address 0.0.0.0 --server.port 8501"

