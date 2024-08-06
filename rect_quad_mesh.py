
import argparse

import numpy as np

def gmsh_header():
    header = '''
$MeshFormat
2.2 0 8
$EndMeshFormat
$PhysicalNames
5
1 2 "periodic_0_l"
1 3 "periodic_1_l"
1 4 "periodic_0_r"
1 5 "periodic_1_r"
2 1 "fluid"
$EndPhysicalNames
'''
    return header

def gmsh_nodes(X):
    data = f'$Nodes\n{len(X)}\n'
    for i,x in enumerate(X):
        data += f'{i+1} ' + ' '.join(str(z) for z in x) + '\n'
    data += '$EndNodes\n'
    return data

def gmsh_boundaries(nx, ny, nele = 0):
    ele = ''
    # west
    for i in range(ny-1):
        nele += 1
        # elm-number elm-type reg-phys reg-elem number-of-nodes node-number-list
        n1 = i*nx + 1
        n2 = (i + 1)*nx + 1
        ele += f'{nele} 1 2 2 1 {n1} {n2}\n'

    # east
    for i in range(ny-1):
        nele += 1
        # elm-number elm-type reg-phys reg-elem number-of-nodes node-number-list
        n1 = (i + 1)*nx
        n2 = (i + 2)*nx
        ele += f'{nele} 1 2 4 3 {n1} {n2}\n'

    # south
    for i in range(nx-1):
        nele += 1
        # elm-number elm-type reg-phys reg-elem number-of-nodes node-number-list
        n1 = i + 1
        n2 = i + 2
        ele += f'{nele} 1 2 3 2 {n1} {n2}\n'

    # north
    for i in range(nx-1):
        nele += 1
        # elm-number elm-type reg-phys reg-elem number-of-nodes node-number-list
        n1 = (ny - 1)*nx + i + 1
        n2 = (ny - 1)*nx + i + 2
        ele += f'{nele} 1 2 5 4 {n1} {n2}\n'

    return nele, ele

def gmsh_elements(nx, ny):
    nele, ele = gmsh_boundaries(nx, ny)

    # elm-number elm-type number-of-tags < tag > … node-number-list
    for j in range(ny - 1):
        for i in range(nx - 1):
            nele += 1
            n1 = j*nx + i + 1
            n2 = j*nx + i + 2
            n3 = (j + 1)*nx + i + 2
            n4 = (j + 1)*nx + i + 1
            ele += f'{nele} 3 2 1 4 {n1} {n2} {n3} {n4}\n'

    return f'$Elements\n{nele}\n' + ele + '$EndElements\n'

def make_mesh(lx, ly, x0, y0, nx, ny):
    Rx = np.linspace(x0, x0 + lx, nx)
    Ry= np.linspace(y0, y0 + ly, ny)
    X = np.zeros((nx*ny, 3))

    for j,ry in enumerate(Ry):
        for i,rx in enumerate(Rx):
            X[j*nx+i,0] = rx
            X[j*nx+i,1] = ry

    header = gmsh_header()
    nodes = gmsh_nodes(X)
    ele = gmsh_elements(nx, ny)

    return header + nodes + ele


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make quad based gmsh of square')
    parser.add_argument('-nx', '--nx', dest='nx', type=int)
    parser.add_argument('-ny', '--ny', dest='ny', type=int)
    parser.add_argument('-lx', default=1, dest='lx', type=float)
    parser.add_argument('-ly', default=1, dest='ly', type=float)
    parser.add_argument('-x0', '--x0', default=0, dest='x0', type=float)
    parser.add_argument('-y0', '--y0', default=0, dest='y0', type=float)

    args = parser.parse_args()

    nx = args.nx
    ny = args.ny
    lx = args.lx
    ly = args.ly
    x0 = args.x0
    y0 = args.y0
    msh = make_mesh(lx, ly, x0, y0, nx + 1, ny + 1)

    f = open(f'rect_{nx}x{ny}.msh', 'w')
    f.write(msh)
