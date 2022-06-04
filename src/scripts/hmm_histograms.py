import pandas as pd
import collections
import numpy as np
from collections import defaultdict
import sys
import os
import matplotlib.pyplot as plt

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

def comparison(first_ingredient, ingredients, histo):
      ingr = df['Unnamed: 2']
      w = [[]] * len(ingr)
      current = 0
      for i in range(len(ingr)):
          recipe = str(ingr[i])
          if recipe == 'nan':
              break
          l = recipe.split(', ')
          aux=[]
          for p in l:
              if(p.strip()):
                  aux.append(p)
          w[current]=aux
          current+=1
      recipes=[]
      
      n_ingr=dict()
      for recipe in w:
          #if len(recipe)==ingredients and first_ingredient in recipe:  
          if first_ingredient in recipe:
              recipes.append(recipe)
      sample=[]
      for recipe in recipes:
          for ingredient in recipe:      
              sample.append(ingredient)
              if not ingredient in n_ingr:
                  n_ingr[ingredient]=0
              n_ingr[ingredient]+=1
      n_ingr[first_ingredient]=0
      if histo:
        plt.figure(figsize=(12, 7))
        plt.hist(sample, bins = len(n_ingr), color = "blue", rwidth=0.9)
        plt.title("Ingredientes combinables con "+str(val)+" en recetas de las fuentes")
        plt.xlabel("Ingredientes")
        plt.xticks(rotation=45)
        plt.ylabel("Frecuencia")
        plt.show()

      
      return n_ingr
      
      
def gen_acur(from_recipe,from_generator):
      c_y=c_n=0
      for key in from_generator:
            if key in from_recipe:
                  #print(key,": yes\n")
                  c_y+=1
            else:
                  #print(key,": no\n")
                  c_n+=1
      return (c_y,c_y+c_n)
                  
      '''
      #aparicion de ingredientes de generador
      c=0
      for key in from_generator:
            c+=1
      for key in from_generator:
            print(key,from_generator[key],"/",c,"=",from_generator[key]/c)
      '''

      '''
      #aparicion de ingredientes en recetas oficiales
      c=0
      for key in from_recipe:
            c+=1
      for key in from_recipe:
            print(key,from_recipe[key],"/",c,"=",from_recipe[key]/c)
      '''
      
if sys.argv[3] == 'false':
  print(state[CurrentState], "--->", end=" ")

  while n-1:
      # Deciding the next state using a random.choice()
      # function,that takes list of states and the probability
      # to go to the next states from our current state
      ingredient = np.random.choice(state, p=MyMatrix[CurrentState])
      CurrentState = state.index(ingredient)
      # printing the path of random walk
      print(state[CurrentState], "--->", end=" ")
      n -= 1
  print("stopped!")
else:
      ingredient_list=[]

      #getting state from user
      
      
      for i in range (30):
        StartingState = state.index(val)
        CurrentState = StartingState
        n = int(sys.argv[2])

        while n-1:
            # Deciding the next state using a random.choice()
            # function,that takes list of states and the probability
            # to go to the next states from our current state
            ingredient = np.random.choice(state, p=MyMatrix[CurrentState])
            ingredient_list.append(ingredient)
            CurrentState = state.index(ingredient)
            n -= 1
      #print(ingredient_list)
      n_ingr={}
      for ingr in ingredient_list:
            if not ingr in n_ingr:
                  n_ingr[ingr]=0
            n_ingr[ingr]+=1
      #generate histogram
      ingredient_list.remove(val) 
      n_ingr.pop(val)
      plt.figure(figsize=(12, 7))
      plt.hist(ingredient_list, bins = len(n_ingr), color = "blue", rwidth=0.9)
      plt.title("Ingredientes con "+str(val)+" en recetas de "+str(sys.argv[2])+" ingredientes")
      plt.xlabel("Ingredientes")
      plt.xticks(rotation=45)
      plt.ylabel("Frecuencia")
      
      from_recipe=comparison(val,n,sys.argv[4])
      plt.show()
      print("Histogramas generados correctamene")
      '''
      acur=gen_acur(from_recipe, n_ingr)
      print("conclusion",acur[0]," de ",acur[1], " ingredientes coinciden con respecto a la fuente")
      print("precision=",acur[0]/acur[1])
      '''



 
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