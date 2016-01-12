#!/usr/bin/python

# Trax python script
# Given a CSV file with Artist and Title as first two columns,
# this script will add 9 other columns in the file corresponding to the 9 features we are interested in
# Usage: ./populate_data songs.csv

import sys
import csv
import time

from pyechonest import config
from pyechonest import song

config.ECHO_NEST_API_KEY="1CTQFDPWDNNGNIYR3"

def read_csv(csv_file):
  with open(csv_file, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    user_data = list(reader)

  # we would normally loop over the 100 songs in user_data using for i in range(100)
  # but echonest only allows 20 request per minute
  # so we do the loop 20 per 20, with a 1 minute pause in between
  for k in range(0,5):
    for i in range(20 * k, 20 * (k + 1)):

      # # normalize the parameter if user likes or not the song
      # user_data[i][3] = normalize(int(user_data[i][3]), 0, 4) # user likes are between 0 (hate) and 4 (love)

      # search for song features in the echonest api
      result = song.search(artist=user_data[i][0], title=user_data[i][1], buckets=['audio_summary'])
      
      # Use echonest's exact title if not the case
      user_data[i][0] = result[0].artist_name
      user_data[i][1] = result[0].title

      # the features we are interested in are the following
      features = ["acousticness", "danceability", "energy", "liveness", "loudness", "mode", "speechiness", "tempo", "valence"]
      for feature in features:
        normed_value = result[0].audio_summary[feature]
        if feature == "loudness":
          normed_value = normalize(normed_value, -20, 140) # [-20, 140] is the range of dB for human hearing
        elif feature == "tempo":
          normed_value = normalize(normed_value, 20, 200) # general songs' tempo range from 20 to 200
        user_data[i].append(normed_value)
      print i, user_data[i][0], "-", user_data[i][1]
    with open("./data/songs_full.csv", "wb") as f:
      writer = csv.writer(f)
      writer.writerows(user_data)

    # here is where we wait for 1 minute  
    if k < 4:
      print "Waiting 1 minute for Echonest API."
      time.sleep(90)

# normalization function
# x is data, minX is minimum values in each column and maxX is maximum values in each column
# output will be between 0 and 1
def normalize(x, minX, maxX): 
  return float(x - minX) / float(maxX - minX)

# Main function
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print >>sys.stderr, "Usage: %s <user_file>" % sys.argv[0]
    sys.exit(1)
  read_csv(sys.argv[1])