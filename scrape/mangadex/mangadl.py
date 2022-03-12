import requests
# import shutil
import urllib

url = "https://api.mangadex.org/at-home/server/8873f979-177a-498a-a40b-3481ceac4bd5?forcePort443=false"
mangaUrl = "https://api.mangadex.org/chapter/8873f979-177a-498a-a40b-3481ceac4bd5?includes[]=manga"

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

for i in range(len(pageData)):
    url = f"{baseUrl}/data/{hashParam}/{pageData[i]}"
    print(url)

    # response = requests.request("GET", url, headers=headers, data=payload)

    # response = requests.get(url, stream=True)
    # with open(f"./example/page{i}.png", 'wb') as out_file:
    #     shutil.copyfileobj(response.raw, out_file)
    # del response
    urllib.request.urlretrieve(url, f"./example/{mangaName}_{i}.png")
