import pathlib
import subprocess
import osmium
import os
from collections import namedtuple


class PoiHandler(osmium.SimpleHandler):
    def __init__(self, poitypes):
        osmium.SimpleHandler.__init__(self)
        self.num_poi = 0
        self.poi_types = poitypes
        self.liste = set()

    def conc_p(self, p, n):
        label = "{};{}".format(p.Tag, p.Type if p.Type != None else "")
        return label

    def is_valid_poi(self, p, n):
        if p.Type == None:
            return n.tags.get(p.Tag) != None
        else:
            return n.tags.get(p.Tag) == p.Type

    def node(self, n):
        '''
            Defines how to handle nodes
        '''
        # Checks if the given node is of any type in the search list
        for p in self.poi_types:
            if self.is_valid_poi(p, n):
                self.num_poi += 1
                data = Poi(n.id, n.tags.get("name"), n.location, n.tags.get(
                    "addr:street"), n.tags.get("addr:housenumber"), self.conc_p(p, n))

                # Adds the first POI-Type that matches
                self.liste.add(data)
                break


class Poi():
    def __init__(self, id, name, location, adress, street_number, poi_type):
        self.id = id
        self.name = name
        # Longitude, Latitude
        self.location = location
        self.street = adress
        self.street_number = street_number
        self.type = poi_type

    def toString(self):
        return "{};{};{};{};{};{}".format(self.id, self.name, self.location, self.street, self.street_number, self.type)


ORIGINAL_MAP_NAME = "nrw.osm.pbf"
POLY_NAME = "duesseldorf.poly"
EXTRACTED_MAP_NAME = "duesseldorf-osmconvert.pbf"
Poi_type = namedtuple("Poi_type", ('Tag', "Type"))

# Type=None looks for all nodes with the given Tag
# Providing a type only adds note of that type
POI_TYPES = [Poi_type(Tag="parking", Type=None),
             Poi_type(Tag='area:highway', Type="pedestrian"),
             Poi_type(Tag="shop", Type=None)]

OUTPUT_CSV_NAME = 'plaetze-duesseldorf.csv'
FILE_PATH = ".\\"
ALL_TO_NODES = True


# Defines how data is extracted from the osm.pbf
if ALL_TO_NODES:
    # tranforms every entry (i.e. relations) to a node with its centerpoint as coordinate.
    # particularly useful when using the data of places
    EXTRACTION_TYPE = " --all-to-nodes -o="
else:
    # extracts the map with relations, paths and nodes
    EXTRACTION_TYPE = " --complete-boundaries -o="


# Concatenating the commandline statement
# The .exe is available at https://wiki.openstreetmap.org/wiki/Osmconvert
cmd_string = FILE_PATH + "osmconvert64-0.8.8p.exe " + FILE_PATH + \
    ORIGINAL_MAP_NAME + " -B=" + POLY_NAME + \
    EXTRACTION_TYPE + FILE_PATH + EXTRACTED_MAP_NAME


# Creates a new map if necessary based on the defined polygon / area
if os.path.isfile(FILE_PATH + EXTRACTED_MAP_NAME):
    print("Map exists.")
else:
    print("You called: " + cmd_string +
          "\n Creating the map will take some time...")
    subprocess.call(cmd_string)
    print("Map creation finished.")

print("POI extraction begins.")

# Extracts all relevant POIs from the newly created map
handler = PoiHandler(POI_TYPES)
handler.apply_file(EXTRACTED_MAP_NAME)
print('Number of POIs: ', handler.num_poi)
for n in handler.liste:
    print(n.toString())

# Writing all POIs to a .csv
with open(OUTPUT_CSV_NAME, 'w', encoding="utf-8") as f:
    f.write("ID;Name;Long/Lat;Adress;Poi_Type")
    for n in handler.liste:
        f.write(n.toString()+"\n")

print("Data is extracted. \n{} POIs were written.".format(len(handler.liste)))
