import argparse
import json
from tld import get_fld
from urllib.parse import urlparse
from adblockparser import AdblockRules

CONTENT_TYPE_INDEX = 1
URL_INDEX = 0

def read_harfile(harfile_path):
    harfile = open(harfile_path, encoding="utf-8")
    harfile_json = json.loads(harfile.read())
    i = 0
    unique_third_party_domains = []
    #urls = []
    #content_types = []

    return_list = []
    for entry in harfile_json['log']['entries']:
        url_content_list = []
        i = i + 1
        url = entry['request']['url']
        content_type = entry['response']['content']['mimeType'] 
        # scripts will have 'javascript' inside content type
        # images will have 'image' inside content type

        url_content_list.append(url)
        url_content_list.append(content_type)
        return_list.append(url_content_list)

    return return_list


def is_script_func(content_type):
    return_val = False
    if content_type.find('javascript') != -1:
        return_val = True
    else:
        return_val = False

    return return_val

def is_image_func(content_type):
    return_val = False
    if content_type.find('image') != -1:
        return_val = True
    else:
        return_val = False

    return return_val

def is_third_party_func(url, first_party_url):
    return_val = False
    if get_fld(url, fail_silently=True) != first_party_url:
        return_val = True
    else:
        return_val = False

    return return_val


def num_blocked_by_request(filter_rules, cnn_urls_content_types, first_party_url, domain):
    rules = AdblockRules(filter_rules)
    num_blocked = 0
    total = 0
    for url_content_type in cnn_urls_content_types:
        url = url_content_type[URL_INDEX]
        content_type = url_content_type[CONTENT_TYPE_INDEX]
        is_script = is_script_func(content_type)
        is_image = is_image_func(content_type)
        is_third_party = is_third_party_func(url, first_party_url)
        if domain == None:
            if rules.should_block(url, {'script': is_script, 'third-party': is_third_party, 'image': is_image}):
                num_blocked = num_blocked + 1
                #print (url, content_type)

        else:
            if rules.should_block(url, {'script': is_script, 'third-party': is_third_party, 'image': is_image, 'domain': domain}):
                num_blocked = num_blocked + 1
                #print (url, content_type)
        total = total + 1
    print (num_blocked, 'out of', total)

def display_num_unique_content_types(url_content_types):
    unique_types = []
    for url_content_type in url_content_types:
        if url_content_type[CONTENT_TYPE_INDEX] not in unique_types:
            #print (url_content_type[CONTENT_TYPE_INDEX])
            unique_types.append(url_content_type[CONTENT_TYPE_INDEX])
    
cnn_url_content_types = read_harfile('www.cnn.com.har')

print("3")

print("a")
print("Number requests blocked for containing ‘cookie-sync?’ string ")
num_blocked_by_request(['cookie-sync?'], cnn_url_content_types, 'cnn.com', None)

print()
print("b")
print("Number requests blocked for loading any image (e.g., jpg, gif etc.) from  px.moatads.com  ")
num_blocked_by_request(['||px.moatads.com^$image'], cnn_url_content_types, 'cnn.com', None)

print()
print("c")
print("Number requests blocked for loading any script from  scorecardresearch.com  ")
num_blocked_by_request(['||scorecardresearch.com^$script'], cnn_url_content_types, 'cnn.com', None)





