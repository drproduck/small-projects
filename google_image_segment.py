#!/usr/bin/env python

"""Get an image from google, then segment it
"""

from lxml import html
import requests
# import cv2
from PIL import Image
from io import BytesIO
import numpy as np
from sklearn.feature_extraction import image
from sklearn.cluster import spectral_clustering
import scipy.sparse as sp
import matplotlib.pyplot as plt
from kernel import *

from bs4 import BeautifulSoup
import re
from urllib.request import urlopen, Request
import os
import json


def get_xpath_from_tree(html_tree, xpath_pat):
    elements = html_tree.xpath(xpath_pat)

    return elements

def get_img_from_url(url):
    resp = requests.get(url)
    img = Image.open(BytesIO(resp.content))

    return img

def get_html_tree(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    return tree

def get_affinity_matrix(img, d=3):
    if d == 3:
        d1,d2,d3 = img.shape
        pixels = img.reshape(d1*d2, d3)
        sigma = get_sigma(pixels)
        mat = gaussianize(pixels, sigma=sigma)
    else:
        d1,d2 = img.shape
        pixels = img.reshape(d1*d2, 1)
        sigma = pixels.std()
        mat = gaussianize(pixels, sigma=sigma)

    print('sigma', sigma)

    return mat
def get_soup(url,header):
    return BeautifulSoup(urlopen(Request(url,headers=header)),'html.parser')


query = input("query image ")# you can change the query for the image here
print('query: ', query)
image_type="ActiOn"
query= query.split()
query='+'.join(query)
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
print(url)
#add the directory for your image here
DIR="Pictures"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
soup = get_soup(url,header)


ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))

print("there are total" , len(ActualImages),"images")

img_large = get_img_from_url(ActualImages[0][0])

print('original image size: ',img_large.size)
reduce_ratio = 0.07
# img_large = img_large.resize((int(img_large.size[0]*reduce_ratio), int(img_large.size[1] * reduce_ratio)))
img_large = img_large.resize((50, 50))

plt.tight_layout()
fig, ax = plt.subplots(1,3)
ax[0].imshow(img_large)
ax[0].set_title('original image')

imarr = np.array(img_large)

# grayscale, keeping full colors don't really work
imarr = 0.2989 * imarr[:,:,0] + 0.5870 * imarr[:,:,1] + 0.1140 * imarr[:,:,2]

print(imarr.shape)
# d1, d2, d3 = imarr.shape
d1, d2 = imarr.shape
imaffmat = get_affinity_matrix(imarr, 2)
print(imaffmat.shape)

n_clusters = 4
labels = spectral_clustering(imaffmat, n_clusters=n_clusters, eigen_solver='arpack')

label_im = labels.reshape((d1, d2))
ax[1].imshow(label_im)
ax[1].set_title('segmentation ({})'.format(n_clusters))

ax[2].imshow(imarr)
ax[2].set_title('gray scale')

plt.show(block=True)


