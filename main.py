import functools
import random
import time
import bisect
import collections
import math


def take_closest(myList, myNumber):
    pos = bisect.bisect_left(myList, myNumber)
    if pos == 0:
        return tuple([myList[0]])
    if pos == len(myList):
        return tuple([myList[-1]])
    before = myList[pos - 1]
    after = myList[pos]
    return before, after


def linearApprox(maxSize=10, intVals=True, returnCached=False):
    def linearApproxDecorator(func):
        calculated = collections.OrderedDict()

        @functools.wraps(func)
        def wrapper_decorator(x):
            nonlocal calculated
            cached = False
            value = None
            sortedKeys = list(calculated.keys())
            if len(sortedKeys) > 0:
                closest = take_closest(sortedKeys, x)
                if len(closest) > 1:
                    closestBefore, closestAfter = closest
                    distB = abs(closestBefore - x)
                    distA = abs(closestAfter - x)
                    if intVals:
                        closestBefore, closestAfter = int(closestBefore), int(closestAfter)
                        distB = int(distB)
                        distA = int(distA)
                    if distA == 0:
                        value = calculated[closestAfter]
                        cached = True
                    elif distB == 0:
                        value = calculated[closestBefore]
                        cached = True
                    elif distB <= maxSize and distA <= maxSize:
                        slope = (calculated[closestAfter] - calculated[closestBefore]) // (closestAfter - closestBefore)
                        value = (slope * (x - closestBefore)) + calculated[closestBefore]
                        cached = True
            else:
                print('failed')
            if value is None:
                value = func(x)
                newCalculated = collections.OrderedDict()
                index = bisect.bisect(list(calculated.keys()), x)
                if len(calculated.keys()) > 0:
                    for i, k in enumerate(calculated.keys()):
                        newCalculated[k] = calculated[k]
                        if index == i+1:
                            newCalculated[x] = value
                        # print(k, calculated[k], i, index)
                else:
                    newCalculated[x] = value
                    # print('.')
                # calculated[x] = value
                calculated = newCalculated
                # print(list(zip(calculated.keys(), calculated.values())))
            if returnCached:
                return value, cached
            else:
                return value

        return wrapper_decorator

    return linearApproxDecorator


if __name__ == '__main__':
    lossSum = 0
    count = 0
    results = []
    delay = 0.00001
    # power = random.randint(3, 3000)
    power = 37
    num = 1000


    def sq(x):
        time.sleep(delay)
        return x ** power
        # return math.factorial(x)


    @linearApprox(10, returnCached=True)
    def sqla(x):
        time.sleep(delay)
        return x ** power
        # return math.factorial(x)


    l = list(range(num))
    random.shuffle(l)
    l1 = list(range(0, num, 9))
    l2 = [e for e in l if e not in l1]
    random.shuffle(l2)

    t1 = time.time()

    for i in l:
        result = sq(i)
        print(result)
        results.append(result)

    t1FinishTime = time.time()
    t2 = time.time()
    pc1 = 0
    # for i in l1:
    #     print(sqla(i))
    # for i in l2:
    #     print(sqla(i))
    for e in l:
        x1, x2 = sqla(e)
        print(x1)
        if x2:
            pc1 += 1

    t2FinishTime = time.time()

    t3 = time.time()
    pc2 = 0
    for i, e in enumerate(l):
        x1, x2 = sqla(e)
        try:
            loss = (abs(results[i] - x1) / abs(results[i]))
            lossSum += loss
            count += 1
            print(loss, ' ', x1)
        except ZeroDivisionError:
            pass
        if x2:
            pc2 += 1

    t3FinishTime = time.time()

    print()
    print()
    # print(time.time())
    print('full calculations:', t1FinishTime - t1)
    print('full approximation:', t2FinishTime - t2, pc1)
    print('cached approximation:', t3FinishTime - t3, pc2)
    print(lossSum/count)

    # while True:
    #     print(sqla(int(input())))
