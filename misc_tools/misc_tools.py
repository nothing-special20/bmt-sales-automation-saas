from pathlib import Path
import re
import shutil
import os
import sys

import requests
import json
import pandas as pd

from googlesearch import search

BMT_DATA_FOLDER = os.getenv('BMT_DATA_FOLDER')
BMT_SALES_AUTOMATION_SAAS = os.path.dirname(os.path.normpath(BMT_DATA_FOLDER)) + '/bmt-sales-automation-saas/'
SPYFU_FOLDER = BMT_SALES_AUTOMATION_SAAS + 'spyfu/'

def extract_static_path(x):
    if ('% static' in x):
        output = re.findall("'.{1,255}?'", x)[0]
        output = re.sub("'", "", output)
        return output
    else:
        return x

# copy all of the file dependencies for a file from one folder to another
def copy_dependencies(file, src_folder, dest_folder):
    data = open(file, 'r').read()
    file_paths = re.findall('".{1,255}?"', data)
    file_paths = [re.sub('"', '', x) for x in file_paths]
    keep_file_exts = ['.css', '.js', '.svg', '.png']
    keep_file_exts = ['\\' + x for x in keep_file_exts]
    keep_file_exts = '|'.join(keep_file_exts)
    # print(extract_static_path("% static 'js/sb-admin-2.min.js' %}"))
    
    file_exts = []
    for x in file_paths:
        try:
            file_exts.append(re.search('\\..{1,5}',x).group(0))
        except:
            pass

    file_exts = list(set(file_exts))

    file_paths = [x for x in file_paths if bool(re.findall(keep_file_exts, x))]
    file_paths = [x for x in file_paths if x[0]!='.']
    file_paths = [extract_static_path(x) for x in file_paths]
    file_paths = [x for x in file_paths if 'custom' not in x]

    file_paths = [re.sub('vendor/bulkit', '', x) for x in file_paths]

    # for x in file_paths:
    #     print(x)

    for x in file_paths:
        src = src_folder + x
        dst = dest_folder + x
        dst_subfolder = os.path.dirname(dst)
        Path(dst_subfolder).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        # try:
        #     shutil.copyfile(src, dst)
        # except:
        #     print('Err! File not found!\t' + src)

# swaps out things like href="lol.png" for href="{ % static 'lol.png' %}"
def django_static_file_ref_update(file):
    data = open(file, 'r').read()
    file_paths = re.findall('".{1,255}?"', data)
    file_paths = [re.sub('"', '', x) for x in file_paths]
    keep_file_exts = ['.css', '.js', '.svg', '.png']
    keep_file_exts = ['\\' + x for x in keep_file_exts]
    keep_file_exts = '|'.join(keep_file_exts)

    file_exts = []
    for x in file_paths:
        try:
            file_exts.append(re.search('\\..{1,5}',x).group(0))
        except:
            pass

    file_exts = list(set(file_exts))

    file_paths = [x for x in file_paths if bool(re.findall(keep_file_exts, x))]
    file_paths = [x for x in file_paths if x[0]!='.']
    file_paths = list(set(file_paths))

    for x in file_paths:
        print('~~~~~~')
        print(x)
        new_path = "{% static '" + x + "' %}"
        data = re.sub(x, new_path, data)
        print(new_path)
    
    new_file = file.split('.')
    new_file = new_file[0] + '_2.' + new_file[1]

    f = open(new_file, "w")
    f.write(data)
    f.close()

    "vendor/jquery/jquery.min.js"
    "{% static 'vendor/jquery/jquery.min.js' %}"

# https://www.spyfu.com/api/v1/core#section/Authentication
def top_domains_per_keyword(keyword):
    # keyword = re.sub(' ', '%20', str(keyword))
    print(keyword)
    querystring = {
                    "term" : keyword,
                    "api_key": "PLHPPBBM"
                }
    api_url = "https://www.spyfu.com/apis/core_api/get_term_ranking_urls_us"
    response = requests.request("GET", api_url, params=querystring)
    try:
        json_object = json.loads(response.text)
    except:
        json_object = {}

    return json_object

def spyfu_data_dump(url, data, folder=''):
    Path(folder).mkdir(parents=True, exist_ok=True)
    xpt_file = re.sub('https{0,1}://', '', url)
    xpt_file = xpt_file.split('/')
    xpt_file = folder + xpt_file[0] + '.json'
    with open(xpt_file, 'w+') as f:
        json.dump(data, f)

def domain_competitors(url):
    querystring = {
                    "domain" : str(url),
                    "isOrganic" : 'true',
                    "r" : '10',
                    "api_key": "PLHPPBBM"
                }
    api_url = "https://www.spyfu.com/apis/core_api/get_domain_competitors_us"
    response = requests.request("GET", api_url, params=querystring) #headers=headers,
    data = json.loads(response.text)
    # json_object = json.loads(data)
    # json_formatted_str = json.dumps(json_object, indent=2)

    return data

def dependency_checker(file, static_folder):
    data = open(file, 'r').read()
    dependency_files = re.findall('".{1,255}?"', data)
    dependency_files = [re.sub('"', '', x) for x in dependency_files]
    dependency_files = [os.path.basename(x) for x in dependency_files]
    dependency_files = [x.split('#')[0] for x in dependency_files if '.' in x]
    
    dependency_files = list(set(dependency_files))

    rm_file_exts = ['Microsoft\\.BasicImage', '#iefix']
    # rm_file_exts = ['\\' + x for x in rm_file_exts]
    rm_file_exts = '|'.join(rm_file_exts)

    dependency_files = [x for x in dependency_files if not bool(re.findall(rm_file_exts, x))]

    static_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(static_folder) for f in filenames]
    static_files = [os.path.basename(x) for x in static_files]

    missing_dependencies = [x for x in dependency_files if x not in static_files]

    for x in missing_dependencies:
        print(x)
    print('Files remaining to download:\t' + str(len(missing_dependencies)))

if __name__ == '__main__':
    if sys.argv[1]=='copy_files':
        # file = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-sales-automation-saas/templates/web/components/bulkit_body_old.html'
        file = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-sales-automation-saas/templates/vendor/bootstrap/surveys_body.html'
        src_folder = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/tools/themeforest-Y3pCVj8L-bulkit-agency-startup-and-saas-template/precompiled/assets/'
        dest_folder = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-sales-automation-saas/static/vendor/bulkit/'
        copy_dependencies(file, src_folder, dest_folder)
        # django_static_file_ref_update(file)

    if sys.argv[1]=='spyfu_top_domains_keyword':
        keyword = 'landscaping companies'
        data = top_domains_per_keyword(keyword)
        folder = SPYFU_FOLDER + 'landscaping/'
        spyfu_data_dump(keyword, data, folder)

    if sys.argv[1]=='spyfu_domain_competitors':
        url = 'newportavelandscaping.com'
        data = top_domains_per_keyword(url)
        folder = SPYFU_FOLDER + 'landscaping/'
        spyfu_data_dump(url, data, folder)
    
    if sys.argv[1] == 'hunter.io':
        folder = SPYFU_FOLDER + 'landscaping/'
        files = [folder + x for x in os.listdir(folder) if '.json' in x]
        final = []
        for f in files:
            json_data = json.load(open(f))['organicGrid']
            data = pd.DataFrame(json_data)
            final.append(data)

        final = pd.concat(final)
        final.to_excel(folder + 'landscaping_output.xlsx', 'data', index=None)

    if sys.argv[1] == 'dependency_check':
        file = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-sales-automation-saas/static/vendor/bulkit/css/app.css'
        static_folder = '/Users/rapple2018/Documents/Professional/Entrepreneur/Bill More Tech/bmt-sales-automation-saas/static/vendor/bulkit'
        dependency_checker(file, static_folder)