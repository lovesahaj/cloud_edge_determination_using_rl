import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv("Sequential_simulation.csv")
df = df.drop("Orchestration architecture", axis=1)
df = df.drop(df.columns[-2:], axis=1)

# df = df[~df['Orchestration algorithm'].isin(['TEST', 'LOCAL', 'MIST', 'EDGE', 'CLOUD', 'RANDOM_GOOD', 'CLOSEST'])]

columns = df.columns

group_by_algo = df.groupby('Orchestration algorithm').mean()
algo_names = df['Orchestration algorithm'].unique()
algo_res = dict()

for name in algo_names:
    algo_res[name] = df[df['Orchestration algorithm'] == name]

for col in columns:
    fig, ax = plt.subplots(1, figsize=(15, 15))
    for algo in algo_res.keys():
        sns.lineplot(algo_res[algo], x='Edge devices count', y=col, ax=ax, label=algo)

    fig.savefig(f"{col.replace('/', '')}.png")
