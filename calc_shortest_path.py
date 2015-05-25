import urllib2, json, itertools
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

def read_gene_list(filename):
  f = open(filename)
  lines = f.read().split('\r')
  gene_list = []
  for line in lines:
    gene_list.append(line.split(',')[4])
  return gene_list


def get_gene_map(gene_name, i_val, G):
  print gene_name
  if float(i_val) < 1:
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


def make_map(gene_list, val, name, G):
  for gene, i_val in zip(gene_list, val):
    get_gene_map(gene, i_val, G)

def genes_combinations(gene_list):
  return list(itertools.combinations(gene_list, 2))

def sample(G):
  ex_name = 'BGN'
  get_gene_map(ex_name, G)

def write_diff(f, gene):
    f.write(gene[0])
    f.write('\t')
    f.write(gene[1])
    f.write('\t')

def write_paths(f, Ga_paths, Gb_paths):
  for path in Ga_paths:
    f.write(path)
    f.write('\t')
  f.write('---')
  f.write('\t')
  for path in Gb_paths:
    f.write(path)
    f.write('\t')

def calc_shortest_path(G1, G2, G3, G4, combs, threshold):
  f = open('result/shortest_path', 'w')
  f_bl = open('result/blocked_path', 'w')
  for comb in combs:
    num_path = []
    try:
      num_path.append(len(nx.shortest_path(G1, comb[0], comb[1])))
      num_path.append(len(nx.shortest_path(G2, comb[0], comb[1])))

      G3_paths = nx.shortest_path(G3, comb[0], comb[1])
      G4_paths = nx.shortest_path(G4, comb[0], comb[1])

      num_path.append(len(G3_paths))
      num_path.append(len(G4_paths))
      if num_path[0] != num_path[1] or num_path[1] != num_path[3]:
        print num_path
        f.write('Alternative Path')
        f.write('\t')
        write_diff(f, comb)
        f.write('---')
        f.write('\t')
        write_paths(f, G3_paths, G4_paths)
        f.write('\n')


    except:
      print 'Not found between %s and %s'% (comb[0], comb[1])
      if len(num_path) >= 1:
        f_bl.write('Blocked Path')
        f_bl.write('\t')
        write_diff(f_bl, comb)
        f_bl.write('\n')

  f.close()
  f_bl.close()
  return 1

if __name__ == "__main__":
  
  filename = 'data/short_hetero.csv' 

  G_1937 = nx.read_dot('result/threshold_3_maps/31937_graph.dot')
  G_mix1 = nx.read_dot('result/threshold_3_maps//3mix1_graph.dot')
  G_mix2 = nx.read_dot('result/threshold_3_maps/3mix2_graph.dot')
  G_231 = nx.read_dot('result/threshold_3_maps/3231_graph.dot')
   
  gene_list = read_gene_list(filename)
  combs = genes_combinations(gene_list)

  threshold = float(5.0)
  calc_shortest_path(G_1937, G_mix1, G_mix2, G_231, combs, threshold)

