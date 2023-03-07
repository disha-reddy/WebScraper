from bs4 import BeautifulSoup
import requests
from PIL import ImageFile
import urllib
import urllib.request 
import csv
import os
import shutil

def getsizes(uri):
    # get file size *and* image size (None if not known)
    file = urllib.request.urlopen(uri)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return size, None

def image_download(image_urls, folderName):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, folderName)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    for img in image_urls:
        # We can split the file based upon / and extract the last split within the python list below:
        file_name = img.split('/')[-1]
        # Now let's send a request to the image URL:
        r = requests.get(img, stream=True)
        # We can check that the status code is 200 before doing anything else:
        if r.status_code == 200:
            # This command below will allow us to write the data to a file as binary:
            finalImageFiles = os.path.join(final_directory, file_name)
            with open(finalImageFiles, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        else:
            # We will write all of the images back to the broken_images list:
            broken_images.append(img)
    # create a zip folder for all the images
    shutil.make_archive(final_directory, 'zip', final_directory)
    

# configurable list of urls
urls = ["https://www.spigot.com/", "https://readscripture.net/", "https://earlychirp.com/", "https://living.guide/fashion/3-chic-cocktail-dresses-for-any-occasion/?utm_source=facebook&utm_medium=Facebook_Mobile_Feed&utm_campaign=23850811306770197&utm_content=fb-23851005666410197&search_term=big%20tall%20apparel"]

# list of acceptable image extensions
imageExtensions = ['jpg', 'png', 'gif']

# collect all image Urls to download
imageUrls  = []

# broken images
broken_images = []

#folder to save all images
imageFolderName = 'image_files'

# open a file and define row headers
csv_file = open('web_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['imageUrl', 'size(file, (width, height))'])

for url in urls:
    # Getting the webpage, creating a Response object.
    response = requests.get(url)

    # Extracting the source code of the page.
    data = response.text

    # Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(data, 'lxml')

    # extracting all images from source code.
    images = soup.find_all('img')
    for item in images:
        imageUrl = item['src']
        if imageUrl.split('.')[-1] in imageExtensions:
            try:
                # file size, image width, image height
                size = getsizes(imageUrl)
                imageUrls.append(imageUrl)
            except:
                size = 'url is not readable may be an ad'
            csv_writer.writerow([imageUrl, size])
# downlaod and zip all the images to a local file   
image_download(imageUrls,imageFolderName)
# print all broken images if any
for image in broken_images:
    print(image)      
csv_file.close()
