#!/usr/bin/python

# Trax python script

import sys
import csv

from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

def read_csv(csv_file):
  with open(csv_file, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    user_data = list(reader)

    print user_data

def neural_network(input):
  print "Neural Network"

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
  neural_network(read_csv(sys.argv[1]))