import requests
import json
import csv

resultadoFinalDict={}
page=1
contador_recursos=0
datasets = set()
dictAliasRecurso={'recurso_description':'http://purl.org/dc/terms/description',
           'recurso_format':'http://purl.org/dc/terms/format',
           'recurso_issued':'http://purl.org/dc/terms/issued',
           'recurso_modified':'http://purl.org/dc/terms/modified',
           'recurso_title':'http://www.w3.org/ns/dcat#accessURL',
           'recurso_access_url':'http://www.w3.org/ns/dcat#accessURL',
           'recurso_mediaType':'http://www.w3.org/ns/dcat#mediaType'
           }

#Si devuelve 2 recursos, significa que finalizó.
while contador_recursos != 2:
    #Hace request
    response = requests.get(f'http://0.0.0.0:5000/catalog.jsonld?page={page}')
    response = response.text
    #Crea diccionario con respuesta y lo carga en diccionario final.
    responseDict = json.loads(response)
    resultadoFinalDict[page] = responseDict
    #Cuenta los recursos de la respuesta
    contador_recursos = len(responseDict)
    page+=1

#Itera diccionario final y lo guarda en archivo CSV
salida = open("salida.csv","w+")
#Se crea header
salida.write('dataset_id; recurso_description; recurso_format; recurso_issued; recurso_modified; '
             'recurso_title; recurso_access_url; recurso_mediaType\n')

for x in resultadoFinalDict:
    for recurso in range(len(resultadoFinalDict[x])):
        dataset_id = ''
        dataset_id = resultadoFinalDict[x][recurso]['@id']

        try:
            #datasets.add(dataset_id.split('/')[4])
            dataset_id = dataset_id.split('/')[4]
            datasets.add(dataset_id)
        except:
            pass

        if dataset_id != '':
            try:
                recurso_description=resultadoFinalDict[x][recurso][dictAliasRecurso['recurso_description']][0]['@value']
            except:
                recurso_description=''
            try:
                recurso_format=resultadoFinalDict[x][recurso]['http://purl.org/dc/terms/format'][0]['@value']
            except:
                recurso_format=''
            try:
                recurso_issued=resultadoFinalDict[x][recurso]['http://purl.org/dc/terms/issued'][0]['@value']
            except:
                recurso_issued=''
            try:
                recurso_modified=resultadoFinalDict[x][recurso]['http://purl.org/dc/terms/modified'][0]['@value']
            except:
                recurso_modified=''
            try:
                recurso_title=resultadoFinalDict[x][recurso]['http://purl.org/dc/terms/title'][0]['@value']
            except:
                recurso_title=''
            try:
                recurso_access_url=resultadoFinalDict[x][recurso]['http://www.w3.org/ns/dcat#accessURL'][0]['@id']
            except:
                recurso_access_url=''
            try:
                recurso_mediaType=resultadoFinalDict[x][recurso]['http://www.w3.org/ns/dcat#mediaType'][0]['@value']
            except:
                recurso_mediaType=''

            if recurso_access_url != '':
                salida.write(f'{dataset_id};{recurso_description};{recurso_format};{recurso_issued};{recurso_modified};'
                f'{recurso_title};{recurso_access_url};{recurso_mediaType}\n')

salida.close()
print(len(datasets))