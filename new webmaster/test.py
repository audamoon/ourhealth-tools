with open("logs/result2023-11-20-18-42.txt", "r", encoding="UTF-8") as result_file:
    results = list(map(lambda x: x.split(";"), result_file.readlines()))

g = 0
results_ranged = [[]]

for i in range(1, len(results)):
    if int(results[i - 1][0]) + 1 == int(results[i][0]):
        results_ranged[g].append(results[i-1])
        if (i == len(results) - 1):
            results_ranged[g].append(results[i])
    if int(results[i - 1][0]) + 1 != int(results[i][0]):
        results_ranged[g].append(results[i-1])
        results_ranged.append([])
        g += 1
        if (i == len(results) - 1):
            results_ranged[g].append(results[i])

print(results_ranged)

for rr in results_ranged:
    min_index = rr[0][0]
    max_index = rr[len(rr) - 1][0]
    print(min_index)
    print(max_index)
    print(list(map(lambda x: x[1], rr)))
