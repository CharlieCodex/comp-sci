from functools import reduce
import random


def np_firstcome(target, class_slots, offset=0):
    class_slots = dict(class_slots)
    state = {}
    _target = dict(target)
    keys = list(_target.keys())
    random.shuffle(keys)
    for person in keys:
        for pref in _target[person]:
            if class_slots[pref] > 0:
                class_slots[pref] -= 1
                state[person] = pref
                break
    if len(state) < len(target):
        _target = {person: _target[person]
                   for person in
                   set(_target.keys()).difference(set(state.keys()))}
        state.update(lottery(target, class_slots, offset))
    return state


def priority(target, class_slots):
    class_slots = dict(class_slots)
    _target = dict(target)
    _dict = {}
    for person in _target:
        if target[person][0] in _dict:
            _dict[target[person][0]].append((person, _target[person][1:]))
        else:
            _dict[target[person][0]] = [(person, _target[person][1:])]
    state = {}
    if len(_dict) == 0:
        return {}
    for cl in _dict:
        for person, _ in _dict[cl]:
            if class_slots[cl] > 0:
                class_slots[cl] -= 1
                state[person] = cl
            else:
                break
    _keys = set(_target.keys()).difference(set(state.keys()))
    __target = {k: _target[k][:1] for k in _keys}
    if len(state) == 0:
        for person in __target:
            for cl in {_cl: class_slots[_cl] for _cl in class_slots if class_slots[_cl] > 0}:
                state[person] = cl
                class_slots[cl] -= 1
                break
        return state
    state.update(priority(__target, class_slots))
    return state


def score_1(class_desireability):
    def score(class_preferences):
        return reduce(
            lambda x, y: x + class_desireability[y],
            class_preferences, 0)
    return score


def score_2(class_desireability):
    def score(class_preferences):
        return reduce(
            lambda x, y: x * class_desireability[y],
            class_preferences, 0)
    return score


def tough_customer(class_requests, class_slots, score=score_1, depth=0):
    if len(class_requests) == 0 or len(
            class_requests[next(iter(class_requests))]) == 0:
        return np_firstcome(class_requests, class_slots)
    class_slots = dict(class_slots)
    class_signups = {cl: 0 for cl in class_slots}
    for person in class_requests:
        cl = class_requests[person][0]
        if cl in class_signups:
            class_signups[cl] += 1
        else:
            class_signups[cl] = 1

    class_desireability = {k: v - (class_slots[k] + 1)
                           for k, v in class_signups.items()}

    score_func = score(class_desireability)

    keys = sorted(class_requests.keys(),
                  key=lambda k: score_func(class_requests[k]))
    state = {}

    for person in keys:
        for index, cl in enumerate(class_requests[person]):
            if class_slots[cl] > 0:
                class_slots[cl] -= 1
                state[person] = (index + depth, cl)
            break

    keys = set(class_requests.keys()).difference(set(state.keys()))
    if len(state) == 0:
        state = np_firstcome(class_requests, class_slots, offset=0)
        return state
    class_requests = {person: class_requests[person][1:] for person in keys}
    state.update(tough_customer(class_requests, class_slots, depth=depth + 1))
    return state


def lottery(class_preferences, class_slots, offset=0):
    state = {}
    for person in class_preferences:
        for index, cl in enumerate(class_preferences[person]):
            if class_slots[cl] > 0:
                class_slots[cl] -= 1
                state[person] = (index + offset, cl)
                break
        else:
            for cl in class_slots:
                if class_slots[cl] > 0:
                    class_slots[cl] -= 1
                    state[person] = (9, cl)
                    break
    return state
