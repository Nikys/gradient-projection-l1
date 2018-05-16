from math import exp
from path_algorithms import min_paths, mincost3
from transport_graph import TransportGraph, TransportEdgeData
from correspondence_matrix import corresp_matrix

S = [0,1,2,3,4]
D = [16,18,20,22,24]
W = [(i,j) for i in S for j in D]
s = [69,90,10,100,53]
d = [128,59,34,61,40]
s_dict = {S[i]:s[i] for i in range(len(S))}
d_dict = {D[i]:d[i] for i in range(len(D))}

magistrals = [(5,6),(7,8),(9,10),(11,12),(13,14),(16,17),(18,19),(20,21),(22,23),(24,15)]
outs = [(15,0),(14,0),(23,1),(6,1),(21,2),(8,2),(19,3),(10,3),(17,4),(12,4)]
ins = [(0,5),(0,16),(1,24),(1,7),(2,22),(2,9),(3,20),(3,11),(4,18),(4,13)]
adds = [(14,5),(6,7),(8,9),(10,11),(12,13),(15,16),(17,18),(19,20),(21,22),(23,24)]

dict_pairs = TransportGraph()
for i in range(25):
    dict_pairs.add_node()

def add_all_in_dictgraph(list_pairs, lens, dict_pairs, coeff):
    for i,el in enumerate(list_pairs):
        data = TransportEdgeData(lens[i],lens[i] * coeff, 0)
        dict_pairs.add_pair(el[0],el[1],data)

magistrals_lens = [4,10,3,3,5,1,2,6,9,2]
outs_lens = [6,9,3,8,5,1,10,8,5,3]
ins_lens = [3,7,6,2,6,5,6,8,7,4]
adds_lens = [1,6,4,3,9,10,4,6,10,1]

add_all_in_dictgraph(magistrals,magistrals_lens, dict_pairs, 0.011)
add_all_in_dictgraph(ins,ins_lens,dict_pairs,0.025)
add_all_in_dictgraph(outs,outs_lens,dict_pairs,0.025)
add_all_in_dictgraph(adds,adds_lens,dict_pairs,0.033)


mpaths = min_paths(graph=dict_pairs, pairs=W, max_k=10)
mcost = mincost3(graph=dict_pairs, path_dict=mpaths)
func_table = {pair:exp(-0.065*cost) for pair,cost in mcost.items()}
rho_matrix = corresp_matrix(input_traffic=s_dict,output_traffic=d_dict,func_table=func_table)