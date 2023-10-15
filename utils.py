import math
import os
from halfedge_mesh import HalfedgeMesh

def midpoint(a,b,mesh): 
    """
    a,b are the vertices of the edge for which mid point is to be calculated
    mesh is the mesh object obtained using the python package provided

    returns the midpoint in array format with len 3 (x,y,z co-ordinates)
    """
    vertices = mesh.vertices
    edges = mesh.edges

    # calculating mid point for a,b edge
    if (b,a) in edges.keys():
        p1 = vertices[a].get_vertex()
        p2 = vertices[b].get_vertex()
        p3 = edges[(a,b)].prev.vertex.get_vertex()
        p4 = edges[(b,a)].prev.vertex.get_vertex()
        mid_ab = []
        mid_ab.append(0.375*(p1[0]+p2[0]) + 0.125*(p3[0]+p4[0]))
        mid_ab.append(0.375*(p1[1]+p2[1]) + 0.125*(p3[1]+p4[1]))
        mid_ab.append(0.375*(p1[2]+p2[2]) + 0.125*(p3[2]+p4[2]))
    else:
        p1 = vertices[a].get_vertex()
        p2 = vertices[b].get_vertex()
        mid_ab = []
        mid_ab.append(0.5*(p1[0]+p2[0]))
        mid_ab.append(0.5*(p1[1]+p2[1]))
        mid_ab.append(0.5*(p1[2]+p2[2]))

    return mid_ab

def updated_vertex(vertex,mesh):
    """
    vertex is the vertex of mesh for which the updated version is to be calculated
    mesh is the mesh object obtained using the python package provided

    return updated vertex of the provided original vertex
    """
    vertices = mesh.vertices
    edge_list = mesh.edges.keys()
    neighbouring_vertices_indices = []
    for i in range(len(vertices)):
        if (vertex, i) in edge_list or (i,vertex) in edge_list:
            if i not in neighbouring_vertices_indices:
                neighbouring_vertices_indices.append(i)
    n = len(neighbouring_vertices_indices)
    neighbouring_vertices = [vertices[i].get_vertex() for i in neighbouring_vertices_indices]

    ## Below commented code is written to reduce the computation due to the above loop, although it is giving the correct number of vertices and faces
    ## proper output is not obtained in the meshlab viewer.
    # neighbouring_vertices = []
    # half_edge = vertices[vertex].halfedge
    # current_halfedge = half_edge
    # neighbouring_vertices.append(current_halfedge.vertex.get_vertex())
    # while True:
    #     current_halfedge = current_halfedge.next
    #     current_halfedge = current_halfedge.opposite
    #     if current_halfedge is None:
    #         break
    #     else:
    #         if current_halfedge == half_edge:
    #             break
    #         else:
    #             neighbouring_vertices.append(current_halfedge.vertex.get_vertex())
    # # print(neighbouring_vertices)
    # n = len(neighbouring_vertices)

    #Calculating the updated vertex co-ordinates of the old vertex
    theta = math.radians(360 / n)
    cosine_part = 0.25*(math.cos(theta))
    sq_part = ( 0.375 + cosine_part)**2
    alpha = (0.625 - sq_part) / n
    V_i = vertices[vertex].get_vertex()
    # Part-1
    v_part_1 = []
    v_part_1.append((1-(n*alpha))*(V_i[0]))
    v_part_1.append((1-(n*alpha))*(V_i[1]))
    v_part_1.append((1-(n*alpha))*(V_i[2]))

    # # Part-2
    v_part_2 = []
    for i in range(3):
        tmp = 0
        for v in neighbouring_vertices:
            tmp = tmp + v[i]
        v_part_2.append(tmp)
    
    v_part_2 = [num * alpha for num in v_part_2]

    # Final updated vertex
    v_updated = []
    v_updated.append(v_part_1[0] + v_part_2[0])
    v_updated.append(v_part_1[1] + v_part_2[1])
    v_updated.append(v_part_1[2] + v_part_2[2])

    return v_updated

def file_printer(file_path,new_updated_vertices,new_faces,obj_output=True):
    """
    creates the output file in obj or off format 
    file_path = output file path in .obj or .off format
    new_updated_vertices = list of new(midpoints) & updated vertices
    new_faces = list of new face (list of list of 3 vertex indices corresponding to the new faces)
    obj_output = Boolean to decide the format of output (.obj by default)

    """

    if obj_output:

        if os.path.exists(file_path):
            print("The file '{}' already exists.".format(file_path))
        else:
            try:
                with open(file_path, 'w') as file:
                    print("File '{}' created successfully.".format(file_path))
            except IOError as e:
                print("Error: Unable to create the file '{}'.".format(str(e)))

        with open(file_path, 'w') as file:
            file.write('')

        for v in new_updated_vertices:
            with open(file_path, 'a') as file:
                file.write('v {} {} {}\n'.format(v[0]+1, v[1]+1, v[2]+1))

        for f in new_faces:
            with open(file_path, 'a') as file:
                file.write('f {}/{} {}/{} {}/{}\n'.format(f[0]+1,f[0]+1,f[1]+1,f[1]+1,f[2]+1,f[2]+1))
    else:

        if os.path.exists(file_path):
            print("The file '{}' already exists.".format(file_path))
        else:
            try:
                with open(file_path, 'w') as file:
                    print("File '{}' created successfully.".format(file_path))
            except IOError as e:
                print("Error: Unable to create the file '{}'.".format(str(e)))

        with open(file_path, 'w') as file:
            file.write('')

        with open(file_path, 'a') as file:
            file.write('OFF\n')
            file.write('{} {} 0\n'.format(len(new_updated_vertices), len(new_faces)))

        for v in new_updated_vertices:
            with open(file_path, 'a') as file:
                file.write('{} {} {}\n'.format(v[0], v[1], v[2]))
        
        for f in new_faces:
            with open(file_path, 'a') as file:
                file.write('3 {} {} {}\n'.format(f[0],f[1],f[2]))
