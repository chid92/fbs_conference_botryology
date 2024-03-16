import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('matchups.csv')
G = nx.DiGraph()

for index, row in df.iterrows():
    if row['games'] != 0:
        G.add_edge(row['team1'], row['team2'], weight=(1 / row['games']))

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=5, font_weight="bold", arrowsize=1)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'),font_size=5, font_color='red')

plt.savefig('graph.png', format='png', bbox_inches='tight')
