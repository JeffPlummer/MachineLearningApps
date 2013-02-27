from __future__ import division
from math import sqrt
from math import cos



# Returns a Euclidan distance based similarity, score for person1 and person2.
# Euclidian distance of 2-dimensional object is sqrt((x1-x2)^2 + (y1-y2)^2 + ...), 
def similarities_euclid_distance(prefs, person1, person2):
  #Get the list of shared items
  sharedItems={}
  for item in prefs[person1]:   # E.g. item = {'Lady in the Water':2.5}
    if item in prefs[person2]:
      sharedItems[item]=1

  #return 1
  # if they have no ratings in common, return 0
  if len(sharedItems)==0: return 0

    # Normal euclid distance will yield smaller number, the closer, or more similar the users.
    # Invert and +1 to make similarities yield a higher # the more similar.
  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item], 2)
    for item in sharedItems])
  
  return 1/(1+sqrt(sum_of_squares))


# Pearson is a measure of how well the two sets of data fit on a single straight
# line.  Can give better results when data is not normalized, e.g. 1 user is
# consitantly more harsh.
def similarities_pearson_distance(prefs, person1, person2):
  #Get the list of shared items
  sharedItems={}
  for item in prefs[person1].keys():   # E.g. item = {'Lady in the Water':2.5}
    if item in prefs[person2].keys():
      sharedItems[item]=1

  n = float(len(sharedItems))

  #return 1
  # if they have no ratings in common, return 0
  if n==0: return -1

  # Add up all the preferences
  sum1=sum([prefs[person1][it] for it in sharedItems.keys()])
  sum2=sum([prefs[person2][it] for it in sharedItems.keys()])

    #Sum up the squares
  sum1Sq = sum([pow(prefs[person1][it], 2) for it in sharedItems.keys()])
  sum2Sq = sum([pow(prefs[person2][it], 2) for it in sharedItems.keys()])

  #Sum up the products
  pSum=sum([prefs[person1][it]*prefs[person2][it] for it in sharedItems.keys()])

  # Calculate Pearson score
  num=(n*pSum)-(1.0*sum1*sum2)
  
  den1=sqrt((n*sum1Sq)-float(pow(sum1,2)))
  den2=sqrt((n*sum2Sq)-float(pow(sum2,2)))
  den=1.0*den1*den2

  if den==0:
    return 0

  r=float(num)/float(den)
  return r


# Returns the Cosine Similarity Score for p1 and p2
def similarities_cosine(prefs, p1, p2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]:
    if item in prefs[p2]: 
      si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # Calcuate the normalized vector
  num_p = sum([prefs[p1][it]*prefs[p2][it] for it in si])
  norm_p1 = sqrt(sum([pow(prefs[p1][it],2) for it in si]))
  norm_p2 = sqrt(sum([pow(prefs[p2][it],2) for it in si]))

  # Calculate the Cosine Similarity Score.
  s_cos =  cos(num_p / (norm_p1*norm_p2))

  return s_cos

# Basic Jaccard.  Only makes sense when using binary data.
def jaccard(vector1,vector2):
  set1,set2,shared=0,0,0
  
  for i in range(len(vector1)):
    if vector1[i]!=0:
      set1+=1 # in vector1
    if vector2[i]!=0: 
      set2+=1 # in vector2
    if vector1[i]!=0 and vector2[i]!=0: 
      shared+=1 # in both
    try:
      return 1.0 - (float(shared)/(set1+set2-shared))
    except:
      print "Divided by 0"

# Returns the Extended Jaccard Coefficient for p1 and p2
def similarities_ext_jaccard(prefs, p1, p2):
  # Get the list of mutually rated items
  si={}
  for item in prefs[p1]:
    if item in prefs[p2]: 
      si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: 
    return 0

  # Calcuate the different parts of the of score
  cross_p = sum([prefs[p1][it]*prefs[p2][it] for it in si])
  norm_p1 = sum([pow(prefs[p1][it],2) for it in si])
  norm_p2 = sum([pow(prefs[p2][it],2) for it in si])

  # Calculate the Extended Jaccard Coefficient.
  EJ = cross_p /(norm_p1 + norm_p2 - cross_p)

  return EJ

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs, person, n=5, similarity=similarities_pearson_distance):
    scores=[(similarity(prefs, person, other), other)
      for other in prefs if other != person]

    # Sort the list so the highest scores appear at the top
    scores.sort()
    scores.reverse()
    return scores[0:n] 


# Get's recommendations for a person by using a weighted average
# of every other user's rankings.
def getRecommendations(prefs, person, similarity=similarities_pearson_distance):
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs, person, other)

    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:

      #only score movies I haven't seen
      if item not in prefs[person] or prefs[person][item]==0:
        # Similarity * Score
        totals.setdefault(item, 0)
        totals[item]+=prefs[other][item]*sim

        # Sum of Similarities
        simSums.setdefault(item, 0)
        simSums[item]+=sim

      # Create the normalized list
      rankings=[(total/simSums[item], item) for item, total in totals.items()]

  # Return the sorted list
  rankings.sort()
  rankings.reverse()
  return rankings


def transformPrefs(prefs):
  result = {}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item, {})

      # Flip the item and the person
      result[item][person] = prefs[person][item]
  return result





critics={ 'Bob' : {'Batman':4.0, 'Superman':3.5, 'Ironman':3.5},
         'Larry' : {'Batman':3, 'Superman':2.5, 'Ironman':2},
         'Samantha' : {'Batman':1.0, 'Superman':1.5, 'Ironman':1.0},
'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

