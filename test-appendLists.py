import numpy as np
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s:%(funcName)s:%(process)d:%(message)s"
)


def second():
    list2 = []

    for j in range(10):
        n = str(np.random.rand() * 100)
        list2.append(n)
    return list2


list1 = []
for i in range(10):
    u = str(np.random.rand() * 100)
    list1.append(u)
logging.debug(list1)

list1.extend(second())
logging.debug(list1)
