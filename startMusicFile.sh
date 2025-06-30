#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Error: No music file specified."
    echo "Usage: $0 <music_path>"
    exit 1
fi

amixer -c 2 sset 'Speaker' 100%

source venv/bin/activate
python3 music-file.py "$1"

