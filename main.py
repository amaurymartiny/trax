#!/usr/bin/python

# Trax python script
# Main neural network script
# Input should be a CSV file with 12 columns:
# 1. Artist 2. Title 3-11. Features (nine of them) 12. Like/Dislike (between 0 and 4)
# Usage: ./main.py <user_full.csv>

import sys
import csv

from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure           import FeedForwardNetwork, FullConnection, BiasUnit
from pybrain.structure.modules   import SoftmaxLayer, LinearLayer, SigmoidLayer, TanhLayer

def read_csv(csv_file):
  with open(csv_file, 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    user_data = list(reader)
    return user_data

def neural_network(input_data):
  print "Neural Network"
  print "=============="

  #Features we chose are:
  #"acousticness", "danceability", "energy", "liveness", "loudness", "mode", "speechiness", "tempo", "valence"
  #[2,              3,              4,         5          6           7       8               9       10]

  features = [2, 3, 4, 5 ,6, 8, 9, 10] # remove mode
  dimInput = len(features)

  dataset = ClassificationDataSet(dimInput, 1, nb_classes=5) # dimInput is the dimension of the input, 1 dimension of the target
  for row in input_data:



    # add all 9 features inside our input tuple
    input_tuple = ()
    for i in features:
      input_tuple += (float(row[i]),) # features are in columns 3 to 11
    # print float(row[3])
    dataset.addSample(input_tuple, [int(row[11])]) # 12th column = last column is the number between 0 and 4 to show if user likes or not the song

  # workaround for _convertToOneOfMany
  # http://stackoverflow.com/questions/27887936/attributeerror-using-pybrain-splitwithportion-object-type-changed
  tstdata_temp, trndata_temp = dataset.splitWithProportion(0.3)
  
  tstdata = ClassificationDataSet(dimInput, 1, nb_classes=5)
  for n in xrange(0, tstdata_temp.getLength()):
    tstdata.addSample( tstdata_temp.getSample(n)[0], tstdata_temp.getSample(n)[1] )

  trndata = ClassificationDataSet(dimInput, 1, nb_classes=5)
  for n in xrange(0, trndata_temp.getLength()):
     trndata.addSample( trndata_temp.getSample(n)[0], trndata_temp.getSample(n)[1] )

  # instead of 1 dimension of 5 classes, we use 5 target neurons
  # http://pybrain.org/docs/tutorial/fnn.html
  trndata._convertToOneOfMany()
  tstdata._convertToOneOfMany()

  print "Number of training patterns: ", len(trndata)
  print "Input and output dimensions: ", trndata.indim, trndata.outdim
  print "First sample (input, target, class):"
  print trndata['input'][0], trndata['target'][0], trndata['class'][0]

  # build neural network
  # using shortcut:
  #fnn = buildNetwork(trndata.indim, 5, trndata.outdim, hiddenclass=TanhLayer, outclass=LinearLayer, bias=True) #middle number is number of hidden layers

  # construct blank network
  fnn = FeedForwardNetwork()

  # add layers
  fnn.addInputModule(LinearLayer(dimInput, name="in"))
  fnn.addModule(SigmoidLayer(12, name="hidden1"))
  fnn.addModule(SigmoidLayer(12, name="hidden2"))
  fnn.addModule(SigmoidLayer(12, name="hidden3"))
  fnn.addOutputModule(LinearLayer(5, name="out"))

  # add bias
  bias = BiasUnit(name='bias')
  fnn.addModule(bias)

  # add connections
  in_to_hidden1 = FullConnection(fnn['in'], fnn['hidden1'])
  hidden1_to_hidden2 = FullConnection(fnn['hidden1'], fnn['hidden2'])
  hidden1_to_bias = FullConnection(fnn['hidden1'], fnn['bias'])
  bias_to_hidden2 = FullConnection(fnn['bias'], fnn['hidden2'])
  hidden2_to_hidden3 = FullConnection(fnn['hidden2'], fnn['hidden3'])
  hidden3_to_bias = FullConnection(fnn['hidden3'], fnn['bias'])
  bias_to_out = FullConnection(fnn['bias'], fnn['out'])
  hidden3_to_out = FullConnection(fnn['hidden3'], fnn['out'])

  fnn.addConnection(in_to_hidden1)
  fnn.addConnection(hidden1_to_hidden2)
  #fnn.addConnection(hidden1_to_bias)
  #fnn.addConnection(bias_to_hidden2)
  fnn.addConnection(hidden2_to_hidden3)
  fnn.addConnection(hidden3_to_out)
  #fnn.addConnection(hidden3_to_bias)
  #fnn.addConnection(bias_to_out)

  # final step to prepare nn
  fnn.sortModules()
  print fnn

  # train
  trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=False, weightdecay=0.01)

  #output_file = open("user1_output.csv", "wb")
  trnresults = []
  tstresults = []
  for i in range(100):
    trainer.trainEpochs(10)
    trnresult = percentError(trainer.testOnClassData(), trndata['class'])
    tstresult = percentError(trainer.testOnClassData(dataset=tstdata), tstdata['class'])


    print "train error: %5.2f%%" % trnresult, "  test error: %5.2f%%" % tstresult

    trnresults.append(trnresult)
    tstresults.append(tstresult)
    #output_file.write("%5.2f,%5.2f\n" % (trnresult, tstresult))

  #output_file.close()

  # print mean 
  print "Train error mean:", sum(trnresults)/float(len(trnresults))
  print "Test error mean:", sum(tstresults)/float(len(tstresults))


# Main function
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print >>sys.stderr, "Usage: %s <user_file>" % sys.argv[0]
    sys.exit(1)
  neural_network(read_csv(sys.argv[1]))
