from math import ceil, log2, sqrt
from random import randint, sample
from itertools import combinations


MIN_NODES = 1
MAX_NODES = 16
MIN_GROUPS = 1
MIN_VIRTS = 2
RUNS = 5000


with open('./run-base.clt', 'r') as run_base:
  model = run_base.read()


def list_of(l):
  return f'[{"; ".join(l)}]'


for run_id in range(RUNS):
  n_nodes = randint(MIN_NODES, MAX_NODES)
  max_groups = ceil(n_nodes/2)
  max_virts = ceil(2**(4+0.6*log2(n_nodes)))
  nodes = [f'node{i}' for i in range(n_nodes)]
  groups = {f'group{i}': ([],[]) for i in range(randint(MIN_GROUPS, max_groups))}
  virts = [f'virt{i}' for i in range(randint(MIN_VIRTS, max_virts))]
  pairs = sample(list(combinations(virts, 2)), randint(1, len(virts) - 1))
  with open(f'runs/run-{n_nodes}-{len(groups)}-{len(virts)}-{len(pairs)}-{run_id}.cl1', 'w') as run:
    run.write(model)
    for node in nodes:
      for group in sample(list(groups), randint(1, ceil(sqrt(len(groups))))):
        groups[group][0].append(node)
      run.write(f'let {node} = Node();\n')
    distinct = combinations(nodes, 2)
    for (node_1, node_2) in distinct:
      run.write(f'assert ({node_1} != {node_2});\n')
    for virt in virts:
      groups['group{}'.format(randint(0, len(groups)-1))][1].append(virt)
      run.write(f'let {virt} = Virt();\n')
    for group in groups:
      run.write(f'let {group} = Group {{ nodes <- ({list_of(groups[group][0])}:Node*); virts <- ({list_of(groups[group][1])}:Virt*); is_restricted <- true; }};\n')
    run.write(f'let cluster = Cluster {{ nodes <- {list_of(nodes)}; groups <- {list_of(groups)}; }};\n')
    for (virt_1, virt_2) in pairs:
      run.write(f'assert({virt_1} <<{["can have affinity", "can have antiaffinity", "has affinity", "has antiaffinity"][randint(0,3)]} with>> {virt_2});\n')
