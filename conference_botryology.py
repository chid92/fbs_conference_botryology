from read_cfdb import CFDB
from cfb_teams_graph import CFGraph

if __name__ == '__main__':
    cfdb = CFDB()
    cfdb.write_matchups_csv('matchups.csv')

    print("Generating graph")
    cfgraph = CFGraph('matchups.csv')
    print("Partitioning")
    cfgraph.partition_graph(9)
