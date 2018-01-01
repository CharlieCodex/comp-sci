import numpy as np
import matplotlib.pyplot as plt


def prep_hist(state, target, num_prefs):
    categories = {i: 0 for i in range(num_prefs + 1)}
    for person in state:
        if state[person] in target[person]:
            categories[target[person].index(state[person])] += 1
        else:
            categories[num_prefs] += 1
    return categories


def draw_hist(data, num_prefs):
    func_data = {}
    for func in data:
        if func == "__targets":
            continue
        func_data[func] = [
            prep_hist(data[func][i], data["__targets"][i], num_prefs)
            for i in range(len(data[func]))
        ]

        result = {
            i: 0
            for i in range(len(func_data[func][0]))
        }

        for entry in func_data[func]:
            for category in entry:
                result[category] += entry[category]
        for category in result:
            category /= len(func_data[func])
        func_data[func] = result
    final_result = {k: [] for k in func_data}
    for c in range(8):
        for func in func_data:
            final_result[func] += [c] * func_data[func][c]
        plt.hist(final_result[func])
    plt.show()
    return final_result


def draw_bar(data, num_prefs):
    performance = {}
    for func in data:
        if func == "__targets":
            continue
        performance[func] = [
            prep_hist(data[func][i], data["__targets"][i], num_prefs)
            for i in range(len(data[func]))
        ]

        result = np.zeros(num_prefs + 1)
        for entry in performance[func]:
            for category in entry:
                result[category] += entry[category]
        for category in result:
            category /= len(performance[func])
        performance[func] = result

    n_groups = num_prefs + 1
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.25
    opacity = 0.8
    rects = {}
    for i, func in enumerate(performance):
        rects[func] = plt.bar(index + i * bar_width,
                              performance[func],
                              bar_width,
                              alpha=opacity,
                              label=func)

    plt.xlabel('Choice Assigned')
    plt.ylabel('Number of placements')
    plt.title('Placement Distribution by Function')
    plt.xticks(index + bar_width,
               [str(i + 1) for i in range(num_prefs)] + ["Random"])
    plt.legend()

    plt.show()
