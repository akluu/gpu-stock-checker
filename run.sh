#!/bin/bash
if [[ ! -d "venv" ]]; then
    python3 -m venv
fi
source venv/bin/activate
pip3 install -r requirements.txt
python3 src/main.py