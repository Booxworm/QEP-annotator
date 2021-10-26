import psycopg2

class DBMS:
    def __init__(self):
        self.con = self.connect()
        self.cur = self.con.cursor()
    
    def __del__(self):
        self.con.close()

    def connect(self):
        con = psycopg2.connect(database="TPC-H", user="postgres", password="root", host="127.0.0.1", port="5432")
        print("Database opened successfully")
        return con

    def getQuery(self):
        print('Enter your query: ')
        query = []
        query.append(input())
        while query[-1][-1] != ';':
            query.append(input())

        joined = ' '.join(query)
        return joined

    def executeQuery(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def explainQuery(self, query):
        return self.executeQuery('EXPLAIN ' + query)