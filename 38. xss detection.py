#!/usr/bin/env python3

# Author:      Abdou Rockikz
# Comments by: Paul Stroud
# Description: TODO: Add description 
# Date:        TODO: Add date
# Modified by: TODO: Add your name

### TODO: Install requests bs4 before executing this in Python3

# Import libraries

import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

# Declare functions

# parses html code to extract and return all forms
def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser") # grab the html using HTTP requests lib, then parse it with bs
    return soup.find_all("form")    # return the list of all forms

# parses the form and returns a dictionary containing its properties
def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

# submits a string to the specific form on the page
### In your own words, describe the purpose of this function as it relates to the overall objectives of the script ###
def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

# scans a url for XSS vulnerabilities
def scan_xss(url):
    forms = get_all_forms(url)  # get a lit of forms on the page
    print(f"[+] Detected {len(forms)} forms on {url}.")
    js_script = '<script>alert="the matrix has you</script>"' # XSS script to inject
    is_vulnerable = False       # initialize the return var
    for form in forms:          # iterate over the list
        form_details = get_form_details(form)   # get the form handle
        content = submit_form(form_details, url, js_script).content.decode()    # try to inject the script, then save the result
        if js_script in content:    # if it contains the injected script
            print(f"[+] XSS Detected on {url}") # alert the user
            print(f"[*] Form details:")
            pprint(form_details)        # pretty print info about the vulnerable form
            is_vulnerable = True        # set the return var
    return is_vulnerable    # return the result (T/F)

# Main

if __name__ == "__main__":
    url = input("Enter a URL to test for XSS:") 
    print(scan_xss(url))    # scan url for XSS and print the results 

### TODO: When you have finished annotating this script with your own comments, copy it to Web Security Dojo
### TODO: Test this script against one XSS-positive target and one XSS-negative target
### TODO: Paste the outputs here as comments in this script, clearling indicating which is positive detection and negative detection
