from copy import deepcopy
from random import randint

def generate_false(path, dists, qtd, distm):
    for i in range(qtd):
        idx_ = randint(1, len(path)-2)
        old_p = path[idx_]
        new_p = path[0]
        while new_p in path:
            new_p = randint(1, len(distm[0])-1)
        
        path[idx_] = new_p
        dists[idx_] = distm[path[idx_-1]][new_p][1]
        dists[idx_+1] = distm[new_p][path[idx_+1]][1]

    return path, dists

def build_path(ini, distm, size):
    path = [ini]
    dists = [0]
    idx_ = ini
    for i in range(size):
        shortest = sorted(distm[idx_], key=lambda x: x[1])
        k = 1
        new_p = shortest[k][0]
        new_d = shortest[k][1]
        while(new_p in path):
            k += 1
            new_p = shortest[k][0]
            new_d = shortest[k][1]
        path.append(new_p)
        dists.append(new_d)

    return path, dists

map_ = {}
with open('vertices_niteroi.lhp', 'r') as f:
    f.readline()
    f.readline()
    f.readline()
    for l in f.readlines():
        l = l.split(' ')
        map_[int(l[0])] = (float(l[-2]), float(l[-1]))

distm = []
with open('d_space_niteroi.lhp', 'r') as f:
    f.readline()
    for l in f.readlines():
        distm.append([(i, int(x)) for i, x in enumerate(l.split(' '))])

paths = []
dists = []
tf = []
for i, l in enumerate(distm):
    path, dist = build_path(i, distm, 14)
    paths.append(deepcopy(path))
    dists.append(deepcopy(dist))
    tf.append(True)

    path, dist = generate_false(path, dist, 5, distm)
    paths.append(deepcopy(path))
    dists.append(deepcopy(dist))
    tf.append(False)

with open('walks.txt', 'w') as f:
    for i, e in enumerate(tf):
        for p in paths[i]:
            f.write(str(p) + '\t')
        for p in paths[i]:
            f.write(str(map_[p][0]) + '\t' + str(map_[p][1]) + '\t')
        for d in dists[i]:
            f.write(str(d) + '\t')
        f.write(str(e) + '\n')
