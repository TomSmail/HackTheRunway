
#tick off received or not

#stepped - including different levels of edge. Thus there could be several edges between people.

#maximum number of cycles.

#show it to all users and get them all to agree

def genGraph(conn):

  numUsers = len(conn.execute(text("SELECT * FROM Users")).fetchall())  
  edges = conn.execute(text("SELECT * FROM User_Has INNER JOIN User_Wants ON User_Has.ArticleID = User_Wants.ArticleID")).fetchall()
  
  graph = [[] for i in range(numUsers)]
  for row in res:
    graph[int(row["User_Has"])].append(int(row["User_Wants"]))
  
  return graph

