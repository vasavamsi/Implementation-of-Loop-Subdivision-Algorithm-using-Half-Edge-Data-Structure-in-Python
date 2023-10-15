import os
import math
from halfedge_mesh import HalfedgeMesh
from utils import *

mesh = HalfedgeMesh("./results/teapot_out_1 iteration.off")

obj_output = True # Check true if output needed is to be in obj format
output_file_path = './results/teapot_out_2_iteration.obj' # Provide the output file path (choose the proper format between .obj and .off)

facets = mesh.facets # Getting list of facets

faces_dict = {}
new_updated_vertices = []
used_vertices = {}
ind = 0
face = 0
for facet in facets:
    faces_dict[face] = []
    a = facet.a
    b = facet.b
    c = facet.c

    # Finding midpoints
    mid_ab = midpoint(a,b,mesh)
    if mid_ab not in new_updated_vertices:
        new_updated_vertices.append(mid_ab)
        faces_dict[face].append(ind)
        ind = ind + 1
    else:
        already_index = new_updated_vertices.index(mid_ab)
        faces_dict[face].append(already_index)

    mid_bc = midpoint(b,c,mesh)
    if mid_bc not in new_updated_vertices:
        new_updated_vertices.append(mid_bc)
        faces_dict[face].append(ind)
        ind = ind + 1
    else:
        already_index = new_updated_vertices.index(mid_bc)
        faces_dict[face].append(already_index)

    mid_ca = midpoint(c,a,mesh)
    if mid_ca not in new_updated_vertices:
        new_updated_vertices.append(mid_ca)
        faces_dict[face].append(ind)
        ind = ind + 1
    else:
        already_index = new_updated_vertices.index(mid_ca)
        faces_dict[face].append(already_index)

    # Finding updated vertices
    for vertex in [facet.a, facet.b, facet.c]:
        if vertex in used_vertices.keys():
            faces_dict[face].append(new_updated_vertices.index(used_vertices[vertex]))
            continue
        else:
            v_updated = updated_vertex(vertex,mesh)
            new_updated_vertices.append(v_updated)
            faces_dict[face].append(ind)
            used_vertices[vertex] = v_updated
            ind = ind+1
    face = face + 1 

# creating the list of new facesSS
new_faces = []
for face in faces_dict.keys():
    
    new_faces.append([faces_dict[face][3], faces_dict[face][0], faces_dict[face][2]])
    new_faces.append([faces_dict[face][0], faces_dict[face][4], faces_dict[face][1]])
    new_faces.append([faces_dict[face][0], faces_dict[face][1], faces_dict[face][2]])
    new_faces.append([faces_dict[face][2], faces_dict[face][1], faces_dict[face][5]])

file_printer(output_file_path,new_updated_vertices,new_faces,obj_output) # creates the output file in needed format
