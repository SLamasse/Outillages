import pandas as pd
import re
import os
import datetime
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
import numpy as np
from requetes import  *  # l'ensemble des requetes SPARQL utilisés ici
from lib.query  import * # fonctions ad hoc 



subject = "medievistes"
represult = "listIdref/"
if not os.path.exists(represult):
    os.makedirs(represult)
separator = ";"

endpoint = "https://data.idref.fr/sparql" # Endpoint IdRef

'''
Etape 0. Chercher toutes les vedettes Rameaux qui ont un/des mots clefs
'''
wsearch  = ["Moyen-âge","Médiéval", "Parodie médiévale","Contes médiévaux", "Prose médiévale", "Récits de voyages médiévaux","Musique -- Moyen âge", "Satire médiévale","Poésie médiévale","Littérature anglaise -- 1100-1500 (moyen anglais)","Littérature hébraïque médiévale","Mathématiques médiévales","Sciences médiévales","Français (langue) -- 1300-1500 (moyen français)","Occitan (langue) -- Avant 1500", "Français (langue) -- Avant 1300 (ancien français)", "Histoire religieuse -- France -- 987-1500","Vie intellectuelle -- Europe -- Moyen âge","Historiographie médiévale","Manuscrits médiévaux","Héraldique"]
wordsSearch = createwordsearch(wsearch)
q = findRameau(wordsSearch)
res = Do_query(endpoint, prefix, q)
IdRef = []
for elt in res["results"]["bindings"]:
      IdRef.append(elt["idref"]["value"])



#print(IdRef)
vedettes = vedettetoSearch(IdRef)
findallscholar= findscholarFromRameau(vedettes)
result =  Do_query(endpoint, prefix, findallscholar)



'''
Etape 1 . On construit un dataFrame en Pandas pour exploiter les
résultats bibliometriques. Il s'agit du fichier de tous les
individus présentés de la façon suivante : 
             'nom', 'lienID', 'naissance','mort', 'genre'
'''
#  Construction du tableau à partir des résultats en JSON 
totab = []
for res in result["results"]["bindings"]:
    if "mort" in res  :
        m = res["mort"]["value"]
    else:
        m = "NA"     
    if "naissance" in res  :
        n = res["naissance"]["value"]
    else:
        n = "NA"     
    if "genre" in res  :
        g = res["genre"]["value"]
    else:
        g = "NA"     

    totab.append([res["nom"]["value"], res["auteur"]["value"], n, m, g])

# Tableau pandas 
resdf = pd.DataFrame(totab, columns=['nom', 'lienID', 'Datenaissance','Datemort', 'genre'])

# On créer deux colonnes n = naissance ; m = mort
resdf['naissance'] = resdf['Datenaissance']
resdf['mort'] = resdf['Datemort']
# des petites transformations regex pour ne garder que les dates
# format 4 chiffres 
resdf['naissance'] =  [re.sub(r'^([0-9]{4}).+',r'\1', str(x)) for x in  resdf['naissance']]
resdf['mort'] =  [re.sub(r'^([0-9]{4}).+',r'\1', str(x)) for x in resdf['mort']]

# y a quand mêmes des scrotules dans les dates 
resdf['naissance'] =  [re.sub(r'^[0-9\-]{1,3}[Xx\#\.\?\s\-]{1,3}|[A-Z]+|[0\-\?]+|[\.]{1,4}|d[0-9]+','0', str(x)) for x in  resdf['naissance']]
resdf['mort'] =  [re.sub(r'^[0-9\-]{1,3}[Xx#\.\?\s\-]{1,3}|[A-Z]+|[0\-\?]+|[\.]{1,4}|d[0-9]+','0', str(x)) for x in resdf['mort']]

# maintenant on peut en faire des entiers pour calculer une médiane de
# vie 
resdf['naissance'] = resdf['naissance'].astype(int)
resdf['mort'] = resdf['mort'].astype(int)
resdf['finActivite'] = resdf['mort'].astype(int)

# quand les individus sont encore vivant on leur donne une fin
# d'activité factice qui est l'année d'aujourd'hui 
nonmort = (resdf['naissance'] > 1925) & (resdf['mort']< 1925)
cetteannee  = datetime.date.today().year
resdf.loc[nonmort, 'finActivite'] = cetteannee 

# On écrit le fichier de resultat complet
#Totfile = represult + "All"  + subject + ".csv"
#resdf.to_csv(Totfile,  index=False, sep=separator)


'''
Etate 2. On filtre le tableau pour ne garder que les individus après
une certaine date 
'''
# On fait une median d'activité
datedebut = 1848
datemax = cetteannee + 1  # todo faire un supérieur ou égal
resdf['median']  = resdf[['finActivite', 'naissance']].median(axis=1)
resdf = resdf[resdf["median"] < datemax]
filterdf = resdf[resdf["median"] > datedebut]

# on calcul et fabrique une colonne d'intervale avec un début auquel
# on ajoute 28 ans
# !!!! -> todo problème avec la fonction zip 
#filterdf['debplus28'] = filterdf['n'] + 28
#filterdf["interval"] = list(zip(filterdf['debplus28'], filterdf['mort']))

# On écrit le fichier filtré csv sur le disque 
#filterfile = represult + "Filter"  + subject + ".csv"
filterfile = represult + subject + ".csv"
filterdf.to_csv(filterfile, index=False, sep=separator)


# On essaie une représentation :  distribution des médiévistes en fonction de leur médiane de vie 
#gp = filterdf.groupby('median')["median"]
#nb = gp.count()
#names = gp.groups.keys()
#plt.bar(names, nb, color='red' )
#plt.show()




