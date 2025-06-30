#!/bin/bash

# Check if an argument was passed
if [ $# -eq 0 ]; then
    echo "Error: No music file specified."
    echo "Usage: $0 <music_url>"
    exit 1
fi

# Set speaker volume
amixer -c 2 sset 'Speaker' 100%

source venv/bin/activate
# Play the music
python3 music.py "$1"

