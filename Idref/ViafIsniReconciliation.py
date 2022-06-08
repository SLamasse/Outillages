import pandas as pd
import re
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
import numpy as np
from requetes import  *  # l'ensemble des requetes SPARQL utilisés ici
from lib.query  import * # fonctions ad hoc 


kwargs = {'sep': ';', 'dtype': str, 'encoding': 'utf8'}
endpoint = "https://data.idref.fr/sparql" # Endpoint IdRef

'''
Etape 1. On récupère le fichier qui est dans le répertoire results
'''
path = "listIdref"
dir_list = os.listdir(path)


prefix  = """ 
    PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
    PREFIX owl: <http://www.w3.org/2002/07/owl#> 
    PREFIX isni: <http://isni.org/ontology#> 
    PREFIX bnf-onto: <http://data.bnf.fr/ontology/bnf-onto/> """

for fichier in dir_list:

    '''
    Etape 2. On ouvre le fichier pour récupérer la colonne idref sur
    laquelle on fait une boucle
    '''
    df = pd.read_csv(path + "/" +fichier, **kwargs)

    IdRef = []
    for link in df.lienID:
        IdRef.append(link)

    allId= IdRefAfiltrer(IdRef)
    query = IdRefalignmentToviaf(allId)
    result =  Do_query(endpoint, prefix, query)
    totab = []
    for res in result["results"]["bindings"]:
        if "idref" in res  :
            idref = res["idref"]["value"]
        else:
            idref = "NA"
        if "nom" in res  :
            nom = res["nom"]["value"]
        else:
            nom = "NA"                
        if "viaf" in res  :
            viaf = res["viaf"]["value"]
        else:
            viaf = "NA"                
        if "isni" in res  :
            isni = res["isni"]["value"]
        else:
            isni = "NA"
        if "frbnf" in res  :
            frbnf = res["frbnf"]["value"]
        else:
            frbnf = "NA"
        totab.append([idref,nom,viaf,isni,frbnf])

    '''
    Etape 3. On écrit les résultats dans un fichier 
    '''
    df = pd.DataFrame (totab, columns = ['Idref','Nom','Viaf','Isni','frbnf'])
    df.to_csv("results/ReconciliationIdrefViaf.csv", index=False, sep=";")
