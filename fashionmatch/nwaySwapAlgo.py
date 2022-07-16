def cycleFind(graph):
  #Use closure to avoid creating a local copy of variables which wastes memory and time, while still creating maintainable code
  
  #dfs_parent = [0 for i in range(len(graph))]
  s = {"Unvisited":0,"JustVisited":1,"FullyExplored":2,"CycleSeen":3,"CycleFirst":4}
  dfs_state = [s["Unvisited"] for i in range(len(graph))]  
  currentCycle = []
  cycles = []
  #ALL CCs
  
  def cycleFindInner(u):
    """Locate Cycles in an unweighted, directed Graph.
       Freely adapted from : https://github.com/stevenhalim/cpbook-code/blob/master/ch4/traversal/cyclecheck.cpp (Steven Halim, Felix Halim, Suhendry Effendy)"""
    nonlocal currentCycle,dfs_state,cycles,dfs_visited #to be able to update from enclosing scope

    # print(u)
    # print(dfs_state)
    dfs_visited[u] = True #Needed to ensure we visited all SCCs


    if (dfs_state[u] != s["CycleSeen"]): #Update state of this node (but don't reset it if it's already part of the current cycle)
      dfs_state[u] = s["JustVisited"]
      
    for v in graph[u]: #DFS - all adjacent nodes
      if (dfs_state[v] == s["Unvisited"]) and (dfs_state[u] != s["CycleSeen"]): #not seen yet so recurse. If we are currently exploring a cycle we don't want to start looking at new nodes since this would create larger cycles when smaller ones suffice, and we want small cycles where possible.
        cycleFindInner(v)
      elif dfs_state[v] == s["JustVisited"]: #Seen before so we've found a cycle
#        print("bb" + str(dfs_state[u]))
        dfs_state[v] = s["CycleSeen"] #save this info so we can start to trace all elements in that cycle
        if (dfs_state[u] != s["CycleSeen"]): # Provided we are on the first loop round this cycle
          dfs_state[u] = s["CycleFirst"] #remember that this node is the start of the cycle so we can stop when we locate it again
        currentCycle.append(v) #save node to current cycle
        cycleFindInner(v) #recurse to discover rest of cycle 
        dfs_state[v] = s["JustVisited"] #once the recursion unwinds, reset so this node can be part of other cycles if it needs to be
      elif (dfs_state[v] == s["CycleFirst"]): #We got all the 
#        print("aa")
        currentCycle.append(v) 
        cycles.append(currentCycle)
        currentCycle = []
        
        

    print("Backtrack out of " + str(u))
    dfs_state[u] = s["FullyExplored"]
        

  dfs_visited = [False for i in range(len(graph))]
  for i in range(len(graph)):
    if not(dfs_visited[i]):
      cycleFindInner(i)
  return cycles


graph = [
  [1],[0,2],[],[4],[3]
]

#graph = [
#  [1],[2,5],[3],[],[5],[6],[0]
#]

# A <-> B <-> C <-> A aaaagh
find cycles every time a new garment is selected

print(cycleFind(graph))