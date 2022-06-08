

'''
J'ai mis ici un ensemble de requêtes qui sont utilisés pour le script
SPARQL 
''' 



#IdRef = ["029400279", "050553720", "050553720", "169554015","030463718","027336905","028298314","028474554","02871203X","029647258","031506313", "027328708", "18379138X", "077071530", "027281566", "027290581","027467317","02945204X", "027336891","02761414X","027700615","027857557","028572688","028972996", "028997263", "028982088", "029647800", "029608236", "033358036","027332004","027516873","033389527","027662705","028406494", "031702287", "031808913", "032784686", "027461491", "027295621","027229319","027296210","027430529","027530523","027782417", "027700658", "031421733", "03231468X", "032609698", "110691695","027336875","156289024","027459233","029112966","030844258", "030886449", "031710050", "033296456","027320332", "033710740","050176978","146881176","027706184","029446708","031120229","027318729","027430464","02743057X","027656039","028429672","02847533X","02852909X","028725913","028974441","029543053","029569834","03105675X","050457446","14503562X","029759994","035280239","101481284","027430499","033369879","034803688","061604526","030466245","02782604X","02822714X","027546160","029771714","111549957","027236412","029690234","027757862","027843882","029426944","027336662","027342689","12514184X","027801330","030469473", "156288907","027531422","027329917","027700267","027226603","101296959","028906969","027324893","027223310","027731553","027495361","028957946","027369846","027229823","02820915X","028210743","028912047","027317153","028907000","027329925"]


prefix = """
    PREFIX dcterms: <http://purl.org/dc/terms/>
    PREFIX marcrel: <http://id.loc.gov/vocabulary/relators/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX bio: <http://purl.org/vocab/bio/0.1/>
    """



def findscholarFromRameau(vedettesRameau):
    findallscholar ="""
    SELECT DISTINCT ?nom ?auteur ?naissance ?mort  ?genre WHERE {
    ?doc dcterms:subject 
    ?idref. filter( """ + vedettesRameau + """)
    ?doc marcrel:aut ?auteur.
    ?auteur foaf:name ?nom.
    ?auteur a foaf:Person.
    OPTIONAL {?auteur foaf:gender ?genre}
    OPTIONAL {?auteur bio:event [a bio:Birth ; bio:date ?naissance]}
    OPTIONAL {?auteur bio:event [a bio:Death ; bio:date ?mort]}
    }
    """
    return findallscholar    
    


def vedettetoSearch(IdRef):
    i = 0
    while i < len(IdRef):
        if i ==0:
            vedettesRameau = "?idref =  <" + IdRef[i] + ">\n"
        else:
            vedettesRameau += " or ?idref =  <" + IdRef[i] + ">\n"
        i +=1

    return vedettesRameau



def IdRefAfiltrer(IdRef):
    i = 0
    while i < len(IdRef):
        if i ==0:
            idR = "<" + IdRef[i] + ">\n"
        else:
            idR += " ,  <" + IdRef[i] + ">\n"
        i +=1

    return idR



def IdRefalignmentToviaf(Idref):
    '''
    Est-ce que je ne peux pas utiliser des or comme plus haut dans la condition de filtre ?  
    '''

    query = """
    SELECT ?idref ?nom ?viaf ?isni ?frbnf 
    WHERE {?idref foaf:primaryTopic ?res
           FILTER(?res IN (""" + Idref + """) 
            )
           ?res foaf:name ?nom.
           optional {?res owl:sameAs ?viaf
                     FILTER((STRSTARTS(STR(?viaf),'http://viaf.org')))
                     } 
           optional {?res isni:identifierValid ?isni} 
           optional {?res bnf-onto:FRBNF ?frbnf}
           } """
    return query

