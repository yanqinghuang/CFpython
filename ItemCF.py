import sys
import operator
import math

W = {}

def LoadData():
  #train = {userId:[iterm1, item2...]} the same as test dict
  #W = {u:{v:value}} the same as C
  #item_users = {item, [user1,user2...]}
  #N(i) = {i:value} The number of users who like i 
  test = {}
  train = {}
  item_users = {}
  TrainFile = 'ml-100k/u2.base'
  TestFile = 'ml-100k/u2.test'
  #load train file
  with open(TrainFile,'r') as file_object:
    for line in file_object:
      (userId, itemId, rating, _) = line.strip().split('\t')
      item_users.setdefault(itemId,[])
      if itemId not in item_users:
        item_users[itemId] = list()
      item_users[itemId].append(userId)

      train.setdefault(userId,[])
      if userId not in train:
        train[userId] = list()
      train[userId].append(itemId)
    # print("item_users: %s"%item_users)
    # print("train: %s"%train)
  #load test file
  with open(TestFile,'r') as test_object:
    for line in test_object:
      (userId, itemId, rating, _) = line.strip().split('\t')
      test.setdefault(userId,[])
      if userId not in test:
        test[userId] = itemId
      else:
        test[userId].append(itemId)
    # print("test: %s"%test)
  return train, test, item_users

def ItemSimilarity(train):
#calculate co-rated users between items
  C = {}
  N = {}
  for user, items in train.items():
    for i in items:
      C.setdefault(i,{})
      N.setdefault(i,0)
      N[i] += 1
      for j in items:
        if i == j:
          continue
        C[i].setdefault(j,0)
        C[i][j] += 1
#calculate finial similarity matrix W
  for i,related_items in C.items():
    W.setdefault(i,{})
    for j, cij in related_items.items():
      W[i][j] = cij / math.sqrt(N[i] * N[j])
  # print("W: ", W)

def ItemSimilarityImp(train):
#calculate co-rated users between items
  C = {}
  N = {}
  for user, items in train.items():
    for i in items:
      C.setdefault(i,{})
      N.setdefault(i,0)
      N[i] += 1
      for j in items:
        if i == j:
          continue
        C[i].setdefault(j,0)
        C[i][j] += 1 / math.log(1 + len(items) * 1.0)
#calculate finial similarity matrix W
  for i,related_items in C.items():
    W.setdefault(i,{})
    for j, cij in related_items.items():
      W[i][j] = cij / math.sqrt(N[i] * N[j])
  # print("W: ", W)

def RecommendN(user, train, K, N):
  rank = {}
  ui = train[user]
  for i in ui:
    for j, wj in sorted(W[i].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
      if j in ui:
        continue
      rank.setdefault(j,0)
      #TBD the pi value represents the like degree of u to i
      pi = 1
      rank[j] += pi * wj
  n_rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[:N]
  # print ("rank: ", n_rank)
  return n_rank

def Recall(train, test, K, N):
  hit = 0
  all = 0
  for user in test.keys():
    tui = test[user]
    n_rank = RecommendN(user, train, K, N)
    for i, pui in n_rank:
      if i in tui:
        hit += 1
    all += len(tui)
  return hit/(all * 1.0)

def Precision(train, test, K, N):
  hit = 0
  all = 0
  for user in test.keys():
    tui = test[user]
    n_rank = RecommendN(user, train, K, N)
    for i, pui in n_rank:
      if i in tui:
        hit += 1
    all += N
  return hit/(all * 1.0)

def Coverage(train, test, K, N):
  recommend_items = set()
  all_items = set()
  for user in train.keys():
    for item in train[user]:
      all_items.add(item)
    rank = RecommendN(user, train, K, N)
    for item, pui in rank:
      recommend_items.add(item)
  return len(recommend_items) / (len(all_items) * 1.0)

def Popularity(train, test, K, N):
  item_popularity = dict()
  for user, items in train.items():
    for item in items:
      if item not in item_popularity:
        item_popularity[item] = 0
      item_popularity[item] += 1
  ret = 0
  n = 0
  for user in train.keys():
    rank = RecommendN(user, train, K, N)
    for item, pui in rank:
      ret += math.log(1 + item_popularity[item])
      n += 1
  ret /= n * 1.0
  return ret


if __name__ == '__main__':
  train, test, item_users = LoadData()
  ItemSimilarityImp(train)
  
  recall = Recall(train, test, 5, 10)
  precision = Precision(train, test, 5, 10)
  coverage = Coverage(train, test, 5, 10)
  popularity = Popularity(train, test, 5, 10)
  print ('test recall: ', recall)
  print ('test precision: ', precision)
  print ('test coverage: ', coverage)
  print ('test popularity: ', popularity)
