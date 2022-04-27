import requests
import sys


targetDir = sys.argv[0]

r = requests.get('https://query.wikidata.org/sparql', {"format":"json", "query":' \
        SELECT ?item ?itemLabel ?coordinates ?itemDescription WHERE { \
    ?item rdfs:label "San Diego" @en; \
    wdt:P625 ?coordinates; \
    wdt:P131* wd:Q99. \
    \
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }  }\
    '})
    

print("=====status code:")
print(r.status_code)
# print(r.headers['content-type'])
# print(r.encoding)
# print(r.text)
# print(r.json())

results = r.json()["results"]["bindings"]
print("=====results:")
print(results)

print("=====print per row results:")
for entries in results:
    for entry in entries:
        print("---")
        print(entry)
        print(entries[entry])
