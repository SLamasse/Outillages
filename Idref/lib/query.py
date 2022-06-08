from SPARQLWrapper import SPARQLWrapper, POST, JSON


def Do_query(endpoint, prefix, requete):
    # On utilise la bibliothèque SPARQLWrapper 
    # On se connecte au endpoint 
    sparql = SPARQLWrapper(endpoint)
    sparql.setMethod(POST)
    # On produit une crée la requête avec prefix + requete
    query = str(prefix + requete)
#    print(query)
    sparql.setQuery(query) 
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result 
    
    
def  createwordsearch(wsearch):
    i = 1

    for elt in wsearch:
        if i == 1:
            wordsearch = """  '" """ + elt + """ " """
        elif i == len(wsearch):
            wordsearch += """ or " """ + elt + """ "' """
        else:
            wordsearch += """ or " """ + elt + """ " """
        i +=1
    return wordsearch


def findRameau(wordsSearch):
    findRameau=u"""SELECT DISTINCT  * 
                            WHERE {	
                                 ?idref a skos:Concept.  
                                 ?idref skos:prefLabel   ?label.  
                                 ?label bif:contains """ +  wordsSearch  + """. 
                            OPTIONAL{ 
                                 ?idref skos:altLabel  ?altlabel. 
                                 ?altlabel bif:contains """  + wordsSearch + """ .}} """ 
    return findRameau


def refBiblioAutorite(autorite):
	query = """
	PREFIX dcterms: <http://purl.org/dc/terms/> 
	SELECT * 
	WHERE {?uri ?relator " + autorite + " ; dcterms:bibliographicCitation ?titre.}"""
