#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
The output should be a dictionary with the tag name as the key
and number of times this tag can be encountered in the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""


#### MMP: This code is amended from the original task to analyse the data for Bogota.
import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict
import re

street_type_re = re.compile(r'\S+\.?\b', re.IGNORECASE)  #amended from original to apply to Bogota

filename="bogota_colombia.osm"


expected=["Carrera","Calle","Avenida","Diagonal","Transversal","Autopista"]  #amended from original to apply to Bogota


def count_tags(filename):
        tree= ET.parse(filename)
        root=tree.iter()
        tag_stat={}
        for item in root:
            if not item.tag in tag_stat:
               tag_stat[item.tag]=1
            else:
                tag_stat[item.tag] +=1
        return tag_stat
        # YOUR CODE HERE

print count_tags(filename)

def audit_street_type(street_types, street_name,street_stats):
    m = street_type_re.search(street_name)
    #street_stats={}
    #for item in expected:
     #       street_stats[item]=0
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
        else:
            if street_type not in street_stats:
                    street_stats[street_type]=0
            else:
                street_stats[street_type]+=1
    return street_stats

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)

    for item in expected:
            street_stats[item]=0
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                   audit_street_type(street_types, tag.attrib['v'], street_stats)
    pprint.pprint(dict(street_types))
    
   # return street_types

print (audit(filename))







