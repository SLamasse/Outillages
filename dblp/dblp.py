# -*- coding: utf-8 -*-
import os
import sys        #Pour lire les paramètres saisis
import requests   #Pour récupérer les données d'une page web
import json       #Pour encoder les données dans un fichier json
import csv        #Pour mettre le résultat de la recherche dans un fichier csv

"""
Fonction qui recherche le mot clef dans la base de donnée dblp.org
On utilise l'API mise en ligne par dblp.org
On met dans l'URL la requête qu'on souhaite afficher
"""
def rechercheapi(nbresult, outformat, search, first=None, year=None):
    if year is not None and first is not None: 
        query = "https://dblp.uni-trier.de/search/publ/api?q=\""+ search +"\" year:" + str(year) + "&f=" + str(first) + "&h=" + str(nbresult) +"&format=" + outformat
    elif year is not None :
        query = "https://dblp.uni-trier.de/search/publ/api?q=\""+ search +"\" year:" + str(year) + "&h=" + str(nbresult) +"&format=" + outformat
    else:
        query = "https://dblp.uni-trier.de/search/publ/api?q=\""+ search +"\"&f=" + str(first) + "&h=" + str(nbresult) +"&format=" + outformat

    resp = requests.get(url=query)
    data = resp.json()
    #print(query)
    return data

"""
Fonction qui lit le résultat de la recherche retourné (qui va lire le fichier json)
On introduit des tests dans cette fonction
hits ce sont les résultats pour le mot clef saisi (c'est un tableau qui commence à 0)
"""
def parsejson(res, motclef):
    reference = []
    auteurs = []
    if 'hit' not in res['result']['hits']:
        return reference, auteurs
    for elt in res['result']['hits']['hit'] :  #Il va lire chaque élément des données parsées (titre, doi, pages, etc.)
        iddblp = elt['@id']
        if 'title' not in elt['info']:
            title = "pas de titre"
        else:
            title =  elt['info']['title']
        if 'ee' not in elt['info']:
            doi = "pas de doi"
        else:
            doi = elt['info']['ee']
        if 'pages' not in elt['info']:
            pages = "pas de pages"
        else:
            pages = elt['info']['pages']
            
        annee = elt['info']['year']
        typeref = elt['info']['type']
        try :
            authors = elt['info']['authors']
            for k,v in authors.items():
                if isinstance(v, list):
                    for elt in v:
                        pid = elt['@pid']
                        a, b = pid.split("/")
                        name = elt['text']
                        pageperson = "https://dblp.uni-trier.de/pid/" + a +"/"+ b +".html"
                        auteurs.append([iddblp, name, pageperson, annee, motclef])      #Information qu'on veut récupérer sur les auteurs
                else:
                    pid = v['@pid']
                    a, b = pid.split("/")
                    name = v['text']
                    pageperson = "https://dblp.uni-trier.de/pid/" + a +"/"+ b +".html"
                    auteurs.append([iddblp, name, pageperson, annee, motclef])          #Informations qu'on veut récupérer sur les références
        except:
            pass
        reference.append([iddblp, motclef, title, annee, typeref, pages, doi])
    return reference, auteurs

"""
Programme principal
"""
def main():
    authors = []
    reference = []
    length = len(sys.argv)                    #Il compte le nombre d'arguments/paramètres saisis
    if length >= 5:                           #S'il y en a plus de 4, il passe au range
        mini = int(sys.argv[3])               #Recherche qui débute à telle année (mini) / Facultatif
        maxi = int(sys.argv[4])               #Recherche qui se termine à telle année (maxi) / Facultatif
    else :                                    #Sinon, j'applique les valeurs par défaut
        mini = 1950                           #Valeurs par défaut pour l'année : entre 1950 et 2021
        maxi = 2021
        #mini = int(input("Annee min: "))
        #maxi = int(input("Annee max: "))
    if length >= 3:                           #Idem avec le nombre de recherche pas année / Facultatif
        nb = sys.argv[2]
    else :
        nb = "100000"                         #Si je ne saisie rien, il recherche 100 000 résultats par défaut.
    if length >= 2 :                          #Idem avec le mot clef / Obligatoire
        search = sys.argv[1]
    else :
        search = input("Mot clef : ")         #Si je saisie tous les autres arguments, sauf le mot clef,
                                              #alors le programme me le demande dans le terminal

    #Pour décomposer le travail de parsing, on fait année par année.
    #Ici on débute en 1950.
    #mini et maxi sont ici les deux années entre lesquelles on veut interroger la base dblp.org
    for a in range(mini,maxi):
        outformat = "json"                                             #Format du fichier parsé
        res1 = rechercheapi(nb, outformat, search, first="0", year=a)  #Ce qu'il retourne pour chaque année
        total = res1['result']['hits']['@total']                       #Il met chaque résultat dans un tableau
        fi = int(total)                                                #Il récupère la taille du tableau
        i = 0

    #On cherche les milliers, puis le reste.
    #On fait mille par mille car l'API ne peut afficher que 1000 références au maximum par page.
    #Donc on veut savoir si c'est divisible par 1000, pour connaître le nombre de pages à tourner.
    #Combien de fois il y a 1000, et le reste me dit ce qu'il faut prendre.
        q, r = divmod(fi,1000)
        if q== 0 and r ==0 :
            pass
        else:
            while (i <= q):
           # f : c'est le nombre du début de la liste de chaque retour
           # r : c'est le nombre de référence dans chaque retour
                f = (i * 1000)
                if i == q :
                    nb = r
                else :
                    nb = 1000
                res = rechercheapi(nb, outformat, search, first=f, year=a)
                mylistref = parsejson(res, search)
                reference.append(mylistref[0])
                authors.append(mylistref[1])
                i += 1
    out = search + "_parsed_data.csv"                #Création du fichier csv des références (avec nom de la recherche)
    with open(out, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL,delimiter=';')
        for elt in reference:
            writer.writerows(elt)
    out = search + "_authors.csv"                    #Création du fichier csv des auteurs (avec nom de la recherche)
    with open(out, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_ALL,delimiter=';')
        for elt in authors:
            writer.writerows(elt)
    return 0

if __name__ == "__main__":
    main()


