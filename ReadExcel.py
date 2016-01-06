# -*- coding: utf-8 -*- 
# import  xdrlib
import sys
import xlrd
import operator
import math
W = {}
def open_excel(file= 'user_item_no0.xls'):
    try:
        print (xlrd.__file__)
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print (e)
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
def excel_table_byindex(file= 'user_item_no0.xls',colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(1,nrows):

         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = int(row[i])
             list.append(app)
    return list

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file= 'user_item_no0.xls',colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数 
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] =  row[i]
             list.append(app)

    return list

def LoadData():
  #train = {userId:[iterm1, item2...]} the same as test dict
  #W = {u:{v:value}} the same as C
  #item_users = {item, [user1,user2...]}
  #N(i) = {i:value} The number of users who like i 
  test = {}
  train = {}
  item_users = {}
  # tables = excel_table_byindex()
  tables = excel_table_byname()
  #load train file
  for row in tables:
    userId = row['User']
    itemId = row['Item']
    # train.setdefault(userId,[])
    if userId not in train:
      train[userId] = set()
    train[userId].add(itemId)

    if itemId not in item_users:
        item_users[itemId] = set()
    item_users[itemId].add(userId)
  # print("item_users: ", item_users)
  print("item_users numbers: ", len(item_users))
  print("train: ", len(train))
  return train, item_users

def FiltMultInterstUser(train):
  filted_users = {}
  for user,items in train.items():
    if len(items)>1:
      filted_users[user] = items
  print ('filted_users list: ', filted_users)
  return filted_users

def ItemSimilarity(train):
#calculate co-rated users between items
  # W = {}
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
  return W

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
  print("W: ", W)

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
  print ("rank: ", n_rank)
  return n_rank

def main():
   train, item_users = LoadData()
   filted_users = FiltMultInterstUser(train)
   W = ItemSimilarity(train)
   for user in train.keys():
     n_rank = RecommendN(user, train,2, 3)
     print('%s n_rank: %s'%(user,n_rank))

if __name__=="__main__":
    main()