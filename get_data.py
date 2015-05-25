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

def get_gene_map(gene_name, i_val, G, threshold):
  print gene_name
  if float(i_val) < float(threshold):
    print 'Too weak edge' 
    return 1

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
  elif float(i_val) > float(4):
    color = 'blue'
  else:
    color = 'green'

  for line in lines:
    if int(line.find(gene_name)) == -1:
      continue
    tmp = line.split('\t')
    G.add_edges_from([(tmp[0], tmp[2], {'color':color, 'weight':i_val})])


def make_map(gene_list, val, name, G, threshold):
  for gene, i_val in zip(gene_list, val):
    get_gene_map(gene, i_val, G, threshold)

  #data = json_graph.node_link_data(G)
  #json.dump(data, open('result/%s_graph.json'%name,'w'))

  nx.write_dot(G,'result/full/%s_graph.dot'% (str(threshold) + name))

def sample(G):
  ex_name = 'BGN'
  get_gene_map(ex_name, G)

if __name__ == "__main__":

  filename = 'data/hetero_data.csv'
  threshold = 3

  c1937, cmix1, cmix2, c231, gene_list = read_gene_from_file(filename)

  print gene_list
  
  G_1937 = nx.DiGraph()
  G_mix1 = nx.DiGraph()
  G_mix2 = nx.DiGraph()
  G_231 = nx.DiGraph()

  #make_map(gene_list, c1937, '1937', G_1937, threshold)
  #make_map(gene_list, cmix1, 'mix1', G_mix1, threshold)
  #make_map(gene_list, cmix2, 'mix2', G_mix2, threshold)
  make_map(gene_list, c231, '231', G_231, threshold)

  print 'Finish' 
