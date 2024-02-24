import argparse
import json
from tld import get_fld
from urllib.parse import urlparse


def read_harfile(harfile_path):
    harfile = open(harfile_path, encoding="utf-8")
    harfile_json = json.loads(harfile.read())
    i = 0
    unique_third_party_domains = []
    urls = []
    content_types = []
    for entry in harfile_json['log']['entries']:
        i = i + 1
        url = entry['request']['url']
        content_type = entry['response']['content']['mimeType'] 
        # scripts will have 'javascript' inside content type
        # images will have 'image' inside content type
        # print (get_fld(url))
        #if get_fld(url) not in unique_third_party_domains and get_fld(url) :
        #    unique_third_party_domains.append(get_fld(url))
        #    print (get_fld(url))
        urls.append(url)
        content_types.append(content_type)

    return urls, content_types
        # print (url, content_type)

def read_json(json_file):
    json_file = open(json_file, encoding='utf-8')
    json_load = json.loads(json_file.read())

    blocked_urls = []
    types_dict = json_load['categories']
    for k, companies_list in types_dict.items():
        #print (k)
        for company_dict in companies_list:
            for company_name, company_urls in company_dict.items():
                for company_main_url, co_url_list in company_urls.items():
                    if get_fld(company_main_url, fail_silently=True) == None:
                        blocked_urls.append(company_main_url)
                    else:                   
                        blocked_urls.append(get_fld(company_main_url))
                    for url in co_url_list:
                        if get_fld(url, fail_silently=True) == None:
                            blocked_urls.append(url)
                        else:                   
                            blocked_urls.append(get_fld(url))

    #print (blocked_urls)
    return blocked_urls

def display_number_unique_urls(urls, not_included_url):
    seen_urls = []
    for url in urls:
        url_fld = get_fld(url, fail_silently=True)
        if url_fld not in seen_urls and url_fld != not_included_url and url_fld != None:
            seen_urls.append(url_fld)
            #print (url_fld)
        elif url not in seen_urls and url != not_included_url and url_fld == None:
            #print(url)
            seen_urls.append(url)
            pass
                    
    print (len(seen_urls), "out of", len(urls))
    return seen_urls

def display_number_unique_urls_2(urls_0, urls_1, not_included_url_0, not_included_url_1):
    seen_urls = []
    for url in urls_0:
        url_fld = get_fld(url, fail_silently=True)
        if url_fld != None and url_fld not in seen_urls and url_fld != not_included_url_0:
            seen_urls.append(url_fld)
        elif url_fld == None and url not in seen_urls and url != not_included_url_0:
            seen_urls.append(url_fld)
            pass
            #print(url)

    for url in urls_1:
        url_fld = get_fld(url, fail_silently=True)
        if url_fld != None and url_fld not in seen_urls and url_fld != not_included_url_1:
            seen_urls.append(url_fld)
        elif url_fld == None and url not in seen_urls and url != not_included_url_1:
            seen_urls.append(url_fld)
            #print(url)
            pass

    print (len(seen_urls), "out of", len(urls_0)+len(urls_1))
    return seen_urls

def display_number_common_values(urls_0, urls_1, combined=False):
    common_urls = []
    for url_i in urls_0:
        for url_j in urls_1:
            if url_i == url_j and url_i not in common_urls:
                common_urls.append(url_i)
                #print (url_i)

    if combined:
        print (len(common_urls), "out of", len(urls_0)+len(urls_1))
    else:
        print (len(common_urls), "out of", len(urls_0))


def display_number_common_values_2(full_urls_0, urls_1, combined=False):
    common_urls = []
    for url_i in full_urls_0:
        for url_j in urls_1:
            fld_url_i = get_fld(url_i, fail_silently = True)
            if fld_url_i == url_j: # and url_i not in common_urls:
                common_urls.append(url_i)
                break
                #print (url_i)

    if combined:
        print (len(common_urls), "out of", len(full_urls_0)+len(urls_1))
    else:
        print (len(common_urls), "out of", len(full_urls_0))

macys_urls, macys_content_types = read_harfile('www.macys.com.har')
cnn_urls, cnn_content_types = read_harfile('www.cnn.com.har')
combined_urls = macys_urls + cnn_urls
print("2")
print("a")
print("Number of unique domains third-party while visiting Macy's")
unique_macys_urls = display_number_unique_urls(macys_urls, 'macys.com')
print()

print("Number of unique third-party domains while visiting CNN")
unique_cnn_urls = display_number_unique_urls(cnn_urls, 'cnn.com')
print()

print("Number of unique third-party domains across both CNN and Macy's")
unique_combined_urls = display_number_unique_urls_2(cnn_urls, macys_urls, 'cnn.com', 'macys.com')

print()

print("b")
print("Number of common unique third-party domains across CNN and Macy's")
display_number_common_values(unique_macys_urls, unique_cnn_urls, True)

print()

blocked_urls = read_json('disconnect.json')

print("c")
print("Number of requests blocked when accessing Macy's")
display_number_common_values_2(macys_urls, blocked_urls)
print()
print("Number of reqeusts blocked when accessing CNN")
display_number_common_values_2(cnn_urls, blocked_urls)
print()
print("Number of requests blocked when accessing both")
display_number_common_values_2(combined_urls, blocked_urls)
