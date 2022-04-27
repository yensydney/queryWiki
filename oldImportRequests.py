from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint

sparql = SPARQLWrapper("https://query.wikidata.org/")
    # "http://www.wikidata.org/entity/"
    # "http://www.wikidata.org/entity/statement/"
    # "http://www.wikidata.org/value/"
    # "http://www.wikidata.org/prop/direct/"
    # "http://wikiba.se/ontology#"
    # "http://www.wikidata.org/prop/"
    # "http://www.wikidata.org/prop/statement/"
    # "http://www.wikidata.org/prop/qualifier/"
    # "http://www.w3.org/2000/01/rdf-schema#"
    # "http://www.bigdata.com/rdf#"



# gets the first 3 geological ages
# from a Geological Timescale database,
# via a SPARQL endpoint
sparql.setQuery("""
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wds: <http://www.wikidata.org/entity/statement/>
    PREFIX wdv: <http://www.wikidata.org/value/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>
    SELECT ?item ?itemLabel ?coordinates ?itemDescription WHERE {
    ?item rdfs:label "San Diego" @en;
    wdt:P625 ?coordinates;
    wdt:P131* wd:Q99.
   
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
    """
)

sparql.setReturnFormat(JSON)
qres = sparql.query().convert()

pprint(qres)
for result in qres['results']['bindings']:
    print(result['object'])

# ret = sparql.queryAndConvert()

# for r in ret["results"]["bindings"]:
#     print(r)