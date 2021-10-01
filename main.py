#!/usr/bin/env python3


import re
from sys import stdin
import grequests
import argparse

# pip install grequests
# check if package.json or package-lock.json already exists in the url

parser = argparse.ArgumentParser(description='Get subdomains from stdin and search for dependency confusion.')
parser.add_argument("-th", help="Number of concurrence threads", default=10, type=int)
parser.add_argument("-to", help="Timeout (in seconds)",  default=15, type=int, required=False)
parser.add_argument("-a", help="String to append in the end of url. E.g: -a=\"?token=foo\"",  default="", required=False)
parser.add_argument("-v", help="Verbose mode", type=int, default=0, required=False)
parser.add_argument("--version", help="Show version and exit", action="store_true")
parser.add_argument("-s", help="Silent, only shows the useful results", action="store_true")
parser.add_argument("-link", help="Show full link to the npm possible vulnerable package", action="store_true")

args = parser.parse_args()
user_input = vars(args)



def sprint(message, require_verbose:int = 0):
    if user_input["s"] == True:
        return
    if user_input["v"] >= require_verbose:
        print(message)
sprint(user_input, 3)

if user_input["version"]:
    sprint("version 0.1", 0)
    exit(0)


if stdin.isatty():
    sprint("Error, you must provide subdomains in stdin")
    exit()

lines = stdin.readlines()

def send_async_request(urls: list, threads: int = 10, timeout:int = 15):
    all_responses = []
    req_list_for_threads = []

    for i in range(len(urls)):
        cr = grequests.get(urls[i], timeout=timeout/10)
        req_list_for_threads.append(cr)

        sprint(cr.url, 2)
        # every time the number of request reches the concurret threads limit, 
        # it is going to send and wait for the response, and only then send more requests
        if i % threads == 0 or len(urls) == i - 1:
            res_list = grequests.map(req_list_for_threads)
            req_list_for_threads = []
            # saving the batch of request this to one array
            for res in res_list:
                all_responses.append(res)

    return all_responses


if not len(lines):
    print("Please, provide the urls/domains in stdin!")
    exit(0)

obj_lines = {}
target_url_list = []


# async request
for i in range(len(lines)):
    line = lines[i]
    obj_lines[i] = {}
    # [0]protocol [1]domain [2]path
    s = re.search("^(https?\:\/\/)?(.+?)(\/.*)?$", line)

    if not s:
        sprint("Invalid url provided! " + line, 3)
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

    url = obj_lines[i]["protocol"] + obj_lines[i]["domain"] + \
        obj_lines[i]["path"] + ("/" if obj_lines[i]["path"][-1] != "/" else "")
    
    target_url_list.append(url + "package.json" + str(user_input["a"]))
    target_url_list.append(url + "package-lock.json" + str(user_input["a"]))

sprint("Sending requests to the target")
target_res_list = send_async_request(target_url_list, user_input["th"], user_input["to"])

# loop through the responses and check if they are valid package or package-lock files
# and if they do, send a request using npm api checking if all the packages exists
# if the packages doesn't exist, we have a possible depencency confusion
all_json_res = []
checked_pkgs = []  # avoid request more than once the package
checked_pkgs_links = []
async_npm_req_list = []

for i in range(len(target_res_list)):

    res = target_res_list[i]
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

    if "devDependencies" in json_res or "dependencies" in json_res:  # package-lock.json
        for x in json_res:
            x = str(x)
            if x in ["devDependencies", "dependencies"]:
                for pkg in json_res[x]:
                    # print(pkg)
                    if pkg not in checked_pkgs:
                        checked_pkgs.append(pkg)
                        checked_pkgs_links.append("https://registry.npmjs.org/"+pkg)

                    else:
                        sprint("PACKAGE ALREDY INCLUDED " + pkg, 3)
                        # if verbose then print already included + pkg
                        continue

            continue
            #

if not len(checked_pkgs):
    sprint("No package file was found.")


sprint("Sending requests to NPM api")
npm_res_list = send_async_request(checked_pkgs_links,  user_input["th"], user_input["to"])

for r in npm_res_list:
    if r.status_code != 200:
        print(str(r.url) if user_input["link"] else str(r.url).replace("https://registry.npmjs.org/", ""))
