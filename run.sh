#!/bin/bash
REQUIREMENTS=$(diff "requirements.txt" <(pip3 freeze))
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
if [ ! -z "$REQUIREMENTS" ]; then
    pip3 install -r requirements.txt
fi
python3 src/main.py