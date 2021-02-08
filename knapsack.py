def optimal_knapsack(capacity, values, costs):

    # adding 0th column to values/costs on the y axis
    values = [0] + values
    costs = [0] + costs

    # initialising matrix kj
    k = []
    # adding 0th column to capacity on x axis
    list_budget_size = range(capacity + 1)
    m = range(len(list_budget_size))
    n = range(len(costs))

    for i in n:
        l = []
        for j in m:
            l.append(-1)
        k.append(l)

    # filling in matrix 'k'
    for i in n:
        for w in m:
            if i == 0 or w == 0:
                k[i][w] = 0
            elif costs[i] <= w:
                k[i][w] = max((values[i] + k[i - 1][w - costs[i]]), (k[i - 1][w]))
            else:
                k[i][w] = k[i - 1][w]

    # backtrack through matrix k to find included elements
    i = len(k) - 1
    j = len(k[0]) - 1
    included_items = []

    while i > 0 and j > 0:
        if k[i][j] != k[i - 1][j]:
            included_items.append(i)
            j = j - costs[i]
        i = i - 1

    return [i - 1 for i in included_items]