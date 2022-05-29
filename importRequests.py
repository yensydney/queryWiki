import requests
import sys

def isValid(response):
    statusCode = response.status_code
    if response.status_code == requests.codes.ok: 
        return True
    else:
        return False

def makeJson(response):
    return response.json()
        

targetDir = sys.argv[0]

r = requests.get('https://query.wikidata.org/sparql', {"format":"json", "query":' \
        SELECT ?item ?itemLabel ?coordinates ?itemDescription WHERE { \
    ?item rdfs:label "Carlsbad" @en; \
    wdt:P625 ?coordinates; \
    wdt:P131* wd:Q99. \
    \
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }  }\
    '})

if isValid(r):
    json = makeJson(r)
    for key in json:
        print(key, json[key])
        print()

sys.exit()

print("=====status code:")
print(r.status_code)
print(r.headers['content-type'])
sys.exit()
print(r.encoding)
print(r.text)
print(r.json())

results = r.json()["results"]["bindings"]
print("=====results:")
print(results)

print("=====print per row results:")
for entries in results:
    for entry in entries:
        print("---")
        print(entry)
        print(entries[entry])
