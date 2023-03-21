import browser_cookie3
import requests
from urllib.request import urlretrieve

import os
from pathlib import Path

script_dir = Path(__file__).parent
output_dir = script_dir / "output"
cookiejar = browser_cookie3.firefox(domain_name='ifunny.co')
print(cookiejar)

x_csrf_token = None

for cookie in cookiejar:
    if cookie.name == "x-csrf-token":
        x_csrf_token = cookie.value

if not x_csrf_token:
    raise Exception("x_csrf_token cookie not found")

headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "content-type": "application/json",
    "Host": "ifunny.co",
    "Pragma": "no-cache",
    "Referer": "https://ifunny.co/account/smiles",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "same-origin",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0", #!
    "x-csrf-token": x_csrf_token, #!
    "x-requested-with": "fetch",
}


#https://ifunny.co/api/v1/account/smiles?next=1678975992.919

def load_urls_from_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read().splitlines()
    except:
        print(f"File doesn't exist: {filename}")
        return []


def get_items(url):
    urls = []
    res = requests.get(url, cookies=cookiejar, headers=headers)
    print(res)
    #print(res.json())

    json_res = res.json()
    next_token = json_res.get("pagination").get("next")

    for item in json_res.get("items"):
        url = item.get("url")
        urls.append(url)
        print(url)

    print(len(json_res.get("items")), "items")
    print(json_res.get("pagination"))
    print("next:", next_token)

    return urls, next_token


def write_urls_to_file(filename, urls):
    with open(filename, 'w') as file:
        file.writelines(
            url + "\n"
            for url in urls
        )

def append_urls_to_file(filename, urls):
    with open(filename, 'a') as file:
        file.writelines(
            url + "\n"
            for url in urls
        )


def append_url_to_file(filename, url):
    with open(filename, 'a') as file:
        file.write(url + "\n")




def main():
    current_urls_set = set(load_urls_from_file(script_dir / "urls.txt"))
    next_id = len(current_urls_set) + 1

    print(f"Current urls: {len(current_urls_set)}")
    print(f"Next ID: {next_id}")

    output_dir.mkdir(parents=True, exist_ok=True)

    new_item_urls = []

    base_url = "https://ifunny.co/api/v1/account/smiles?next="
    next_token=" "
    next_url = base_url

    while next_token:
        urls, next_token = get_items(next_url)
        next_url = base_url + next_token

        for url in urls:
            # Don't continue if we're starting to see duplicates
            if url in current_urls_set:
                next_token = None
            else:
                new_item_urls.append(url)


    ### Download newly found items

    print(f"Found {len(new_item_urls)} new items")

    for new_url in reversed(new_item_urls):
        url_filename = new_url.split("/")[-1]
        dst = output_dir / f"{next_id} {url_filename}"
        print(f"Downloading {new_url} as {dst}")
        urlretrieve(new_url, dst)

        append_url_to_file("urls.txt", new_url)
        next_id += 1



if __name__ == "__main__":
    main()















