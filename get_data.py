import urllib2, json
import networkx as nx
from networkx.readwrite import json_graph

def read_gene_from_file(filename):
  f = open(filename)
  lines = f.read().split('\r')

  c1937 = []
  cmix1 = []
  cmix2 = []
  c231 = []
  gene_list = []

  for line in lines:
    tmp = line.split(',')
    c1937.append(tmp[0])
    cmix1.append(tmp[1])
    cmix2.append(tmp[2])
    c231.append(tmp[3])
    gene_list.append(tmp[4])

  return c1937, cmix1, cmix2, c231, gene_list

def get_gene_map(gene_name, i_val):
  url='http://www.pathwaycommons.org/pc2/graph?source=%s&kind=neighborhood&format=BINARY_SIF'%gene_name
  try:
    response = urllib2.urlopen(url)
    html = response.read()
    lines=html.split('\n')
  except:
    print 'Gene %s Not Found' % gene_name
    return 1
 
  if float(i_val) > float(10):
    color = 'red'
  else:
    color = 'blue'
  i = 0
  for line in lines:
    tmp = line.split('\t')
    G.add_edges_from([(tmp[0], tmp[2], {'color':color, 'weight':i_val})])

    i += 1
    if i > 3:
      break

def make_map(gene_list, val, name):
  i = 0
  for gene, i_val in zip(gene_list, val):
    i += 1
    get_gene_map(gene, i_val)
    if i > 2:
      break  
  data = json_graph.node_link_data(G)
  json.dump(data, open('result/%s_graph.json'%name,'w'))

def sample(G):
  ex_name = 'BGN'
  get_gene_map(ex_name, G)

if __name__ == "__main__":

  filename = 'data/hetero_data.csv'
  c1937, cmix1, cmix2, c231, gene_list = read_gene_from_file(filename)

  print gene_list
  
  G = nx.DiGraph()
  make_map(gene_list, c1937, '1937')
  make_map(gene_list, cmix1, 'mix1')
  make_map(gene_list, cmix2, 'mix2')
  make_map(gene_list, c231, '231')

  
