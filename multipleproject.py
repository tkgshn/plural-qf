import math
from itertools import combinations as combinations
import numpy as np
import sys
import ast

def connection_oriented_cluster_match(groups, contributions):
    # groups: a 2d array. groups[i] is a list of people in group i (assume every person has an index).
    # contributions: a 2d array. contributions[i] is the amount agent i contributed to each project.

    agents = list(range(len(contributions)))

    if any(any(c < 0 for c in contributions[i]) for i in agents):
        raise NotImplementedError("negative contributions not supported")

    # memberships[i] is the number of groups agent i is in
    memberships = [len([g for g in groups if i in g]) for i in agents]

    # friend_matrix[i][j] is the number of groups that agent i and j are both in
    friend_matrix = [[len([g for g in groups if i in g and j in g])  for i in agents] for j in agents]

    # build up the funding amounts for each project
    funding_amounts = []

    for project in range(len(contributions[0])):
        # add in everyone's contributions to a specific project
        funding_amount = sum(contributions[i][project] for i in agents)

        def K(i, h):
            if sum([friend_matrix[i][j] for j in h]) > 0:
                return math.sqrt(contributions[i][project])
            return contributions[i][project]

        funding_amount += sum(2 * math.sqrt(sum(K(i,p[1])/memberships[i] for i in p[0])) * math.sqrt(sum(K(j,p[0])/memberships[j] for j in p[1])) for p in combinations(groups, 2))
        funding_amounts.append(funding_amount)

    return funding_amounts

fn_dict = {'cocm': connection_oriented_cluster_match}

def usage_info():
    print("usage: python3 pluralqf.py <function> <groups> <contributions>")
    print("available functions:")
    for k in fn_dict.keys():
        print("  " + k)
    exit()

try:
    f = fn_dict[sys.argv[1]]
except KeyError:
    usage_info()

try:
    groups = ast.literal_eval(sys.argv[2])
    contributions = ast.literal_eval(sys.argv[3])
except IndexError:
    usage_info()
except ValueError:
    usage_info()

print(fn_dict[sys.argv[1]](groups, contributions))
