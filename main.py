#!/usr/bin/env python3


import re
from sys import stdin
import  grequests 


# pip install grequests

# IDEA: OPTIONS TO:
#   APPEND SOME STRING
#   SET TIMEOUT LIMIT
#   VERBOSE MODE
# check if package.json or package-lock.json already exists in the url
# dependencies and devdependencies 

lines = stdin.readlines()

if not len(lines):
    print("Please, provide the urls/domains in stdin!")
    exit(0)

obj_lines = {}
async_req_list = []

print("Requesting to target")
# async request
for i in range(len(lines)):
    line = lines[i]
    obj_lines[i] = {}
    # [0]protocol [1]domain [2]path
    s = re.search("^(https?\:\/\/)?(.+?)(\/.*)?$", line)
    
    if not s:
        obj_lines[i]["valid"] = False
        continue

    obj_lines[i]["valid"] = True

    # unless specified http, it is going to be https
    obj_lines[i]["protocol"] = "https://"
    
    if s.group(1):
        obj_lines[i]["protocol"] = s.group(1)
    
    obj_lines[i]["domain"] = s.group(2)

    obj_lines[i]["path"] = "/"
    if s.group(3):
        obj_lines[i]["path"] = s.group(3)
    
    url = obj_lines[i]["protocol"] + obj_lines[i]["domain"] + obj_lines[i]["path"] + ("/" if obj_lines[i]["path"][-1] != "/" else "")

    async_req_list.append(grequests.get(url + "package.json", timeout=5))
    async_req_list.append(grequests.get(url + "package-lock.json", timeout=5))
    # j = package.json()
    # if j:
    #r.close()

# wait for all the responses
npm_res_list = grequests.map(async_req_list)

# loop through the responses and check if they are valid package or package-lock files
# and if they do, send a request using npm api checking if all the packages exists
# if the packages doesn't exist, we have a possible depencency confusion
all_json_res = []
checked_pkgs = [] # avoid request more than once the package
async_npm_req_list = []


print("Requesting to npm")
for i in range(len(npm_res_list)):
    
    res  = npm_res_list[i]
    json_res = {}
    is_json = False
    try:
        json_res = res.json()
        is_json = True
    except:
        is_json = False

    if not is_json == True or not len(json_res) > 0 or json_res == {}:
        continue   

    all_json_res.append(json_res)
    # OK, here we have a valid json
    # but is it really what we want?
    

    if "devDependencies" in json_res or "dependencies" in json_res: # package-lock.json
        for x in json_res:
            x = str(x)
            if x in ["devDependencies", "dependencies"]:
                for pkg in json_res[x]:
                    # print(pkg)
                    if pkg not in checked_pkgs:
                        checked_pkgs.append(pkg)
                        async_npm_req_list.append(grequests.get("https://registry.npmjs.org/" + pkg, timeout=10))
                    else:
                        # if verbose then print already included + pkg
                        continue 
            
            continue
            #
    

# wait for the response of npm
npm_res_list = grequests.map(async_npm_req_list)
print(npm_res_list)
for r in npm_res_list:
    if r and r.status_code != 200:
        print("We have something! " + str(r.url))
    else:
        print("Valid " + r.url)
