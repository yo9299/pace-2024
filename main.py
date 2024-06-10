#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  3 17:18:13 2024

@author: vardevol
"""
import sys 
sys.setrecursionlimit(100000)
import signal
from collections import defaultdict

class Killer:
  exit_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit)
    signal.signal(signal.SIGTERM, self.exit)

  def exit(self,signum, frame):
    self.exit_now = True

#create graph directly when i iterate over edges
def create_graph(filename):
    #input_graph = open(filename, 'r')
    #lines= input_graph.readlines()
    lines = filename.readlines()
    #input_graph.close()
    lines = [line.rstrip() for line in lines] 
    i= 0#
    data=lines[i].split(" ")
    if data[0] == 'c':
        i= 1
        data= lines[i].split("")
    (n_a, n_b, n_edges) = (int(data[2]), int(data[3]), int(data[4]))
    edges =lines[(i+1):]
    map_edges = {} #key: [] for key in list(range(n_a+1, n_a+n_b +1))}
    for i in range(len(edges)):
        e = edges[i].split(" ")
        start = int(e[0])
        end = int(e[1])
        if end in map_edges:
            map_edges[end].append( start)
        else:
            map_edges[end] = [start]
    isolated =[] 
    for j in range(n_a+1, n_a+n_b +1):
        if j not in map_edges:
            isolated.append(j)
    graph = Bipartite_graph(map_edges, n_a, n_b, n_edges, isolated)
    return graph

class Bipartite_graph:
    def __init__(self, edges, n_a, n_b, n_edges, isolated):
        self.edges=edges
        self.n_edges = n_edges
        self.n_a = n_a
        self.n_b = n_b
        self.orderB = list(range(self.n_a +1, self.n_b +self.n_a+1))
        self.isolated = isolated
        self.vertices = list(edges.keys() )
    
    def group_by_twins(self):
        twin_dict = defaultdict(list)
        for key in self.edges:
            twin_dict[tuple(self.edges[key])].append(key)
        return list(twin_dict.values())
    
def compute_total_crossings(graph, cursol):
    value = 0 
    for i in range(len(cursol)):
        for j in range(i+1, len(cursol)):
            value += crossing_nb(graph, cursol[i], cursol[j])
    return value

def compare_total_crossings(graph, sol1, sol2):
    killer = Killer() 
    c1 = 0
    c2 = 0 
    for i in range(len(sol1)):
        for j in range(i+1, len(sol1)):
            c1 += crossing_nb(graph, sol1[i], sol1[j])
            #check if in the same order in sol2 and do not recompute
            c2 += crossing_nb(graph, sol2[i], sol2[j])
            if killer.exit_now:
                break
        if killer.exit_now:
            break 
    return c1, c2 
            
def compare_total_crossings2(graph, sol1, sol2):
    #killer= Killer()
    c1 = 0
    c2 = 0 
    for u in graph.vertices: #range(len(graph.vertices)): #range(graph.n_a +1, graph.n_a + graph.n_b + 1):
        for v in graph.vertices[graph.vertices.index(u)+1:] : 
            if sol1.index(u) < sol1.index(v) and sol2.index(u) > sol2.index(v) :
                c1  += crossing_nb(graph, u, v)
                c2 += crossing_nb(graph, v, u)
            elif sol1.index(u) > sol1.index(v) and sol2.index(u) < sol2.index(v) :
                c2 += crossing_nb(graph, u, v)
                c1 += crossing_nb(graph, v, u)
            if killer.exit_now:
                break 
    return c1, c2 

def compare_total_crossings3(graph, sol1, sol2, sol3):
    #killer= Killer()
    c1 = 0
    c2 = 0 
    c3=0 
    for u in graph.vertices: #range(len(graph.vertices)): #range(graph.n_a +1, graph.n_a + graph.n_b + 1):
        for v in graph.vertices[graph.vertices.index(u)+1:] : #  range( u+1, len(graph.vertices)) : #u+1, graph.n_a + graph.n_b +1):
            if sol1.index(u) < sol1.index(v) and sol2.index(u) > sol2.index(v) and sol3.index(u) > sol3.index(v):
                c1  += crossing_nb(graph, u, v)
                add = crossing_nb(graph, v, u)
                c3 += add
                c2 += add 
            elif sol1.index(u) < sol1.index(v) and sol2.index(u) > sol2.index(v) and sol3.index(u) < sol3.index(v) :
                add = crossing_nb(graph, u, v)
                c2 += crossing_nb(graph, v, u)
                c1 += add
                c3 += add 
            elif sol1.index(u) < sol1.index(v) and sol2.index(u) < sol2.index(v) and sol3.index(u) > sol3.index(v) :
                add = crossing_nb(graph, u, v)
                c3 += crossing_nb(graph, v, u)
                c1 += add
                c2 += add 
            elif sol1.index(u) > sol1.index(v) and sol2.index(u) < sol2.index(v) and sol3.index(u) < sol3.index(v) :
                add = crossing_nb(graph, u, v)
                c1 += crossing_nb(graph, v, u)
                c2 += add
                c3 += add 
            elif sol1.index(u) > sol1.index(v) and sol2.index(u) < sol2.index(v) and sol3.index(u) > sol3.index(v) :
                add = crossing_nb(graph, v, u)
                c2 += crossing_nb(graph, u, v)
                c1 += add
                c3 += add 
            elif sol1.index(u) > sol1.index(v) and sol2.index(u) > sol2.index(v) and sol3.index(u) < sol3.index(v) :
                add = crossing_nb(graph, v, u)
                c3 += crossing_nb(graph, u, v)
                c1 += add
                c2 += add 
            if killer.exit_now:
                break 
    return c1, c2 ,c3

#this function counts the pairs x,y with x in graph.edges[u], y in graph.edges[v] with x > y 
def crossing_nb(graph, vertex1, vertex2):
    cross= [(x,y) for x in graph.edges[vertex1] for y in graph.edges[vertex2] if x > y ]
    return len(cross) 

def upper_bound_sol(graph):
    scores = dict((key, [0,0,0]) for key in (graph.vertices))
    for eq in graph.group_by_twins(): # in graph.vertices:
        v = eq[0]
        mean = 0
        median = [] 
        for n in graph.edges[v]: # 
            mean += n
            median.append(n)
        for u in eq : 
            if mean== 0:
                scores[u][0] = 0
                scores[u][1] = 0
            else :
                scores[u][0] =( mean/len(graph.edges[v]))
                if len(median) % 2 == 1:
                    scores[u][1] = median[len(median) // 2]
                else :
                    scores[u][1] = (median[len(median)// 2] + median[(len(median) +1)//2])/2
            if killer.exit_now:
                break 
        #scores[v][2] = (scores[v][1] + scores[v][0]) /2
            
    sortedsol = sorted(scores, key=lambda x : scores[x][0] ) #skey=scores[0].get)
    sortedsol1 = sorted(scores, key=lambda x : scores[x][1])
    #sortedsol2 = sorted(scores, key=lambda x : scores[x][2])
    #print(sortedsol)
    #print([input_graph.orderB.index(v) for v in sortedsol] )
    #the return type is wrong
    return sortedsol, sortedsol1 #, sortedsol2 


def local_move(graph, sol):
    #killer = Killer()
    for iteration in range(len(sol)):
        for i in range(len(sol)-1):
            j= i +1 
            if crossing_nb(graph, sol[j], sol[i]) < crossing_nb(graph,sol[i], sol[j]):
                new_i = sol[j]
                new_j = sol[i]
                sol[i] = new_i 
                sol[j] = new_j 
                if killer.exit_now:
                    break 
    return sol 

def exchange_distance2(graph, sol):
    for iteration in range(len(sol)):
        for i in range(len(sol)-2):
            j = i +2
            if crossing_nb(graph, sol[j], sol[i]) + crossing_nb(graph, sol[j], sol[i+1])  < crossing_nb(graph,sol[i], sol[j]) + crossing_nb(graph, sol[i+1], sol[j]) :
                new_i = sol[j]
                new_j = sol[i]
                sol[i] = new_i 
                sol[j] = new_j 
                if killer.exit_now:
                    break 
    return sol 
            
def exchange_distancek(graph, sol, k):
    
    for iteration in range(len(sol)):
        for i in range(len(sol)-k):
            j = i +k
            olds = 0
            news = 0 
            for l in range(i, i +k):
                news += crossing_nb(graph, sol[j], sol[l])
                olds += crossing_nb(graph,sol[l], sol[j])
                if news < olds :
                    
                    new_i = sol[j]
                    new_j = sol[i]
                    sol[i] = new_i 
                    sol[j] = new_j 
                if killer.exit_now:
                    break 
            
    return sol 

killer= Killer()

def solve(g):
    #killer = Killer()
    s_mean, s_med = upper_bound_sol(g)
    #if killer.exit_now:
    #    sol = s_med
    #else: 
    #s_med =  upper_bound_med(g)
    #c_mean = compute_total_crossings(g, s_mean)
    if killer.exit_now:
        return s_mean + g.isolated
    c_mean, c_med = compare_total_crossings2(g, s_mean, s_med)
    x= zip([s_mean, s_med], [c_mean, c_med])
    sol = min(x, key= lambda x: x[1])[0]
    if killer.exit_now:
        return sol + g.isolated
    sol1 = exchange_distancek(g, sol, 3) #local_move(g, sol)
    
    if killer.exit_now:
        return sol1 + g.isolated
    
    
    final_sol = exchange_distance2(g, sol1)
    if killer.exit_now:
        return final_sol + g.isolated
    fin = local_move(g, final_sol)
    
    #sol2 = exchange_distancek(graph, sol, 3)

    
    #if killer.exit_now:
     #   sol = s_med
    #else:
    #sol = s_mean
    #sol = min(s_mean, s_med, key=lambda x : compute_total_crossings(g, x))
    return fin + g.isolated

def write_solution(list_B):
    '''sol = open( "sol.sol", "a")
    towrite = []
    for i in range(len(list_B)):
        towrite.append(str(list_B[i]) + "\n")

    sol.writelines(towrite)
    sol.close()'''
    for i in range(len(list_B)):
       sys.stdout.write(str(list_B[i]) + "\n")
   
        
filename = sys.stdin  
#filename = sys.argv[1]


def main():
    graph = create_graph(filename)
    #g = Bipartite_graph(graph, ordera, orderb)
             
    sol = solve(graph)
            #print(time.time()-tps)
    write_solution(sol)



if __name__ == "__main__":
    #print("entered main")
    main()
