import sys
import operator
import math

W = {}

def LoadData():
  #train = {userId:[iterm1, item2...]} the same as test dict
  #W = {u:{v:value}} the same as C
  #item_users = {item, [user1,user2...]}
  #N(u) = {u:value} The number of items user u like 
  test = {}
  train = {}
  TrainFile = 'ml-100k/u2.base'
  TestFile = 'ml-100k/u2.test'
  # TestFile = 'u.test'
  #load train file
  with open(TrainFile,'r') as file_object:
    for line in file_object:
      (userId, itemId, rating, _) = line.strip().split('\t')
      train.setdefault(userId,[])
      if userId not in train:
        train[userId] = itemId
      else:
        train[userId].append(itemId)
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
  return train, test

# def UserSimilarityC(train):
#   W = {}
#   for u in train.keys():
#     W.setdefault(u,{})
#     for v in train.keys():
#       W[u].setdefault(v,0)
#       if u==v:
#         continue
#       W[u][v] = len(list(set(train[u]).intersection(set(train[v]))))
#       W[u][v] = W[u][v] / math.sqrt(len(train[u]) * len(train[v]) * 1.0)
#   print("W[u][v]: ", W)

def UserSimilarityS(train):
  # build inverse table for item_users
  item_users = {}
  for u,items in train.items():
    for i in items:
      if i not in item_users.keys():
        item_users[i] = list()
      item_users[i].append(u)
  # print("item_users: %s"%item_users)
  #calculate co-rated items between users
  C = {}
  N = {}
  for item, users in item_users.items():
    for u in users:
      C.setdefault(u,{})
      N.setdefault(u,0)
      N[u] += 1
      for v in users:
        if u==v:
          continue
        C[u].setdefault(v,0)
        C[u][v] += 1
  # print ("C[u][v]: %s"%C)
  #calculate finial similarity matrix W

  for u,related_users in C.items():
    W.setdefault(u,{})
    for v,cuv in related_users.items():
      W[u][v] = cuv / math.sqrt(N[u] * N[v])
  # print ("W: %s"%W)

def RecommendN(user, train, N):
  rank = {}
  rank.setdefault(user,{})
  interacted_items = train[user]
  for v,wuv in sorted(W[user].items(), key=operator.itemgetter(1), reverse=True)[0:5]:
    for i in train[v]:
      if i in interacted_items:
        #we should filter items user interacted before
        continue
      rank[user].setdefault(i,0)
      #TBD the rvi value represents the like degree of v to i
      rvi = 1
      rank[user][i] += wuv * rvi
  n_rank = sorted(rank[user].items(), key=operator.itemgetter(1), reverse=True)[:N]
  # print ("rank: %s"%n_rank)
  return n_rank


def Recall(train, test, N):
  hit = 0
  all = 0
  for user in test.keys():
    tui = test[user]
    n_rank = RecommendN(user, train, N)
    for i, pui in n_rank:
      if i in tui:
        hit += 1
    all += len(tui)
  return hit/(all * 1.0)

def Precision(train, test, N):
  hit = 0
  all = 0
  for user in test.keys():
    tui = test[user]
    n_rank = RecommendN(user, train, N)
    for i, pui in n_rank:
      if i in tui:
        hit += 1
    all += N
  return hit/(all * 1.0)

def Coverage(train, test, N):
  recommend_items = set()
  all_items = set()
  for user in train.keys():
    for item in train[user]:
      all_items.add(item)
    rank = RecommendN(user, train, N)
    for item, pui in rank:
      recommend_items.add(item)
  return len(recommend_items) / (len(all_items) * 1.0)

def Popularity(train, test, N):
  item_popularity = dict()
  for user, items in train.items():
    for item in items:
      if item not in item_popularity:
        item_popularity[item] = 0
      item_popularity[item] += 1
  ret = 0
  n = 0
  for user in train.keys():
    rank = RecommendN(user, train, N)
    for item, pui in rank:
      ret += math.log(1 + item_popularity[item])
      n += 1
  ret /= n * 1.0
  return ret

if __name__ == '__main__':
  train, test  = LoadData()
  UserSimilarityS(train)

  recall = Recall(train, test, 10)
  precision = Precision(train, test, 10)
  coverage = Coverage(train, test, 10)
  popularity = Popularity(train, test, 10)
  print ('test recall: ', recall)
  print ('test precision: ', precision)
  print ('test coverage: ', coverage)
  print ('test popularity: ', popularity)