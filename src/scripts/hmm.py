import pandas as pd
import collections
import numpy as np
from collections import defaultdict
import sys
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
RECENTAS_PATH = os.path.join(__location__, './recetas.csv')
df = pd.read_csv(RECENTAS_PATH)

#print(df.shift(-3).to_string())
#print(df.shift(-3)['Unnamed: 1'].to_string())
#print(df.shift(-3)['Unnamed: 2'].to_string())

df = df.shift(-4)
names = df['Unnamed: 1']
ingr = df['Unnamed: 2']
#print(names)
#print(ingr[0])

w = []

for i in ingr:
  i = str(i)
  if i == 'nan':
    break
  l = i.split(', ')
  for p in l:
    if(p.strip()):
      w.append(p)

c = collections.Counter(w)
#print(c)
#map['gin']['vodka']=0.05
#asigna valores
d = {}
for i in list(c.elements()):
  d[i] = float(c[i])/len(w)

sum = 0
for i in d.keys():
  sum += d[i]

#print(sum)
#print(d)

######### new probabilities

ingr_new = {}
sum = {}
ingr_set = {}

for i in ingr:
  i = str(i)
  if i == 'nan':
    break
  l = i.split(', ')
  for i1 in l:
    if(i1.strip()):
      ingr_set[i1] = 0

for i1 in ingr_set.keys():
  for i2 in ingr_set.keys():
      ingr_new[(i1,i2)] = 0

for i in ingr:
  i = str(i)
  if i == 'nan':
    break
  l = i.split(', ')
  for i1 in l:
    if(i1.strip()):
      ingr_set[i1] = 0
      for i2 in l:
        if(i2.strip()):
          ingr_new[(i1,i2)] += 1

#print(ingr_new)


for i1 in ingr_set.keys():
  for i2 in ingr_set.keys():
      if i1 in sum:
        sum[i1] += ingr_new[(i1,i2)]
      else:
        sum[i1] = ingr_new[(i1,i2)]

#print(sum)

for i1 in ingr_set.keys():
  for i2 in ingr_set.keys():
    ingr_new[(i1,i2)] /= sum[i1]

for i1 in ingr_set.keys():
  dif = abs(ingr_new[(i1, i1)] - .10)
  ingr_new[(i1, i1)] = 0.10
  part = dif/(len(ingr_set.keys())-1)
  for i2 in ingr_set.keys():
    if i1 != i2:
      ingr_new[(i1, i2)] += part

#print(ingr_new) 

for i1 in ingr_set.keys():
  add = 0
  for i2 in ingr_set.keys():
    add += ingr_new[(i1,i2)]
  #print('{} sum: {}'.format(i1, add))

############ matrix


matrix = []

for i1 in ingr_set.keys():
  lista = []
  for i2 in ingr_set.keys():
    lista.append(ingr_new[(i1,i2)])
  matrix.append(lista)

#print(matrix)

#np.savetxt('test.csv',matrix, delimiter=',')

pd.DataFrame(matrix, index=ingr_set.keys(), columns = ingr_set.keys()).to_csv("file.csv")

ingr_set.keys()

state =[]

for key in ingr_set.keys():
  state.append(key)

#print(state)

import scipy.linalg
import numpy as np
 
 
# Encoding this states to numbers as it
# is easier to deal with numbers instead
# of words.
#state = ["A", "E"]
 
# Assigning the transition matrix to a variable
# i.e a numpy 2d matrix.
#MyMatrix = np.array([[0.6, 0.4], [0.7, 0.3]])
MyMatrix = matrix
# Simulating a random walk on our Markov chain
# with 20 steps. Random walk simply means that
# we start with an arbitrary state and then we
# move along our markov chain.
n = 5
 
# decide which state to start with
StartingState = 0
CurrentState = StartingState
 
#getting state from user
val = sys.argv[1]
#print(val)
StartingState = state.index(val)
CurrentState = StartingState
n = sys.argv[2]
#print(n)
n = int(n)
# printing the stating state using state
# dictionary
#print(state[CurrentState], "--->", end=" ")
result = ''
result += state[CurrentState]
while n-1:
    # Deciding the next state using a random.choice()
    # function,that takes list of states and the probability
    # to go to the next states from our current state
    ingredient = np.random.choice(state, p=MyMatrix[CurrentState])
    CurrentState = state.index(ingredient)
    # printing the path of random walk
    #print(state[CurrentState], "--->", end=" ")
    #arr_states[iterarion_n] = state[CurrentState]
    result += ',' + state[CurrentState]
    n -= 1

print(result)
#print("stopped!")

# Let us find the stationary distribution of our
# Markov chain by Finding Left Eigen Vectors
# We only need the left eigen vectors
MyValues, left = scipy.linalg.eig(MyMatrix, right=False, left=True)
 
#print("left eigen vectors = \n", left, "\n")
#print("eigen values = \n", MyValues)
 
# Pi is a probability distribution so the sum of
# the probabilities should be 1 To get that from
# the above negative values we just have to normalize
pi = left[:, 0]
pi_normalized = [(x/np.sum(pi)).real for x in pi]
#pi_normalized