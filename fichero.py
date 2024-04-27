import json
import os
import pandas as pandas
import uuid             #Para crear un id único para cada usuario ingresado

def crear_fichero(formulario):
    print("dentro de crear json")
    #comprobamos si existe el fichero
    if os.path.exists("archivo.txt"):
        print("existe")
        #si no existe lo creamos        
        formulario = dict(formulario)
        formulario['id'] = uuid.uuid4().hex
        print(formulario)
        formulario = json.dumps(formulario)
        fichero = open("archivo.txt", "a")
        fichero.write(formulario + '\n')
    else:
        #si existe añadimos contenido al final
        print("NO EXISTE")
        with open('archivo.txt', 'w') as fichero:
            formulario = dict(formulario)
            formulario['id'] = uuid.uuid4().hex
            print(formulario)
            formulario = json.dumps(formulario)
            fichero.write(formulario + '\n')
    fichero.close()
    
def leer_fichero():
    if os.path.exists("archivo.txt"):
        f = open('archivo.txt','r+')
        s = f.read()
        s=[ json.loads(s) for s in s.splitlines()]
        df=pandas.DataFrame(s)
        f.close()   
        return df
    else:
        return "error" 
    
# def cuenta_lineas():
#     #Devuelve el número de lineas ya que lo utilizaremos como id
#     lines = 0
#     with open('archivo.txt','r') as fichero:
#         for line in fichero:
#             lines = lines + 1
#     print('numero de lineas :',lines)
#     fichero.close()
#     return lines

def buscar_registro(id):
    #Buscamos el la linea que contiene el id y devolvemos su indice
    fichero = open('archivo.txt','r+')
    datos = fichero.readlines()
    indice = 0
    registro = {}
    for linea in datos:
        if (id) in linea:
            print("Encontrado el id en el indice nº ",indice )
            print('registro ' ,linea)
            registro = linea
            break
    fichero.close() 
    return registro 
 
def cargar_registro(indice):
    pass

def leer_registro(indice):
    #Accedemos directamente a la línea indice y leemos sus datos
    indice = int(indice)
    with open('archivo.txt','r') as fichero:
        datos = fichero.readlines()
    fichero.close()
    return (datos[indice])
    
    