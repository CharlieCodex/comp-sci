from funcs import np_firstcome, tough_customer, score_2
import random
import time
import numpy as np
import quickstart


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print(method.__name__, (te - ts) * 1000)
        return result
    return timed


def validate_slots(state, slots):
    slots = dict(slots)
    for person in state:
        slots[state[person][1]] -= 1
        if slots[state[person][1]] < 0:
            return False
    return True


def cost(state, target):
    return (
        cost1(state, target) / len(target),
        cost2(state, target) / len(target)**2,
        cost3(state, target) / np.log(len(target)),
    )


def cost1(state, target):
    _c = 0
    for person in state:
        if state[person] in target[person]:
            _c += target[person].index(state[person])
        else:
            _c += len(target[person])
    return _c


def cost2(state, target):
    _c = 0
    for person in state:
        if state[person] in target[person]:
            _c += target[person].index(state[person])**2
        else:
            _c += len(target[person])**2
    return _c


def cost3(state, target):
    _c = 0
    for person in state:
        if state[person] in target[person]:
            _c += 1 / (target[person].index(state[person]) + 1)
        else:
            _c += 1 / (len(target[person]) + 1)
    return _c


def gen_sample_data(classes, num_prefs, num=100):
    t = {}
    for n in range(num):
        name = 'Person ' + str(n)
        choices = list(classes)
        random.shuffle(choices)
        choices = choices[:num_prefs]
        t[name] = choices
    return t


def test_np_funcs(class_dict, num_prefs, num=100):
    data = {
        "firstcome": [],
        "tc": [],
        "tc2": [],
        "__targets": []
    }
    slots = dict(class_dict)
    for epoch in range(num):
        print("epoch", epoch)
        t = gen_sample_data(slots.keys(), num_prefs, 400)
        for _ in range(1):
            data["__targets"].append(t)
            data["firstcome"].append(np_firstcome(t, slots))
            data["tc"].append(tough_customer(t, slots))
            data["tc2"].append(tough_customer(t, slots, score_2))
    return data


def avg_cost(data):
    data = dict(data)

    targets = data["__targets"]
    del data["__targets"]

    costs = {func: [] for func in data}
    for func in data:
        for index, entry in enumerate(data[func]):
            costs[func].append(cost(entry, targets[index]))
    stats = {}
    for func in costs:
        stat = stats[func] = {}
        stat["mean"] = np.mean(costs[func], 0)
        stat["std"] = np.std(costs[func], 0)
    return stats


sheets = quickstart.Sheets()


def get_class_slots(sheet):
    raw = sheets.get_range(sheet, "Classes!A2:C")
    slots_dict = {row[0]: int(row[2]) for row in raw}
    return slots_dict


def get_class_preferences(sheet):
    raw = sheets.get_range(sheet, "Copy of Student Preferences!A2:N")
    preference_dict = {row[0]: row[6:] for row in raw}
    return preference_dict


def write_state(sheet, state):
    data = [list(state[person])
            for person in sorted(state.keys(), key=lambda x: int(x[1:]))]
    sheets.write_to_range(sheet, 'Copy of Student Preferences!E2:F', data)
