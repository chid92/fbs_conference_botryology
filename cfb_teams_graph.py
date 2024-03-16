import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class CFGraph:
    def __init__(self, filename):
        self.graph = nx.DiGraph()
        for index, row in pd.read_csv(filename).iterrows():
            if row['games'] != 0:
                self.graph.add_edge(row['team1'], row['team2'], weight=(1 / row['games']))

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
