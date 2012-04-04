from collada.triangleset import BoundTriangleSet

__author__ = 'benjamin.loesch'

import collada
import sys
import traceback
import math


vertices = []
index = []




def write_to_json(dict,file):


    file.write('{\n')
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
    file.write('\n\t}\n')




def convertCollada(filename,colladastring,center):

    tmpColladaFilename = 'tmp'+filename
    part = filename.split('.')
    tmpJsonFilename = part[0]+'.json'

    colfile = open(tmpColladaFilename,'w')
    colfile.write(colladastring)
    colfile.close()

    try:

        col = collada.Collada(tmpColladaFilename,\
            ignore=[collada.DaeUnsupportedError, collada.DaeBrokenRefError])

        upaxis = col.assetInfo.upaxis;
        scale = col.assetInfo.unitmeter;
        if scale is None:
            scale=1
        else:
            scale=float(scale)



        file = open(tmpJsonFilename,'w')
        file.write('\t[[')

        for geom in col.scene.objects('geometry'):
            id = 1
            jsonobject = {}
            jsonobject['Center'] = center
            jsonobject['IndexSemantic'] = 'TRIANGLES'
            jsonobject['VertexSemantic'] = 'p'
            jsonobject['Vertices']= []
            jsonobject['Indices'] = []

            for prim in geom.primitives():

                if not isinstance(prim, BoundTriangleSet):
                    continue

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

                jsonobject['Vertices']=[]
                jsonobject['Indices']=[]

                trinr = 0
                idx = 0
                while trinr < prim.ntriangles:

                    i=0
                    while i<3:
                        if(upaxis == "X_UP"):
                            x1 = prim.vertex[prim.vertex_index[trinr][i]][1]*scale
                            y1 = prim.vertex[prim.vertex_index[trinr][i]][0]*scale
                            z1 = prim.vertex[prim.vertex_index[trinr][i]][2]*scale
                        if(upaxis == "Y_UP"):
                            x1 = prim.vertex[prim.vertex_index[trinr][i]][0]*scale
                            y1 = prim.vertex[prim.vertex_index[trinr][i]][1]*scale
                            z1 = prim.vertex[prim.vertex_index[trinr][i]][2]*scale
                        if(upaxis == "Z_UP"):
                            x1 = prim.vertex[prim.vertex_index[trinr][i]][1]*scale
                            y1 = prim.vertex[prim.vertex_index[trinr][i]][2]*scale
                            z1 = prim.vertex[prim.vertex_index[trinr][i]][0]*scale


                        if math.isnan(float(x1)) or math.isnan(float(y1)) or math.isnan(z1):
                            return "{\"alert \" : \" error: file contains NaN values!\"}"

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

                            if math.isnan(float(u1)) or math.isnan(float(v1)):
                                return "Error: File contains NaN values."

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
                file.write(',')


        file.seek(-2,1) #set cursor pos back to remove last ','
        file.write(']]')
        file.close()
        return tmpJsonFilename


    except:
        traceback.print_exc()
        print
        return "Error: Failed to load collada file."










if __name__ == '__main__':
    f = open(sys.argv[1],'r')
    fn = sys.argv[1].split('/')
    fn = fn[-1]
    colladastring = f.read()
    f.close

    convertCollada(fn,colladastring,[8.365824, 47.022749, 500])





