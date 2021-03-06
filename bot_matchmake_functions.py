import numpy as np
import random

# [tankSR, dpsSR, suppSR, ready]
# build 2 teams of 6

# /* Build a function that takes playerData. minimize SR diff; return the following:
# Matchmaker output:
# Team A: (avg SR)
# P1  P4
# P2	P5
# P3	P6
# Team B: (avg SR)
# P4	P7
# P5	P8
# P6	P9  */##
# prefer 0 = no preference, 1 = mt, 2 = ot, 3 = dps, 4 = support

# Map pool
mapList = ['Blizzard World', 'Busan', 'Dorado',
           'Eichenwalde', 'Hanamura', 'Havana',
           'Hollywood', 'Ilios', 'Junkertown',
           'King\'s Row', 'Lijiang Tower', 'Nepal',
           'Numbani', 'Oasis', 'Rialto',
           'Route 66', 'Temple of Anubis', 'Volskaya Industries',
           'Watchpoint: Gibraltar']

mapList2 = ['Blizzard World', 'Busan', 'Dorado',
            'Eichenwalde', 'New York Cit', 'Havana',
            'Hollywood', 'Ilios', 'Junkertown',
            'King\'s Row', 'Lijiang Tower', 'Nepal',
            'Numbani', 'Oasis', 'Rialto',
            'Route 66', 'Toronto', 'Rome',
            'Watchpoint: Gibraltar', 'Rio de Janeiro',
            'Gothenburg', 'Monte Carlo', 'India']


# main matchmaking function
# chooses 12 players, splits into roles, matchmakes roles, and then combines them back together
def matchmake(playerData):
    queued = 0
    for i in playerData.keys():
        if playerData[i]['queue'] != 'none':
            queued += 1
    if queued < 12:
        return [-1, -1]

    roles = split(playerData)

    tank = roles[0]
    dps = roles[1]
    supp = roles[2]

    t = balance(tank)
    d = balance(dps)
    s = balance(supp)

    return combine(playerData, t, d, s)


# ready is a bool
# playerData is a hash table of any number of people
# splits all players into their chosen roles, then selects 4 for each role
def split(playerData):
    tank = []
    dps = []
    supp = []

    for name in playerData.keys():
        role = playerData[name]['queue']
        if role == 'tank':
            tank.append([name, playerData[name]['tank']])
        elif role == 'dps':
            dps.append([name, playerData[name]['dps']])
        elif role == 'support':
            supp.append([name, playerData[name]['support']])

    return [select(tank), select(dps), select(supp)]


# selects 4 players from a pool of any number
# role comes in as a list, returns a list of the randomly selected players
def select(role):
    # print(len(role))
    selected = []
    nums = np.random.choice(len(role), 4, replace=False)
    for i in range(len(nums)):
        selected.append(role[i])
    return selected


# given a role hash table
# add to the value bucket a new entry, Team A or B
# 6 members on A, 6 on B
# as even SR spread as possible
# Assume that role is a list of length 4
def balance(role):
    bestPair = []
    average2 = 0
    bestDifference = 5000
    totalsr = 0
    for i in range(len(role)):
        totalsr += role[i][1]

    for i in range(1, len(role)):
        avg1 = (role[0][1] + role[i][1]) / 2
        avg2 = (totalsr - role[0][1] - role[i][1]) / 2
        difference = avg1 - avg2
        if abs(difference) < abs(bestDifference):
            average2 = avg2
            bestDifference = difference
            bestPair = [avg1, role[0][0], role[i][0]]

    otherPair = [average2]
    for i in range(len(role)):
        if not (role[i][0] in bestPair):
            otherPair.append(role[i][0])

    both = [bestPair, otherPair]
    return both


# list.insert(0, thing-to-insert)
# to prepend things to a list ^^^

# combines the different roles into a team
# average sr is first element in both team A and team B
# good work team
def combine(playerData, tank, dps, supp):
    dReverse = False
    sReverse = False
    tankDiff = tank[0][0] - tank[1][0]
    dpsDiff = dps[0][0] - dps[1][0]
    suppDiff = supp[0][0] - supp[1][0]
    average1 = tank[0][0]
    average2 = tank[1][0]
    playerData[tank[0][1]]['team'] = 1
    playerData[tank[0][2]]['team'] = 1
    playerData[tank[1][1]]['team'] = 2
    playerData[tank[1][2]]['team'] = 2

    # brute force calculation of combined sr average
    bestDiff = tankDiff + dpsDiff + suppDiff
    if abs(tankDiff - dpsDiff + suppDiff) < abs(bestDiff):
        bestDiff = tankDiff - dpsDiff + suppDiff
        sReverse = False
        dReverse = True
    if abs(tankDiff + dpsDiff - suppDiff) < abs(bestDiff):
        bestDiff = tankDiff + dpsDiff - suppDiff
        dReverse = False
        sReverse = True
    if abs(tankDiff - dpsDiff - suppDiff) < abs(bestDiff):
        bestDiff = tankDiff - dpsDiff - suppDiff
        dReverse = True
        sReverse = True

    # add to team A or B depending on above calculations
    if dReverse:
        playerData[dps[1][1]]['team'] = 1
        playerData[dps[1][2]]['team'] = 1
        playerData[dps[0][1]]['team'] = 2
        playerData[dps[0][2]]['team'] = 2
        average1 += dps[1][0]
        average2 += dps[0][0]
    else:
        playerData[dps[0][1]]['team'] = 1
        playerData[dps[0][2]]['team'] = 1
        playerData[dps[1][1]]['team'] = 2
        playerData[dps[1][2]]['team'] = 2
        average1 += dps[0][0]
        average2 += dps[1][0]

    if sReverse:
        playerData[supp[1][1]]['team'] = 1
        playerData[supp[1][2]]['team'] = 1
        playerData[supp[0][1]]['team'] = 2
        playerData[supp[0][2]]['team'] = 2
        average1 += supp[1][0]
        average2 += supp[0][0]
    else:
        playerData[supp[0][1]]['team'] = 1
        playerData[supp[0][2]]['team'] = 1
        playerData[supp[1][1]]['team'] = 2
        playerData[supp[1][2]]['team'] = 2
        average1 += supp[0][0]
        average2 += supp[1][0]

    return [playerData, int(average1 / 3), int(average2 / 3)]


# Selects a random map from the map pool
def randomMap():
    i = random.randint(0, 18)
    return mapList[i]


# main matchmaking function
# chooses 12 players, splits into roles, matchmakes roles, and then combines them back together
def matchmake2(playerData):
    t_queued = 0
    d_queued = 0
    s_queued = 0

    for i in playerData.keys():
        if playerData[i]['queue'] == 'tank':
            t_queued += 1
        if playerData[i]['queue'] == 'dps':
            d_queued += 1
        if playerData[i]['queue'] == 'support':
            s_queued += 1
    if t_queued < 2 or d_queued < 4 or s_queued < 4:
        return [-1, -1]

    roles = split(playerData)

    tank = roles[0]
    dps = roles[1]
    supp = roles[2]

    t_idx = np.random.choice(len(tank), 2, replace=False)
    t = [tank[t_idx[0]], tank[t_idx[1]]]
    d = balance(dps)
    s = balance(supp)

    return combine2(playerData, t, d, s)


def combine2(playerData, tank, dps, supp):
    dReverse = False
    sReverse = False
    tankDiff = tank[0][1] - tank[1][1]
    dpsDiff = dps[0][0] - dps[1][0]
    suppDiff = supp[0][0] - supp[1][0]
    average1 = tank[0][1]
    average2 = tank[1][1]
    playerData[tank[0][0]]['team'] = 1
    playerData[tank[1][0]]['team'] = 2

    # brute force calculation of combined sr average
    bestDiff = tankDiff + dpsDiff + suppDiff
    if abs(tankDiff - dpsDiff + suppDiff) < abs(bestDiff):
        bestDiff = tankDiff - dpsDiff + suppDiff
        sReverse = False
        dReverse = True
    if abs(tankDiff + dpsDiff - suppDiff) < abs(bestDiff):
        bestDiff = tankDiff + dpsDiff - suppDiff
        dReverse = False
        sReverse = True
    if abs(tankDiff - dpsDiff - suppDiff) < abs(bestDiff):
        bestDiff = tankDiff - dpsDiff - suppDiff
        dReverse = True
        sReverse = True

    # add to team A or B depending on above calculations
    if dReverse:
        playerData[dps[1][1]]['team'] = 1
        playerData[dps[1][2]]['team'] = 1
        playerData[dps[0][1]]['team'] = 2
        playerData[dps[0][2]]['team'] = 2
        average1 += dps[1][0]
        average2 += dps[0][0]
    else:
        playerData[dps[0][1]]['team'] = 1
        playerData[dps[0][2]]['team'] = 1
        playerData[dps[1][1]]['team'] = 2
        playerData[dps[1][2]]['team'] = 2
        average1 += dps[0][0]
        average2 += dps[1][0]

    if sReverse:
        playerData[supp[1][1]]['team'] = 1
        playerData[supp[1][2]]['team'] = 1
        playerData[supp[0][1]]['team'] = 2
        playerData[supp[0][2]]['team'] = 2
        average1 += supp[1][0]
        average2 += supp[0][0]
    else:
        playerData[supp[0][1]]['team'] = 1
        playerData[supp[0][2]]['team'] = 1
        playerData[supp[1][1]]['team'] = 2
        playerData[supp[1][2]]['team'] = 2
        average1 += supp[0][0]
        average2 += supp[1][0]

    return [playerData, int(average1 / 3), int(average2 / 3)]


def split2(playerData):
    tank = []
    dps = []
    supp = []

    for name in playerData.keys():
        role = playerData[name]['queue']
        if role == 'tank':
            tank.append([name, playerData[name]['tank']])
        elif role == 'dps':
            dps.append([name, playerData[name]['dps']])
        elif role == 'support':
            supp.append([name, playerData[name]['support']])

    return [select2(tank), select(dps), select(supp)]


def select2(role):
    # print(len(role))
    selected = []
    nums = np.random.choice(len(role), 2, replace=False)
    for i in range(len(nums)):
        selected.append(role[i])
    return selected


# Selects a random map from the map pool
def randomMap2():
    i = random.randint(0, 18)
    return mapList2[i]
