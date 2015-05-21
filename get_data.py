import urllib2, json
import networkx as nx
from networkx.readwrite import json_graph

def read_gene_from_file(filename):
  #depend on input data 
  return 1

def get_gene_map(gene_name, G):
  url='http://www.pathwaycommons.org/pc2/graph?source=%s&kind=neighborhood&format=BINARY_SIF'%gene_name
  response = urllib2.urlopen(url)
  html = response.read()
  lines=html.split('\n')
  for line in lines:
    tmp = line.split('\t')
    G.add_nodes_from([tmp[0], tmp[1]])

  data = json_graph.node_link_data(G)
  json.dump(data, open('output_graph.json','w'))

  return Graph

def make_map(gene_list):
  return 1

if __name__ == "__main__":
  """
  filename = 'data/'
  gene_list = read_gene_from_file(filename)

  Graph = make_map(gene_list)
  """

  G = nx.DiGraph()
  ex_name = 'BGN'  
  get_gene_map(ex_name, G)


