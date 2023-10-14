import datetime
import json
from scipy.stats import norm

# with open("../offices.txt", "r", encoding='utf-8') as f:
#     all_deps = json.loads(f.read())
#     for dep in all_deps:
#         point_name = dep["salePointName"]
#         openHours = dep["openHoursIndividual"]
#
#         for day in openHours:
#             print(day["days"])
#             print(day["hours"])
#             print()

# d = datetime.date.today()
# start_time = datetime.time(int("09".strip("0")), 0, 0)
# end_time = datetime.time(int("21".strip("0")), 0, 0)
#
# start_time = datetime.datetime.combine(d, start_time)
# end_time = datetime.datetime.combine(d, end_time)
#
# while end_time > start_time:
#     print(start_time, "-", start_time + datetime.timedelta(minutes=5))
#     print(start_time.hour)
#     start_time += datetime.timedelta(minutes=5)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# x-axis ranges from -3 and 3 with .001 steps
x = np.arange(8, 21, 1/12)

# plot normal distribution with mean 0 and standard deviation 1

y1 = [int(i * 250) for i in norm.pdf(x, 17, 3.5)]
y2 = [int(i * 5) for i in norm.pdf(x, 14, 0.5)]
y = []

for i in range(len(x)):
    y.append(y1[i] + y2[i])

plt.plot(x, y)
plt.show()
