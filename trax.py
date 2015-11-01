#!/usr/bin/python

# Trax python script

import sys

from pyechonest import config
from pyechonest import track
config.ECHO_NEST_API_KEY="1CTQFDPWDNNGNIYR3"

def fingerprint(file):
  t = track.track_from_filename(file)
  # t.get_analysis()
  # print "Fingerprint:",   t.echoprintstring
  print "Acousticness:",  t.acousticness
  print "Danceability:",  t.danceability
  print "Energy:",        t.energy
  print "Liveness:",      t.liveness
  print "Loudness:",      t.loudness
  print "Mode:",          "minor" if t.mode else "major"
  print "Speechiness:",   t.speechiness
  print "Tempo:",         t.tempo
  print "Time Signature", t.time_signature
  print "Valence:",       t.valence

# Main function
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print >>sys.stderr, "Usage: %s <audio file>" % sys.argv[0]
    sys.exit(1)
  fingerprint(sys.argv[1])