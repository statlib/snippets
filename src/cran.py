import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import os
import zipfile

# URL of the index page
url = "https://cran.r-project.org/bin/windows/contrib/4.3"

# Make a request to the website
r = requests.get(url)
r.raise_for_status()

# Parse the HTML of the page
soup = BeautifulSoup(r.text, 'html.parser')

# Find all <a> tags, which represent links
links = soup.find_all('a')

# Packages
pkgs = [
    'cellWise',
    'ggrepel',
    'glmmTMB',
    'htmltools',
    'lme4',
    'marginaleffects',
    'mrfDepth',
    'polyCub',
    'robustlmm',
    'rstan',
    'sampling',
    'slider',
    'sp',
    'spam',
    'spatstat.explore',
    'spatstat.geom',
    'spatstat.linnet',
    'spatstat.model',
    'spatstat.random',
    'spatstat.sparse',
    'spatstat.utils',
    'svglite',
    'testthat',
    'utf8',
    'warp',
    'wk'
]

# Filter the links to only .zip files
zip_links = [link.get('href') for pkg in pkgs for link in links if link.get('href').endswith('.zip') and link.get('href').split("_")[0] == pkg]

# Now we can download each of the .zip files
for zip_link in tqdm(zip_links):
    # Combine the base URL with the specific zip link
    zip_url = os.path.join(url, zip_link)
    
    # Make a request to download the .zip file
    r = requests.get(zip_url)
    r.raise_for_status()
    
    # Save the content of the request to a .zip file
    with open(zip_link, 'wb') as f:
        f.write(r.content)

