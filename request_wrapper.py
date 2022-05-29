import requests
import pdb
import time
import sys

# for linkedgeodata: #http://linkedgeodata.org/sparql

class RequestWrapper:
    def __init__(self, baseuri = "https://query.wikidata.org/sparql"):

        self.baseuri = baseuri

    def response_handler(self, response, query):
        if response.status_code == requests.codes.ok: 
            ret_json = response.json()['results']['bindings']
        elif response.status_code == 500: 
            ret_json = []
            #print(q_id)
            print('Internal Error happened. Set ret_json to be empty list')
        
        elif response.status_code == 429: 

            print(response.status_code)
            print(response.text)
            retry_seconds = int(response.text.split('Too Many Requests - Please retry in ')[1].split(' seconds')[0])
            print('rerun in %d seconds' %retry_seconds)
            time.sleep(retry_seconds + 1)
            
            response = requests.get(self.baseuri, params = {'format':'json', 'query':query})
            ret_json = response.json()['results']['bindings']
            #print(ret_json)
            print('resumed and succeeded')

        else:
            print(response.status_code, response.text)
            exit(-1)

        return ret_json

    '''Search for wikidata entities given the name string'''
    def wikidata_query (self, name_str): 
        
        query = """
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

            SELECT ?item ?coordinates ?itemDescription WHERE {
            ?item rdfs:label \"%s\"@en;
                    wdt:P625 ?coordinates . 
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
                    }
            """%(name_str)

        response = requests.get(self.baseuri, params = {'format':'json', 'query':query})


        ret_json = self.response_handler(response, query)

        return ret_json


    '''Search for wikidata entities given the name string'''
    def wikidata_query_withinstate (self, name_str, state_id = 'Q99'): 


        query = """
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

            SELECT ?item ?coordinates ?itemDescription WHERE {
            ?item rdfs:label \"%s\"@en;
                    wdt:P625 ?coordinates ;
                    wdt:P131+ wd:%s;
                    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
                    }
            """%(name_str, state_id)

        #print(query)

        response = requests.get(self.baseuri, params = {'format':'json', 'query':query})

        ret_json = self.response_handler(response, query)
        
        return ret_json
        

    '''Search for nearby wikidata entities given the entity id'''
    def wikidata_nearby_query (self, q_id):

        query = """
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

            SELECT ?place ?placeLabel ?location ?instanceLabel ?placeDescription
            WHERE
            {
              wd:%s wdt:P625 ?loc .
              SERVICE wikibase:around {
                  ?place wdt:P625 ?location .
                  bd:serviceParam wikibase:center ?loc .
                  bd:serviceParam wikibase:radius "5" .
              }
              OPTIONAL {    ?place wdt:P31 ?instance  }
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
              BIND(geof:distance(?loc, ?location) as ?dist)
            } ORDER BY ?dist
            LIMIT 200
            """%(q_id)
            # initially 2km

        #pdb.set_trace()
        
        response = requests.get(self.baseuri, params = {'format':'json', 'query':query})


        ret_json = self.response_handler(response, query)
        
            

        return ret_json


        

    def linkedgeodata_query (self, name_str):

        query = """

        Prefix lgdo: <http://linkedgeodata.org/ontology/>
        Prefix geom: <http://geovocab.org/geometry#>
        Prefix ogc: <http://www.opengis.net/ont/geosparql#>
        Prefix owl: <http://www.w3.org/2002/07/owl#>
        Prefix wgs84_pos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        Prefix owl: <http://www.w3.org/2002/07/owl#>
        Prefix gn: <http://www.geonames.org/ontology#>

        Select ?s, ?lat, ?long {
            {?s rdfs:label \"%s\";
                wgs84_pos:lat ?lat ;
                wgs84_pos:long ?long;
                } 
        } 
        """%(name_str)

        

        response = requests.get(self.baseuri, params = {'format':'json', 'query':query})


        ret_json = self.response_handler(response, query)


        return ret_json

def guide():
    print("Option 1 (query all): $ python3", sys.argv[0], "<'all'> <entity-name>")
    print("ex. $ python3", sys.argv[0], 'all "New York"')
    print()
    print("Option 2 (query ca only): $ python3", sys.argv[0], "<'ca'> <entity-name>")
    print("ex. $ python3", sys.argv[0], 'ca "San Diego"')
    print()
    print("Option 3 (query nearby query): $ python3", sys.argv[0], "<'nearby'> <QID>")
    print("ex. $ python3", sys.argv[0], 'nearby Q370771')
    print()





    
if __name__ == '__main__':
    # new object
    example = RequestWrapper(baseuri = 'https://query.wikidata.org/sparql')

    #Sydney's examples

    # # making string with more than 1 word
    # full = sys.argv[1]
    # for i in range(2, len(sys.argv)):
    #     full += " " + sys.argv[i]
    # # print(full)

    # #printing out the within state function
    # result = example.wikidata_query_withinstate(full)
    # print(result)

    #printing out the nearby function
    # result2 = example.wikidata_nearby_query(sys.argv[1])
    # print(result2)

    #more user friendly version
    if sys.argv[1] == "all":
        result = example.wikidata_query(sys.argv[2])
        print(result)
    elif sys.argv[1] == "ca":
        result = example.wikidata_query_withinstate(sys.argv[2])
        print(result)
    elif sys.argv[1] == "nearby":
        result = example.wikidata_nearby_query(sys.argv[2])
        print(result)
    else:
        guide()




    #Zekun's examples

    #print(request_wrapper_wikidata.wikidata_nearby_query('Q370771'))
    #print(request_wrapper_wikidata.wikidata_query_withinstate('San Bernardino'))

    # not working now
    # print(request_wrapper_wikidata.linkedgeodata_query('San Bernardino'))