import requests
# import shutil
import urllib
import os

url = input("Enter the URL of the manga: ")
# url = "https://api.mangadex.org/at-home/server/f3fe6db4-916c-404b-8b26-4eb24981d5e7?forcePort443=false"
mangaUrl = input("Enter the URL of the manga info: ")
# mangaUrl = "https://api.mangadex.org/chapter/f3fe6db4-916c-404b-8b26-4eb24981d5e7?includes[]=scanlation_group&includes[]=manga&includes[]=user"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
mangaResponse = requests.request("GET", mangaUrl, headers=headers, data=payload)

data = response.json()
mangaData = mangaResponse.json()

baseUrl = data['baseUrl']
pageData = data["chapter"]["data"]
hashParam = data["chapter"]["hash"]
mangaName = mangaData["data"]["relationships"][1]["attributes"]["title"]["en"]
mangaVol = mangaData["data"]["attributes"]["volume"]

if mangaVol:
    path = mangaName + "/vol-" + mangaVol
    os.makedirs(path, exist_ok=True)
else:
    path = mangaName
    os.makedirs(path, exist_ok=True)

for i in range(len(pageData)):
    url = f"{baseUrl}/data/{hashParam}/{pageData[i]}"
    print(url)

    # response = requests.request("GET", url, headers=headers, data=payload)

    # response = requests.get(url, stream=True)
    # with open(f"./example/page{i}.png", 'wb') as out_file:
    #     shutil.copyfileobj(response.raw, out_file)
    # del response
    if mangaVol:
        urllib.request.urlretrieve(url, f"./{path}/page-{i+1}.png")
    else:
        urllib.request.urlretrieve(url, f"./{path}/page-{i+1}.png")
