from fashionmatch.db import get_db


def genGraph():
    db, cur = get_db()
    cur.execute("""SELECT * FROM "User";""")

    users = [a["userid"] for a in cur.fetchall()]

    cur.execute(
        """SELECT * FROM "User_Has" INNER JOIN "User_Wants" ON "User_Has".articleid = "User_Wants".articleid""")
    edges = cur.fetchall()

    graph = {uid: [] for uid in users}

    for row in edges:
        hasUser = int(row["hasuserid"])
        wantsUser = int(row["wantsuserid"])
        hasID = int(row["hasid"])
        wantsID = int(row["wantsid"])
        graph[hasUser].append(
            {"v": int(wantsUser), "HasID": hasID, "WantsID": wantsID})

    return graph


def cycleFind(graph):
    # Use closure to avoid creating a local copy of variables which wastes memory and time, while still creating maintainable code

    #dfs_parent = [0 for i in range(len(graph))]
    s = {"Unvisited": 0, "JustVisited": 1,
         "FullyExplored": 2, "CycleSeen": 3, "CycleFirst": 4}
    # print(graph)
    dfs_state = {key: s["Unvisited"] for key in graph}
    currentCycle = []
    cycles = []
    # ALL CCs

    def cycleFindInner(u):
        """Locate Cycles in an unweighted, directed Graph.
           Freely adapted from : https://github.com/stevenhalim/cpbook-code/blob/master/ch4/traversal/cyclecheck.cpp (Steven Halim, Felix Halim, Suhendry Effendy)"""
        nonlocal currentCycle, dfs_state, cycles, dfs_visited  # to be able to update from enclosing scope

        # print(u)
        # print(dfs_state)
        dfs_visited[u] = True  # Needed to ensure we visited all SCCs

        # Update state of this node (but don't reset it if it's already part of the current cycle)
        if (dfs_state[u] != s["CycleSeen"]):
            dfs_state[u] = s["JustVisited"]

        for dest in graph[u]:  # DFS - all adjacent nodes
            v = dest["v"]
            # not seen yet so recurse. If we are currently exploring a cycle we don't want to start looking at new nodes since this would create larger cycles when smaller ones suffice, and we want small cycles where possible.
            if (dfs_state[v] == s["Unvisited"]) and (dfs_state[u] != s["CycleSeen"]):
                cycleFindInner(v)
            elif dfs_state[v] == s["JustVisited"]:  # Seen before so we've found a cycle
                #        print("bb" + str(dfs_state[u]))
                # save this info so we can start to trace all elements in that cycle
                dfs_state[v] = s["CycleSeen"]
                # Provided we are on the first loop round this cycle
                if (dfs_state[u] != s["CycleSeen"]):
                    # remember that this node is the start of the cycle so we can stop when we locate it again
                    dfs_state[u] = s["CycleFirst"]
                currentCycle.append(dest)  # save node to current cycle
                cycleFindInner(v)  # recurse to discover rest of cycle
                # once the recursion unwinds, reset so this node can be part of other cycles if it needs to be
                dfs_state[v] = s["JustVisited"]
            elif (dfs_state[v] == s["CycleFirst"]):  # We got all the
                #        print("aa")
                currentCycle.append(dest)
                cycles.append(currentCycle)
                currentCycle = []

        print("Backtrack out of " + str(u))
        dfs_state[u] = s["FullyExplored"]

    dfs_visited = {key: False for key in graph}
    for key in graph:
        if not(dfs_visited[key]):
            cycleFindInner(key)

    return cycles
