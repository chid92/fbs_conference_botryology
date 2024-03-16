from read_cfdb import CFDB
from cfb_teams_graph import CFGraph
import math

if __name__ == '__main__':
    cfdb = CFDB()
    cfdb.write_matchups_csv('matchups.csv')
    cfgraph = CFGraph('matchups.csv')

    number = len(cfdb.teams)
    divisors = []
    for divisor in [i for i in range(3, int(math.sqrt(number)) + 1) if number % i == 0]:
        print(f'Partitioning {divisor}')
        cfgraph.partition_graph(divisor)
