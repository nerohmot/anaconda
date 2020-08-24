# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:56:40 2020

@author: hoeren
"""
import requests
from bs4 import BeautifulSoup, element
import subprocess    

url = 'https://docs.anaconda.com/anaconda/packages/py3.7_linux-64/'

html_content = requests.get(url).text
soup = BeautifulSoup(html_content, 'lxml')
table = soup.find_all('table')[0]
packages = {}

def find_in_conda_forge(package, version):
    line = f'conda search -c conda-forge {package}=={version}'
    process = subprocess.Popen(line.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)    


for package in table.find_all('tr'):
    attribute_marker = 0
    attributes = package.find_all('td')
    for attribute in attributes:
        if attribute_marker == 0:  # name
            package_name = attribute.get_text()
        if attribute_marker == 1:  # version
            package_version = attribute.get_text()
        if attribute_marker == 2:  # description
            package_description = attribute.get_text()
        if attribute_marker == 3:  # in installer
            if len(attribute.contents)>0:
                packages[package_name] = package_version
        attribute_marker += 1

cnt = 0
for package_name in packages:
    package_version = packages[package_name]
    print(f'{package_name}=={package_version} ... ', end='')
    find_in_conda_forge(package_name, package_version)
    cnt +=1
    
print(f'{cnt} packages')