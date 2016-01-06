import sys
import operator
import math
import random
#records = [[user1,item1,tag1],[user2,item2,tag2]...]
#user_tags = {u,{b:counts}}
#user_items = {u,{i:counts}}
#tag_items = {b,{i:counts}}
#recomment_items = {i: value}
#recomment_n = [i: value] top N list
#train = {user:[item1, item2...]}
user_tags = {}
user_items = {}
tag_items = {}
item_tags = {}
def LoadDataRecords():
  records = []
  TrainFile = 'Delicious/user_taggedbookmarks-timestamps.dat'
  with open(TrainFile,'r') as file_object:
    for line in file_object:
      (userId, itemId, tagId, timestamp) = line.strip().split('\t')
      itemList = []
      itemList.append(userId)
      itemList.append(itemId)
      itemList.append(tagId)
      records.append(itemList)
  # print ('records: ',records)
  return records

def SplitData(records, M, k, seed):
  test = {}
  train = {}
  random.seed(seed)
  for user, item, tag in records:
    test.setdefault(user, [])
    train.setdefault(user, [])
    if random.randint(0,M) == k:
      if user not in test:
        test[user] = list()
      test[user].append(item)
    else:
      if user not in train:
        train[user] = list()
      train[user].append(item)
  # print('test dataset: ', test)
  return train, test

def InitStat(records):
  for userId, itemId, tagId in records:
    user_tags.setdefault(userId, {})
    user_items.setdefault(userId, {})
    tag_items.setdefault(tagId, {})
    item_tags.setdefault(itemId, {})
    user_tags[userId].setdefault(tagId, 0)
    user_tags[userId][tagId] = user_tags[userId][tagId] + 1
    tag_items[tagId].setdefault(itemId, 0)
    tag_items[tagId][itemId] = tag_items[tagId][itemId] + 1
    user_items[userId].setdefault(itemId, 0)
    user_items[userId][itemId] = user_items[userId][itemId] + 1
    item_tags[itemId].setdefault(tagId, 0)
    item_tags[itemId][tagId] = item_tags[itemId][tagId] + 1
  # print ('user_tags: ', user_tags)
  # print ('user_items: ', user_items)
  # print ('tag_items: ', tag_items)
  # print ('item_tags: ', item_tags)
  return user_tags, user_items, tag_items, item_tags

def Recommend(user, N):
  recommend_items = {}
  tagged_items = user_items[user]
  for tag, wut in user_tags[user].items():
    for item, wti in tag_items[tag].items():
      if item in tagged_items.keys():
        continue
      if item not in recommend_items.keys():
        recommend_items[item] = wut * wti
      else:
        recommend_items[item] += wut * wti
  recommend_n = sorted(recommend_items.items(), key=operator.itemgetter(1), reverse=True)[:N]
  # print('recommend_n: ',recommend_n)
  return recommend_n

#Test result index
def CosineSim(item_tags, i, j):
  ret = 0
  for b, wib in item_tags[i].items():
    if b in item_tags[j].keys():
      ret += wib * item_tags[j][b]
  ni = 0
  nj = 0
  for b, w in item_tags[i].items():
    ni += w * w
  for b, w in item_tags[j].items():
    nj += w * w
  if ret == 0:
    return 0
  return ret / math.sqrt(ni * nj)

def Diversity(item_tags, recommend_items):
  ret = 0
  n = 0
  for i, value in recommend_items:
    for j, value in recommend_items:
      if i == j:
        continue
      ret += CosineSim(item_tags, i, j)
      n += 1
  print('Result Diversity: ', ret / (n * 1.0))
  return ret / (n * 1.0)

def Recall(train, test, N):
  hit = 0
  all = 0
  for user in train.keys():
    tui = test[user]
    n_rank = Recommend(user, N)
    for i, pui in n_rank:
      if i in tui:
        hit += 1
    all += len(tui)
  return hit/(all * 1.0)

def Precision(train, test, N):
  hit = 0
  all = 0
  for user in train.keys():
    tui = test[user]
    n_rank = Recommend(user, N)
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
    rank = Recommend(user, N)
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
    rank = Recommend(user, N)
    for item, pui in rank:
      ret += math.log(1 + item_popularity[item])
      n += 1
  ret /= n * 1.0
  return ret

if __name__ == '__main__':
  records  = LoadDataRecords()
  train, test = SplitData(records, 8, 2, 0.5)
  user_tags, user_items, tag_items, item_tags = InitStat(records)
  # recommend_n = Recommend('18481',18)
  # Diversity(item_tags, recommend_n)

  recall = Recall(train, test, 10)
  precision = Precision(train, test, 10)
  coverage = Coverage(train, test, 10)
  # popularity = Popularity(train, test, 10)
  print ('test recall: ', recall)
  print ('test precision: ', precision)
  print ('test coverage: ', coverage)
  # print ('test popularity: ', popularity)

