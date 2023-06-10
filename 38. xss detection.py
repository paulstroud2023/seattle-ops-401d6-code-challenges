#!/usr/bin/python3

# Author:      Abdou Rockikz
# Description: python scanner for XSS vulnerabilities
# Date:        06/09/2023
# Comments by: Paul Stroud

### Install requests bs4 before executing this in Python3

# Import libraries
import requests                         # for HTTP requests
from pprint import pprint               # pretty print for complex output
from bs4 import BeautifulSoup as bs     # for parsing HTML
from urllib.parse import urljoin        # for crafting URLs

# Declare functions

# parses html code to extract and return all forms
def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser") # grab the html using HTTP requests lib, then parse it with bs
    return soup.find_all("form")    # return the list of all forms

# parses the form and returns a dictionary containing its properties
def get_form_details(form):
    details = {}        # initialize the dictionary
    action = form.attrs.get("action").lower()           # get "action" attribute of the form, convert to lowercase
    method = form.attrs.get("method", "get").lower()    # get "method" attribute of the form, convert to lowercase
    inputs = []         # initialize the list
    for input_tag in form.find_all("input"):                        # make a list of all inputs in the form and iterate over it
        input_type = input_tag.attrs.get("type", "text")            # get "type" or "text" attrs of the input field
        input_name = input_tag.attrs.get("name")                    # get the "name" attr of the input
        inputs.append({"type": input_type, "name": input_name})     # add the type/name to the list as a dictionary element
    # populate the dictionary
    details["action"] = action          
    details["method"] = method
    details["inputs"] = inputs
    return details      # return the dictionary

# submits a string to the specific form on the page
def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])   # make the target URL
    inputs = form_details["inputs"]                     # get the list of inputs
    data = {}                                           # initialize the data dict
    for input in inputs:                                # iterate over the list
        if input["type"] == "text" or input["type"] == "search":    # if the field is "text"/"search"
            input["value"] = value                      # enter the value
        input_name = input.get("name")                  # save the input name
        input_value = input.get("value")                # save the input value
        if input_name and input_value:                  # if both vars are non-zero
            data[input_name] = input_value              # add a dict entry

    if form_details["method"] == "post":                # if HTTP POST request
        return requests.post(target_url, data=data)     # craft and return a POST request
    else:
        return requests.get(target_url, params=data)    # craft and return a GET request

# scans a url for XSS vulnerabilities
def scan_xss(url):
    forms = get_all_forms(url)                          # get a list of forms on the page
    print(f"[+] Detected {len(forms)} forms on {url}.")
    js_script = '<script>alert="the matrix has you</script>"' # XSS script to inject
    is_vulnerable = False                               # initialize the return var
    for form in forms:                                  # iterate over the list
        form_details = get_form_details(form)           # get the form handle
        content = submit_form(form_details, url, js_script).content.decode()    # try to inject the script, then save the result
        if js_script in content:                        # if it contains the injected script
            print(f"[+] XSS Detected on {url}")         # alert the user
            print(f"[*] Form details:")
            pprint(form_details)                        # pretty print info about the vulnerable form
            is_vulnerable = True                        # set the return var
    return is_vulnerable                                # return the result (T/F)

# Main

if __name__ == "__main__":
    url = input("Enter a URL to test for XSS:") 
    print(scan_xss(url))    # scan url for XSS and print the results 

### TODO: When you have finished annotating this script with your own comments, copy it to Web Security Dojo
### TODO: Test this script against one XSS-positive target and one XSS-negative target
### TODO: Paste the outputs here as comments in this script, clearling indicating which is positive detection and negative detection
