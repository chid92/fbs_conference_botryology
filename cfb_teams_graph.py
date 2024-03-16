import pandas as pd
import networkx as nx
import itertools
import random
from tqdm import tqdm


class CFGraph:
    def __init__(self, filename):
        self.graph = nx.DiGraph()
        for index, row in pd.read_csv(filename).iterrows():
            self.graph.add_edge(row['team1'], row['team2'], weight=row['games'])

    def partition_graph(self, num_partitions, num_iterations=1000):
        nodes = list(self.graph.nodes())
        random.shuffle(nodes)
        partitions = [nodes[i::num_partitions] for i in range(num_partitions)]
        progress_bar = tqdm(total=num_iterations, desc="Reading matchups")

        for _ in range(num_iterations):
            improved = False
            for i, j in itertools.combinations(range(num_partitions), 2):
                cut = nx.algorithms.cuts.cut_size(self.graph,
                                                  partitions[i],
                                                  partitions[j],
                                                  weight='weight')
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

        with open(f'partitions{int(len(nodes) / num_partitions)}.txt', 'w') as f:
            for i, partition in enumerate(partitions):
                f.write(f'\nPartition {i + 1}\n')
                for team in partition:
                    f.write(f'{team}\n')

        return partitions
