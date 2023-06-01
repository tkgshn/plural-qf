import math
from itertools import combinations as combinations
import numpy as np
import sys
import ast
import math
import matplotlib.pyplot as plt

def connection_oriented_cluster_match(groups, contributions):
    # groups: a 2d array. groups[i] is a list of people in group i (assume every person has an index).
    # contributions: an array. contributions[i] is the amount agent i contributed to a project.

    agents = list(range(len(contributions)))

    if any(contributions[i] < 0 for i in agents):
        raise ValueError("Negative contributions are not supported.")

    # memberships[i] is the number of groups agent i is in
    memberships = [len([g for g in groups if i in g]) for i in agents]

    # friend_matrix[i][j] is the number of groups that agent i and j are both in
    friend_matrix = [[len([g for g in groups if i in g and j in g])  for i in agents] for j in agents]

    # build up the funding amount. First, add in everyone's contributions
    funding_amount = sum(contributions)

    def K(i, h):
        if sum([friend_matrix[i][j] for j in h]) > 0:
            return math.sqrt(contributions[i])
        return contributions[i]

    funding_amount += sum(2 * math.sqrt(sum(K(i,p[1])/memberships[i] for i in p[0])) * math.sqrt(sum(K(j,p[0])/memberships[j] for j in p[1])) for p in combinations(groups, 2))

    return funding_amount

def simulate_contribution_changes(groups, contributions, agent_index, min_contribution, max_contribution, step):
    contribution_range = range(min_contribution, max_contribution + 1, step)
    funding_amounts = []

    for contribution in contribution_range:
        new_contributions = contributions.copy()
        new_contributions[agent_index] += contribution
        funding_amount = connection_oriented_cluster_match(groups, new_contributions)
        funding_amounts.append(funding_amount)

    return contribution_range, funding_amounts

# グラフの描画
plt.figure(figsize=(10, 6))
plt.xlabel("Contribution Add")
plt.ylabel("Funding Amount")
plt.suptitle('python3 pluralqf.py cocm [[0],[1,2],[2,3,4,5],[5,6]]" "[10, 1, 20, 10, 0, 15, 10]')
# plt.suptitle('181.00492455253504')
# plt.text(1.02, 0.5, "181.00492455253504", va='center', rotation=270)

plt.title("181.00492455253504")

# エージェントの情報
groups = [[0],[1,2],[2,3,4,5],[5,6]]
# contributions = [10, 10, 5, 20, 15, 25, 10]
contributions = [10, 1, 20, 10, 0, 15, 10]

# 各エージェントの寄付の変化に対するFunding amountのシミュレーションと描画
agent0_contribution_range, agent0_funding_amounts = simulate_contribution_changes(groups, contributions, 0, 0, 100, 1)
agent1_contribution_range, agent1_funding_amounts = simulate_contribution_changes(groups, contributions, 1, 0, 100, 1)
agent2_contribution_range, agent2_funding_amounts = simulate_contribution_changes(groups, contributions, 2, 0, 100, 1)
agent3_contribution_range, agent3_funding_amounts = simulate_contribution_changes(groups, contributions, 3, 0, 100, 1)
agent4_contribution_range, agent4_funding_amounts = simulate_contribution_changes(groups, contributions, 4, 0, 100, 1)
agent5_contribution_range, agent5_funding_amounts = simulate_contribution_changes(groups, contributions, 5, 0, 100, 1)
agent6_contribution_range, agent6_funding_amounts = simulate_contribution_changes(groups, contributions, 6, 0, 100, 1)

# plt.plot(agent0_contribution_range, agent0_funding_amounts, label="Agent 0")
# plt.plot(agent1_contribution_range, agent1_funding_amounts, label="Agent 1")
# plt.plot(agent2_contribution_range, agent2_funding_amounts, label="Agent 2")
# plt.plot(agent3_contribution_range, agent3_funding_amounts, label="Agent 3")
# plt.plot(agent4_contribution_range, agent4_funding_amounts, label="Agent 4")
# plt.plot(agent5_contribution_range, agent5_funding_amounts, label="Agent 5")
# plt.plot(agent6_contribution_range, agent6_funding_amounts, label="Agent 6")

plt.plot(agent0_contribution_range, agent0_funding_amounts, label="Agent 0", color="blue")
plt.plot(agent1_contribution_range, agent1_funding_amounts, label="Agent 1", color="orange")
plt.plot(agent2_contribution_range, agent2_funding_amounts, label="Agent 2", color="green")
plt.plot(agent3_contribution_range, agent3_funding_amounts, label="Agent 3", color="red")
plt.plot(agent4_contribution_range, agent4_funding_amounts, label="Agent 4", color="purple")
plt.plot(agent5_contribution_range, agent5_funding_amounts, label="Agent 5", color="brown")
plt.plot(agent6_contribution_range, agent6_funding_amounts, label="Agent 6", color="gray")


plt.legend()
plt.show()
