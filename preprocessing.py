import os
import plotly.graph_objects as go
import psycopg2

from collections import deque
from igraph import Graph

class DBMS:
    def __del__(self):
        if self.con:
            self.con.close()

    def connect(self, database='TPC-H', user='postgres', password='Dolphin123:', host='127.0.0.1', port='5432'):
        try:
            self.con = psycopg2.connect(database=database, user=user, password=password, host=host, port=port)
            self.cur = self.con.cursor()
            print('Database opened successfully')
            return True
        except:
            self.con = None
            print('Failed to connect to database')
            return False

    def getQuery(self):
        query = []
        print('Enter your query: ')
        
        # Use default query if left blank
        tmp = input()
        if tmp == '':
            return 'SELECT * FROM customer, orders WHERE c_custkey = o_custkey;'
        
        query.append(tmp)
        while tmp[-1] != ';':
            tmp = input()
            query.append(tmp)

        joined = ' '.join(query)
        return joined

    def executeQuery(self, query):
        print(query)
        try:
            self.cur.execute(query)
            self.con.commit()
        except:
            self.con.rollback()
        return self.cur.fetchall()

    def explainQuery(self, query):
        return self.executeQuery('EXPLAIN (COSTS FALSE, FORMAT JSON) ' + query)[0][0][0]

    def explainQueryString(self, query):
        return self.executeQuery('EXPLAIN (COSTS FALSE)' + query)

class QepGraph:
    def __init__(self):
        if not os.path.exists("images"):
            os.mkdir("images")
        
        if not os.path.exists("images/blank.png"):
            self.createBlank()

    def createQepGraph(self, qep):
        g = Graph()

        q = deque()
        q.append(qep['Plan'])

        index = 0
        nodeLabels = []

        while len(q) > 0:
            # Dequeue node from queue
            node = q.popleft()

            # Add one vertice to graph, and record its label
            g.add_vertices(1)
            nodeLabels.append(node['Node Type'])

            # Add edge to graph if parent exists
            if 'Parent' in node:
                g.add_edges([(node['Parent'], index)])

            # Check for children of node, and enqueue
            if 'Plans' in node:
                for plan in node['Plans']:
                    plan['Parent'] = index
                    q.append(plan)
            index += 1
        
        # Create plot with the finished graph
        self.createPlot(g, nodeLabels)
    
    def createPlot(self, g, nodeLabels):
        numNodes = len(nodeLabels)
        lay = g.layout('rt')

        position = {k: lay[k] for k in range(numNodes)}
        Y = [lay[k][1] for k in range(numNodes)]
        M = max(Y)

        E = [e.tuple for e in g.es] # list of edges
        L = len(position)

        # X and Y coordinates of nodes
        Xn = [position[k][0] for k in range(L)]
        Yn = [2*M-position[k][1] for k in range(L)]

        # X and Y coordinates of edges
        Xe = []
        Ye = []
        for edge in E:
            Xe+=[position[edge[0]][0],position[edge[1]][0], None]
            Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]

        labels = nodeLabels

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Xe,
                        y=Ye,
                        mode='lines',
                        line=dict(color='rgb(210,210,210)', width=1),
                        hoverinfo='none'
                        ))
        fig.add_trace(go.Scatter(x=Xn,
                        y=Yn,
                        mode='markers',
                        name='bla',
                        marker=dict(symbol='square',
                                        size=50,
                                        color='#6175c1',    #'#DB4551',
                                        line=dict(color='rgb(50,50,50)', width=1)
                                        ),
                        text=labels,
                        hoverinfo='text',
                        opacity=0.8
                        ))

        def makeAnnotations(pos, text, font_size=10, font_color='rgb(0,0,0)'):
            L=len(pos)
            if len(text)!=L:
                raise ValueError('The lists pos and text must have the same len')
            annotations = []
            for k in range(L):
                annotations.append(
                    dict(
                        text=labels[k], # or replace labels with a different list for the text within the circle
                        x=pos[k][0], y=2*M-position[k][1],
                        xref='x1', yref='y1',
                        font=dict(color=font_color, size=font_size),
                        showarrow=False)
                )
            return annotations

        # Hide axis line, grid, ticklabels and title
        axis = dict(showline=False,
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )

        fig.update_layout(
                    annotations=makeAnnotations(position, nodeLabels),
                    font_size=12,
                    showlegend=False,
                    xaxis=axis,
                    yaxis=axis,
                    hovermode='closest',
                    plot_bgcolor='rgb(248,248,248)'
                    )
        fig.write_image("images/qep.png")

    def createBlank(self):
        fig = go.Figure()

        # Hide axis line, grid, ticklabels and title
        axis = dict(showline=False,
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )

        fig.update_layout(
                    xaxis=axis,
                    yaxis=axis,
                    plot_bgcolor='rgb(248,248,248)'
                    )
        fig.write_image("images/blank.png")