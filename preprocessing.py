import os
import plotly.graph_objects as go
import psycopg2

from collections import deque
from igraph import Graph, EdgeSeq

class DBMS:
    def __init__(self, pw):
        self.con = self.connect(pw)
        self.cur = self.con.cursor()
    
    def __del__(self):
        self.con.close()

    def connect(self, pw):
        con = psycopg2.connect(database="TPC-H", user="postgres", password=pw, host="127.0.0.1", port="5432")
        print("Database opened successfully")
        return con

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
        self.cur.execute(query)
        return self.cur.fetchall()

    def explainQuery(self, query):
        return self.executeQuery('EXPLAIN (COSTS FALSE, FORMAT JSON) ' + query)[0][0][0]


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
            node = q.popleft()

            g.add_vertices(1)
            print('Adding node {}'.format(node['Node Type']))
            nodeLabels.append(node['Node Type'])

            if 'Parent' in node:
                g.add_edges([(node['Parent'], index)])
                print('Adding edge ({}, {})'.format(node['Parent'], index))

            if 'Plans' in node:
                for plan in node['Plans']:
                    plan['Parent'] = index
                    q.append(plan)
            index += 1
        
        self.createPlot(g, nodeLabels)
    
    def createPlot(self, g, nodeLabels):
        nr_vertices = len(nodeLabels)
        # v_label = list(map(str, range(nr_vertices)))
        print('v_label: {}'.format(nodeLabels))
        # g = Graph.Tree(nr_vertices, 2) # 2 stands for children number
        lay = g.layout('rt')

        position = {k: lay[k] for k in range(nr_vertices)}
        print('position: {}'.format(position))

        Y = [lay[k][1] for k in range(nr_vertices)]
        print('Y: {}'.format(Y))

        M = max(Y)

        es = EdgeSeq(g) # sequence of edges
        E = [e.tuple for e in g.es] # list of edges
        print('E: {}'.format(E))

        L = len(position)
        Xn = [position[k][0] for k in range(L)]
        print('Xn: {}'.format(Xn))

        Yn = [2*M-position[k][1] for k in range(L)]
        print('Yn: {}'.format(Yn))

        Xe = []
        Ye = []
        for edge in E:
            Xe+=[position[edge[0]][0],position[edge[1]][0], None]
            Ye+=[2*M-position[edge[0]][1],2*M-position[edge[1]][1], None]
        print('Xe: {}'.format(Xe))
        print('Ye: {}'.format(Ye))

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
                        marker=dict(symbol='circle-dot',
                                        size=18,
                                        color='#6175c1',    #'#DB4551',
                                        line=dict(color='rgb(50,50,50)', width=1)
                                        ),
                        text=labels,
                        hoverinfo='text',
                        opacity=0.8
                        ))

        def make_annotations(pos, text, font_size=10, font_color='rgb(0,0,0)'):
            L=len(pos)
            if len(text)!=L:
                raise ValueError('The lists pos and text must have the same len')
            annotations = []
            for k in range(L):
                annotations.append(
                    dict(
                        text=labels[k], # or replace labels with a different list for the text within the circle
                        x=pos[k][0] - 0.03, y=2*M-position[k][1],
                        xref='x1', yref='y1',
                        font=dict(color=font_color, size=font_size),
                        showarrow=False)
                )
            return annotations

        axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )

        fig.update_layout(
                    annotations=make_annotations(position, nodeLabels),
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
        
        axis = dict(showline=False, # hide axis line, grid, ticklabels and  title
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    )

        fig.update_layout(
                    xaxis=axis,
                    yaxis=axis,
                    hovermode='closest',
                    plot_bgcolor='rgb(248,248,248)'
                    )
        fig.write_image("images/blank.png")