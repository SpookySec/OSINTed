import requests
import webbrowser

def ReverseSearchImage(image):
    gurl='https://www.google.com/searchbyimage/upload'
    murl={'encoded_image': (image, open(image, 'rb')), 'image_content': ''}
    response = requests.post(gurl, files=murl, allow_redirects=False)
    fetchUrl = response.headers['Location']
    return fetchUrl