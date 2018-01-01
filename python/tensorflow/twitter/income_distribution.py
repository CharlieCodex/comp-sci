import matplotlib.pyplot as plt
import numpy as np
import wbdata


def aggregate(data, k_x, k_y):
    countries = {}
    for entry in data:
        country = entry['country']['id']
        if country not in countries:
            countries[country] = ([], [], entry['country']['value'])
        countries[country][0].append(entry[k_x])
        countries[country][1].append(entry[k_y])
    return countries


data = wbdata.get_data('SP.POP.TOTL', country=("XP", "1W", "XD", "XM"))
agg = aggregate(data, 'date', 'value')


def safe_div(a, b):
    if a is None or b is None:
        return None
    return float(a) / float(b)


def mapper(tpl):
    i, v = tpl
    return safe_div(v, agg['1W'][1][i])


for country in (c for c in agg if c != '1W'):
    plt.plot(agg[country][0],
             list(map(mapper, enumerate(agg[country][1]))),
             label=agg[country][2])

xi = np.arange(1960, 2018, 10)
plt.xlabel('Year')
plt.ylabel('Population of Group')
plt.xticks(xi, xi)
plt.legend()
plt.show()
