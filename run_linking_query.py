#from query_wrapper import QueryWrapper
from request_wrapper import RequestWrapper
from get_namelist import *
import glob
import os
import json
import time
import sys

DATASET_OPTIONS = ['OSM', 'OS', 'USGS', 'GB1900']
KB_OPTIONS = ['wikidata', 'linkedgeodata']

DATASET = 'USGS'
KB = 'wikidata'
OVERWRITE = True
WITHIN_CA = True
NEARBY = False

assert DATASET in DATASET_OPTIONS
assert KB in KB_OPTIONS


def process_one_namelist(sparql_wrapper, namelist, out_path):

    if OVERWRITE:
        # flush the file if it's been written
        with open(out_path, 'w') as f:
            f.write('')


    for name in namelist:
        name = name.replace('"', '')
        name = name.strip("'")  # removing spaces
        if len(name) == 0: # making sure name is not empty
          continue
        print(name)
        mydict = dict()

        if KB == 'wikidata': # calling correct functions
            if WITHIN_CA:
                mydict[name] =  sparql_wrapper.wikidata_query_withinstate(name)
            else:
                mydict[name] =  sparql_wrapper.wikidata_query(name)

        elif KB == 'linkedgeodata':
            mydict[name] =  sparql_wrapper.linkedgeodata_query(name)
        else:
            raise NotImplementedError # exception

        line = json.dumps(mydict)
        
        with open(out_path, 'a') as f:
            f.write(line)
            f.write('\n')
        time.sleep(1)


def process_namelist_dict(sparql_wrapper, namelist_dict, out_dir):
    i = 0
    for map_name, namelist in namelist_dict.items():
        # if i <=5:
        #     i += 1
        #     continue 

        print('processing %s' %map_name)

        if WITHIN_CA:
            out_path = os.path.join(out_dir, KB + '_' + map_name + '.json')
        else:
            out_path = os.path.join(out_dir, KB + '_ca_' + map_name + '.json')

        process_one_namelist(sparql_wrapper, namelist, out_path)
        i+=1


if KB == 'linkedgeodata':
    sparql_wrapper = RequestWrapper(baseuri = 'http://linkedgeodata.org/sparql')
elif KB == 'wikidata':
    sparql_wrapper = RequestWrapper(baseuri = 'https://query.wikidata.org/sparql')
else:
    raise NotImplementedError



if DATASET == 'OSM':
    osm_dir = '../surface_form/data_sample_london/data_osm/'
    osm_paths = glob.glob(os.path.join(osm_dir, 'embedding*.json'))
    
    out_path = 'outputs/'+KB+'_linking.json'
    namelist = get_name_list_osm(osm_paths)
    
    print('# files',len(file_paths))

    process_one_namelist(sparql_wrapper, namelist, out_path)
    
    
elif DATASET == 'OS':  
    histmap_dir = 'data/labGISReport-master/output/'
    file_paths = glob.glob(os.path.join(histmap_dir, '10*.json'))
    
    out_path = 'outputs/'+KB+'_os_linking_descript.json'
    namelist = get_name_list_usgs_od(file_paths)
    
    print('# files',len(file_paths))
    

    process_one_namelist(sparql_wrapper, namelist, out_path)
    
elif DATASET == 'USGS':
    histmap_dir = 'data/labGISReport-master/output/'
    file_paths = glob.glob(os.path.join(histmap_dir, 'USGS*.json'))
    
    if WITHIN_CA:
        out_dir = 'outputs/' + KB +'_ca'
    else:
        out_dir = 'outputs/' + KB 
    namelist_dict = get_name_list_usgs_od_per_map(file_paths)

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    
    print('# files',len(file_paths))

    process_namelist_dict(sparql_wrapper, namelist_dict, out_dir)

elif DATASET == 'GB1900':

    file_path = 'data/GB1900_gazetteer_abridged_july_2018/gb1900_abridged.csv'
    out_path = 'outputs/'+KB+'_gb1900_linking_descript.json'
    namelist = get_name_list_gb1900(file_path)


    process_one_namelist(sparql_wrapper, namelist, out_path)
    
else:
    raise NotImplementedError

def guide():
        print()
        print("Wrong format! See below.")
        print()
        print("Option 1 (query all): $ python3", sys.argv[0], "<'all'> <entity-name>")
        print("ex. $ python3", sys.argv[0], 'all "New York" "San Diego"')
        print()
        print("Option 2 (query ca only): $ python3", sys.argv[0], "<'ca'> <entity-name>")
        print("ex. $ python3", sys.argv[0], 'ca "San Diego" "Death Valley"')
        print()
        # print("Option 3 (query nearby query): $ python3", sys.argv[0], "<'nearby'> <QID>")
        # print("ex. $ python3", sys.argv[0], 'nearby Q370771')
        # print()




#namelist = namelist[730:]   #for GB1900



print('done')

if __name__ == '__main__':
    example = RequestWrapper(baseuri = 'https://query.wikidata.org/sparql')
    myNamesList = []
    # myNamesList = ['San Diego', 'Death Valley', 'Disney']
    # myNamesDict = {''}
    # process_one_namelist(example, myNames, "test.txt")
    # process_namelist_dict(example, )
    if len(sys.argv) > 2:
        for i in range(2, len(sys.argv)):
            myNamesList.append(sys.argv[i])
        if sys.argv[1] == "all":
            WITHIN_CA = False
            NEARBY = False
            process_one_namelist(example, myNamesList, "test.txt")
        elif sys.argv[1] == "ca":
            WITHIN_CA = True
            NEARBY = False
            process_one_namelist(example, myNamesList, "test.txt")
        # elif sys.argv[1] == "nearby":
        #     NEARBY = True
        #     WITHIN_CA = False
            
        else:
            guide()
    else:
        guide()













