from read_cfdb import CFDB

if __name__ == '__main__':
    cfdb = CFDB()
    cfdb.write_matchups_csv('matchups.csv')
