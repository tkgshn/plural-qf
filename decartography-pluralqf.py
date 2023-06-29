# %% [markdown]
# ## Data get from FDD Data-hub

# %%
# imports
import pandas as pd

# load data
FDDdata = "data/GR03_contributions.csv"
pd.read_csv(FDDdata)

# %% [markdown]
# ## Define Crowdworker's profile

# %%
#imports
import numpy as np

#define crowdworker class
class CrowdWorker:
    def __init__(self, name, humanity_score=0, staking_amount=0):
        self.name = name
        self.humanity_score = humanity_score
        self.staking_amount = staking_amount #optional
        self.weight = humanity_score + np.sqrt(staking_amount) #quadratic staking? the formula require to adjusting after experiment
        self.choices = [] #empty at first

#assume workers stats 
workers = [
    CrowdWorker('CrowdWorkerA', 10, 0), #weight 10
    CrowdWorker('CrowdWorkerB', 45, 0.1), #weight 45.3162
    CrowdWorker('CrowdWorkerC', 86, 0.05) #weigt 86.223
    ]

# %% [markdown]
# ## Generate Task for Crowdworker

# %%
import pandas as pd

# FDDdataをpandas DataFrameに読み込む（最初の20行だけ）
data = pd.read_csv(FDDdata, nrows=20)

# 'address'カラムをリストに変換
addresses = data['address'].tolist()


# %%
import random

#generate tasks from address list
def worker_selection(worker, addresses):
    random_addresses = random.sample(addresses, 9) #it's so simple implemenmtation, for generate task. must be improved as golden standerd? in production
    # instructions for the worker on command line
    print(f"{worker.name}, please choose 3 addresses from the following list by typing the corresponding numbers (separated by space):")
    for i, address in enumerate(random_addresses):
        print(f"{i}: {address}")
    
    # Get the worker's choices from the command line.
    while True:
        choices = input().split()
        
        # Make sure the worker's choices are valid.
        if all(0 <= int(choice) < 9 for choice in choices) and len(choices) == 3: #crowd worker is going to select 3 answers from 9 addresses
            break
        else:
            print("Invalid input. Please choose 3 addresses by typing the corresponding numbers (0-8) separated by space.")
    
    # Add the worker's choices to their list of choices.
    chosen_addresses = [random_addresses[int(choice)] for choice in choices]
    worker.choices.extend(chosen_addresses)
    return chosen_addresses

n_sessions = 3 #number of task per session(each crowdworker will do 3 tasks)
votes_matrix = np.zeros((len(addresses), len(addresses)))
worker_voting_power = {}

for worker in workers:
    for _ in range(n_sessions):
        chosen_addresses = worker_selection(worker, addresses)
        for address in chosen_addresses:
            votes_matrix[addresses.index(address), [addresses.index(chosen) for chosen in chosen_addresses]] += worker.weight
    print(f"Profile: Humanity Score - {worker.humanity_score}, Staking Amount - {worker.staking_amount}, Voting Weight - {worker.weight}")
    print(f"-------------")
    print(f"{worker.name} has finished their task. Please pass it on to the next person.")
    worker_voting_power[worker.name] = worker.weight * n_sessions

# %%
def peer_prediction(workers):
    correlation_scores = []
    for worker in workers:
        peers = [w for w in workers if w != worker]
        match_counts = [len(set(worker.choices).intersection(set(peer.choices))) for peer in peers]
        average_match_count = sum(match_counts) / len(match_counts)
        correlation_scores.append(average_match_count)
    return correlation_scores


# %%
import math

def calculate_rewards(workers, correlation_scores, total_reward=100):
    weighted_scores = [math.sqrt(worker.weight) * correlation_scores[i] for i, worker in enumerate(workers)]
    total_weighted_scores = sum(weighted_scores)
    reward_ratios = [score / total_weighted_scores for score in weighted_scores]
    rewards = [ratio * total_reward for ratio in reward_ratios]
    return rewards


# %%
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.expand_frame_repr', False)

def calculate_data(workers):
    data = {"Worker Name": [], "Total Voting Power": [], "Average Match Count": [], "Reward Distribution (%)": []}
    total_voting_power = {worker.name: worker.weight * n_sessions for worker in workers}

    correlation_scores = []
    for worker in workers:
        peers = [w for w in workers if w != worker]
        match_counts = [len(set(worker.choices).intersection(set(peer.choices))) for peer in peers]
        average_match_count = sum(match_counts) / len(match_counts)
        correlation_scores.append(average_match_count)

    total_reward = 100
    weighted_scores = [math.sqrt(worker.weight) * correlation_scores[i] for i, worker in enumerate(workers)]
    total_weighted_scores = sum(weighted_scores)
    reward_ratios = [score / total_weighted_scores for score in weighted_scores]
    rewards = [ratio * total_reward for ratio in reward_ratios]

    for i, worker in enumerate(workers):
        data["Worker Name"].append(worker.name)
        data["Total Voting Power"].append(total_voting_power[worker.name])
        data["Average Match Count"].append(correlation_scores[i])
        data["Reward Distribution (%)"].append(rewards[i])
        
    return data

# Calculate data
data = calculate_data(workers)

# Create DataFrame
df = pd.DataFrame(data)

# Display DataFrame
print(df)


try:
    correlation_scores = peer_prediction(workers)
except:
    correlation_scores = np.zeros((len(addresses), len(addresses)))

calculate_rewards(workers, correlation_scores)

pca = PCA(n_components=2)
votes_pca = pca.fit_transform(votes_matrix)

kmeans = KMeans(n_clusters=3, random_state=0)
clusters = kmeans.fit_predict(votes_pca)

clustered_addresses = {i+1: [] for i in range(max(clusters)+1)}

for i, cluster in enumerate(clusters):
    clustered_addresses[cluster+1].append(addresses[i])

for cluster, addresses in clustered_addresses.items():
    print(f"Cluster {cluster}: {addresses}")

# define input_data which is Cluster {cluster}: {addresses}
input_data = clustered_addresses

# plt.figure(figsize=(10,10))
# plt.scatter(votes_pca[:, 0], votes_pca[:, 1], c=clusters)

# for i, txt in enumerate(addresses):
#     plt.annotate(txt, (votes_pca[i, 0], votes_pca[i, 1]))

# plt.show()

# %%
def convert_data(input_data):
    category_indices = {category: idx for idx, category in enumerate(input_data.keys())}
    result = []

    # Add individual categories
    for category, names in input_data.items():
        result.append({"sets": [category_indices[category]], "label": category, "size": len(names)})

    # Calculate overlaps
    for i, (cat1, names1) in enumerate(input_data.items()):
        for j, (cat2, names2) in enumerate(input_data.items()):
            if j <= i:
                continue
            overlap_count = len(set(names1) & set(names2))
            result.append({"sets": [category_indices[cat1], category_indices[cat2]], "size": overlap_count})

    return result

output_data = convert_data(input_data)

print(output_data)


# # %%
# from IPython.display import display, Javascript, HTML


# html = """
# <head>
#     <meta charset="utf-8">
#     <title>Venn Diagram with venn.js in Jupyter Notebook</title>
# </head>
# <body>
#     <div id="venn"></div>
# </body>
# </html>
# """

# javascript = f"""
# require.config({{
#     paths: {{
#         d3: "https://d3js.org/d3.v4.min",
#         venn: "https://benfred.github.io/venn.js/venn"
#     }}
# }});

# require(['d3', 'venn'], function(d3, venn) {{
#     var data = {output_data};
#     var chart = venn.VennDiagram();
#     d3.select("#venn").datum(data).call(chart);
# }});
# """

# display(HTML(html))
# display(Javascript(javascript))


