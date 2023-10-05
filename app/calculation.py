# Import
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from bs4 import BeautifulSoup, Tag
import time
from pathlib import Path
from shutil import rmtree
from PIL import Image
import urllib.request
from zipfile import ZipFile
import uuid

chromedriverPATH = 'C:\\Users\ASUS\AppData\Local\Programs\Python\Python39\chromedriver.exe'


def calculate(baseUrl: str):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Hides the browser window
    driver = webdriver.Chrome(
        options=chrome_options)
    driver.get(baseUrl)
    time.sleep(8)
    htmltext = driver.page_source
    soup = BeautifulSoup(htmltext, "lxml")
    images = soup.find_all("img", {"class": "thumbnail-image"})
    paths = []
    for item in images:
        if "BigBlueButton" not in item.get("alt"):
            paths.append(baseUrl.split("playback")[
                0][:-1]+'/'.join(item.get("src").split("/")[:-2]))
    newPaths = list(dict.fromkeys(paths))
    # with open("paths.txt", "w") as foo:
    #     foo.write('\n'.join(newPaths))
    newPaths = newPaths[:2]
    for path in newPaths:
        print("Main")
        x = 1
        while True:
            z = "%s/slide-%s.png" % (path, str(
                x))
            try:
                urllib.request.urlretrieve(z, "app/images/%s.png" % str(x))
                print("Cycle-1  ", x)
                x += 1
                continue
            except:
                break
        output = []
        for i in range(1, x):
            if i != 1:
                image = Image.open("app/images/%s.png" % str(i))
                output.append(image.convert('RGB'))
            print("Cycle-2  ", i)
        image = Image.open("app/images/1.png")
        image.save(r'app/result/%s.pdf' % str(newPaths.index(path)+1),
                   save_all=True, append_images=output)
        print("image saved!")
        for file in Path("app/images").glob("**/*"):
            if file.is_file():
                file.unlink()
            elif file.is_dir():
                rmtree(file)

        print("path deleted!")
    driver.quit()
    zipName=str(uuid.uuid4())
    zipObj = ZipFile('data/%s.zip'%zipName, 'w')
    for index in range(len(newPaths)):
        zipObj.write('app/result/%s.pdf' % str(index+1))
    zipObj.close()
    for file in Path("app/result").glob("**/*"):
        if file.is_file():
            file.unlink()
        elif file.is_dir():
            rmtree(file)
    return zipName
    # return len(newPaths)
calculate("https://class17.ui.ac.ir/playback/presentation/2.3/d54d2447a0da358e7946fe142a96658a91b982bf-1649496305040")