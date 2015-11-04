#!/usr/bin/python

# Trax python script

import sys

from pyechonest import config
from pyechonest import song

config.ECHO_NEST_API_KEY="1CTQFDPWDNNGNIYR3"

def dataset():
  results = song.search(buckets=["id:rdio-US", "audio_summary"], limit=True, results=100, sort="song_hotttnesss-desc")
  print results[23].artist_name

# Main function
if __name__ == "__main__":
  dataset()