#!/usr/bin/python

# Trax python script

import sys
import math
import json
import operator

from pyechonest import config
from pyechonest import song

config.ECHO_NEST_API_KEY="1CTQFDPWDNNGNIYR3"

def euclidianDistance(song1, song2):
  features = ["acousticness", "danceability", "energy", "liveness", "loudness", "mode", "speechiness", "tempo", "valence"]
  distance = 0
  for feature in features:
    distance += pow(song1.audio_summary[feature] - song2.audio_summary[feature], 2)
  return math.sqrt(distance)

def knn(song, trainingSet, k):
  distances = []
  for i in range(len(trainingSet)):
    d = euclidianDistance(song, trainingSet[i])
    distances.append((trainingSet[i], d))
  distances.sort(key=operator.itemgetter(1))
  neighbors = []
  for i in range(k):
    neighbors.append(distances[i][0])
  return neighbors


# Main function
if __name__ == "__main__":
  # get dataset: 100 most popular songs
  results = song.search(buckets=["id:rdio-US", "audio_summary"], limit=True, results=100, sort="song_hotttnesss-desc")
  # print the euclidianDistance
  print euclidianDistance(results[13], results[48])
  # print 2nn of song44
  print results[44], "nearest neighbors:", knn(results[44], results, 3)
