#!/usr/bin/python

# Trax python script

import sys
import math
import json

from pyechonest import config
from pyechonest import song

config.ECHO_NEST_API_KEY="1CTQFDPWDNNGNIYR3"

def dataset():
  results = song.search(buckets=["id:rdio-US", "audio_summary"], limit=True, results=100, sort="song_hotttnesss-desc")
  print euclidianDistance(results[13], results[48])

def euclidianDistance(song1, song2):
  features = ["acousticness", "danceability", "energy", "liveness", "loudness", "mode", "speechiness", "tempo", "time_signature", "valence"]
  distance = 0
  for feature in features:
    distance += pow(song1.audio_summary[feature] - song2.audio_summary[feature], 2)
  return math.sqrt(distance)

# Main function
if __name__ == "__main__":
  dataset()