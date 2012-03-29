__author__ = 'benjamin.loesch'

import collada
import sys
import traceback


print 'Attempting to load file %s' % sys.argv[1]

vertices = []
index = []

def write_to_json(dict,file):

    file.write('\t[[{\n')
    for key in dict:
        if str(key)=='Color':
            continue
        value = dict[key]
        if(str(key)=='color'):
            continue
        if(isinstance(value,str)):
            file.write('\"'+str(key)+'\" : \"'+str(dict[key])+'\",\n')
        else:
            file.write('\"'+str(key)+'\" : '+str(dict[key])+',\n')
    file.seek(-3,1) #set cursor pos back to remove last ','
    file.write('\n\t}]]\n')
    file.close()


if __name__ == '__main__':

    try:
        col = collada.Collada(sys.argv[1],\
            ignore=[collada.DaeUnsupportedError, collada.DaeBrokenRefError])

        file = open('../output/test.json','w')

        for geom in col.scene.objects('geometry'):
            id = 1
            jsonobject = {}
            jsonobject['Center'] = [8.365824,47.022749,400]
            jsonobject['IndexSemantic'] = 'TRIANGLES'
            jsonobject['VertexSemantic'] = 'p'
            jsonobject['Vertices']= []
            jsonobject['Indices'] = []

            for prim in geom.primitives():

                #determine the VertexSemantic --------------------------------------------------------------------------

                mat = prim.material
                value = getattr(mat.effect, 'diffuse')
                if (isinstance(value, tuple)):
                    jsonobject['VertexSemantic'] = 'pc'
                    jsonobject['Color'] = value


                if (isinstance(value, collada.material.Map)):
                    colladaimage = value.sampler.surface.image
                    jsonobject["DiffuseMap"] = colladaimage.path
                    jsonobject['VertexSemantic'] = 'pt'

                #-------------------------------------------------------------------------------------------------------


                trinr = 0
                idx = 0;
                while trinr < prim.ntriangles:

                    i=0
                    while i<3:
                        x1 = prim.vertex[prim.vertex_index[trinr][i]][0]
                        y1 = prim.vertex[prim.vertex_index[trinr][i]][1]
                        z1 = prim.vertex[prim.vertex_index[trinr][i]][2]

                        jsonobject['Vertices'].append(x1)
                        jsonobject['Vertices'].append(y1)
                        jsonobject['Vertices'].append(z1)

                        if (jsonobject['VertexSemantic'].find('n') != -1):
                            nx1 = prim.normal[prim.normal_index[trinr][i]][0]
                            ny1 = prim.normal[prim.normal_index[trinr][i]][1]
                            nz1 = prim.normal[prim.normal_index[trinr][i]][2]
                            jsonobject['Vertices'].append(nx1)
                            jsonobject['Vertices'].append(ny1)
                            jsonobject['Vertices'].append(nz1)

                        if(jsonobject['VertexSemantic'].find('c') != -1):
                            jsonobject['Vertices'].append(jsonobject['Color'][0])
                            jsonobject['Vertices'].append(jsonobject['Color'][1])
                            jsonobject['Vertices'].append(jsonobject['Color'][2])
                            jsonobject['Vertices'].append(jsonobject['Color'][3])

                        if (jsonobject['VertexSemantic'].find('t') != -1):
                            u1 = prim.texcoordset[0][prim.texcoord_indexset[0][trinr][i]][0]
                            v1 = prim.texcoordset[0][prim.texcoord_indexset[0][trinr][i]][1]
                            jsonobject['Vertices'].append(u1)
                            jsonobject['Vertices'].append(v1)

                        i=i+1

                    jsonobject['Indices'].append(idx)
                    idx = idx+1
                    jsonobject['Indices'].append(idx)
                    idx = idx+1
                    jsonobject['Indices'].append(idx)
                    idx = idx+1



                    trinr = trinr+1


        write_to_json(jsonobject,file)



    except:
        traceback.print_exc()
        print
        print "Failed to load collada file."
        sys.exit(1)

    print
    print 'Successfully loaded collada file.'
    print 'There were %d errors' % len(col.errors)

    for e in col.errors:
        print e








