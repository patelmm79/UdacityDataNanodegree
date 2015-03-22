#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


OSMFILE="bogota_colombia.osm"
#OSMFILE="example.osm"

street_type_re = re.compile(r'\S+\.?\b', re.IGNORECASE)


expected=["Carrera","Calle","Avenida","Diagonal","Transversal","Autopista"]

# UPDATE THIS VARIABLE
mapping = { "Av": "Avenida",
            "CALLE": "Calle",
            "CL":"Calle",
            "Cl": "Calle",
            "Cll":"Calle",
            "Clle":"Calle",
            "Cr":"Carrera",
            "Carrea":"Carrera",
            "Carrera15":"Carrera 15",
            "CR":"Carrera",
            "Cra":"Carrera",
            "Crr":"Carrera",
            "aV":"Avenida",
            "calle":"Calle",
            "cra":"Carrera",
            "crr":"Carrera",
            "carrera":"Carrera",
            "economia.uniandes.edu.co":"",
            "email":"",
            "industrial.uniandes.edu.co":"",
            "url":""
            }# mapping library specific to Bogota


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):
    
    # YOUR CODE HERE
    m = street_type_re.search(name)
    
    if m.group(0) not in expected and m.group(0) in mapping:
        name=name.replace(m.group(0),mapping[m.group(0)])
    return name



def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
            try:
                node["visible"]= element.attrib["visible"]
            except KeyError:
                pass
            
            node["id"]= element.attrib["id"]
            node["type"]= element.tag
            created={}
            for item in CREATED:
                created[item]=element.attrib[item]
            node["created"]=created
            pos=[]
            try:
                pos.append(float(element.attrib["lat"]))
                pos.append(float(element.attrib["lon"]))
            except KeyError:
                pass
            node["pos"]=pos
            address={}
            for tag in element.iter("tag"):
                if problemchars.search(tag.attrib["k"]):
                    pass
                if lower_colon.search(tag.attrib["k"]):
                    pass
                
                if tag.attrib["k"]=="addr:housenumber":
                    address["housenumber"]=tag.attrib["v"]
                if tag.attrib["k"]=="addr:street":
                    address["street"]=update_name(tag.attrib["v"],mapping)
                if tag.attrib["k"]=="addr:postcode":
                    address["postcode"]=tag.attrib["v"]
                if tag.attrib["k"]=="amenity":
                    node["amenity"]=tag.attrib["v"]
                if tag.attrib["k"]=="shop":
                    node["shop"]=tag.attrib["v"]
                if tag.attrib["k"]=="cuisine":
                    node["cuisine"]=tag.attrib["v"]
                if tag.attrib["k"]=="name":
                    node["name"]=tag.attrib["v"]
                if tag.attrib["k"]=="phone":
                    node["phone"]=tag.attrib["v"]
                if tag.attrib["k"]=="shop":# added to include shop data
                    node["shop"]=tag.attrib["v"]
                if tag.attrib["k"]=="name":# added to include location names
                    node["name"]=tag.attrib["v"]
                node["address"]=address
            nodes=[]
            for tag in element.iter("nd"):
                nodes.append(tag.attrib["ref"])
            if element.tag=="way":
                node["node_refs"]=nodes
                
                
            #print node
        # YOUR CODE HERE
            #print node
            return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    
    with codecs.open(file_out, "w", encoding='utf8') as fo:

        output=[]
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            
            if el:
                
                data.append(el)
                
                
        fo.write(json.dumps(data).encode('utf-8'))## correction to initial JSON creation code was required in order to obtain proper output acceptable by MongoDB
       
        fo.close()
   
    return data


def quantify_street_types(data):
    # This function processes the street names in the created dictionaries, and counts the number of streets for each
    # for each street type in the "Expected" list.
    
     street_stats={}# output statistics to determine how many types of each expecdted street
     for item in expected:
         street_stats[item]=0
         
     for dict in data:
         if "address" in dict and "street" in dict["address"] and dict["address"]["street"]!='':
           street_type=  street_type_re.search(dict["address"]["street"]).group(0)
           if street_type in expected:
             #print street_type_re.search(dict["address"]["street"]).group(0)
             street_stats[street_type]+=1
     return street_stats

print quantify_street_types(process_map(OSMFILE,False))
