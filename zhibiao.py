
def Recall(train, test, N):
  hit = 0
  all = 0
  for user in train.keys():
    tui = test[user]
    n_rank = RecommendN(user, trian, N)
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
    n_rank = RecommendN(user, trian, N)
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
    for item in items
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