
#tick off received or not

#stepped - including different levels of edge. Thus there could be several edges between people.

#maximum number of cycles.

#show it to all users and get them all to agree

def genGraph(conn):

  numUsers = int(conn.execute(text("SELECT UserID FROM Users")).fetchall()[-1]["UserID"])
  edges = conn.execute(text("SELECT * FROM User_Has INNER JOIN User_Wants ON User_Has.ArticleID = User_Wants.ArticleID")).fetchall()
  
  graph = {}
  for row in res:
    if int(row["User_Has"]) in graph:
      graph[int(row["User_Has"])].append(int(row["User_Wants"]))
    else:
      graph[int(row["User_Has"])] = []

  return graph

