import pandas as pd
import networkx as nx
import itertools
import random
import matplotlib.pyplot as plt
from tqdm import tqdm


class CFGraph:
    def __init__(self, filename):
        self.graph = nx.DiGraph()
        for index, row in pd.read_csv(filename).iterrows():
            self.graph.add_edge(row['team1'], row['team2'], weight=row['games'])

        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos,
                with_labels=True,
                node_size=1000,
                node_color="skyblue",
                font_size=5,
                font_weight="bold",
                arrowsize=1)
        nx.draw_networkx_edge_labels(self.graph, pos,
                                     edge_labels=nx.get_edge_attributes(self.graph, 'weight'),
                                     font_size=5,
                                     font_color='red')
        plt.savefig('graph.png',
                    format='png',
                    bbox_inches='tight')

    def partition_graph(self, num_partitions, num_iterations=1000):
        nodes = list(self.graph.nodes())
        random.shuffle(nodes)
        partitions = [nodes[i::num_partitions] for i in range(num_partitions)]
        progress_bar = tqdm(total=num_iterations, desc="Reading matchups")

        for _ in range(num_iterations):
            improved = False
            for i, j in itertools.combinations(range(num_partitions), 2):
                cut = nx.algorithms.cuts.cut_size(self.graph, partitions[i], partitions[j], weight='weight')

                for u in partitions[i]:
                    for v in partitions[j]:
                        new_partitions = [partitions[p][:] for p in range(num_partitions)]
                        new_partitions[i].remove(u)
                        new_partitions[j].remove(v)
                        new_partitions[i].append(v)
                        new_partitions[j].append(u)

                        if nx.algorithms.cuts.cut_size(self.graph,
                                                       new_partitions[i],
                                                       new_partitions[j],
                                                       weight='weight') < cut:
                            partitions = new_partitions
                            improved = True
                            break
                    if improved:
                        break
                if improved:
                    break
            if not improved:
                break
            progress_bar.update(1)

        for i, partition in enumerate(partitions):
            print(f"Partition {i + 1}: {partition}")

        return partitions
