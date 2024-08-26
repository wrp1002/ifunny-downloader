import browser_cookie3
import requests
from urllib.request import urlretrieve

import os
import webbrowser
from pathlib import Path

script_dir = Path(__file__).parent
output_dir = script_dir / "output"


class iFunnyAPI:
    def __init__(self):
        self.cookies = self.get_cookies_from_browser()
        self.x_csrf_token = self.get_csrf_from_cookies()
        self.headers = {
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
            "x-csrf-token": self.x_csrf_token, #!
            "x-requested-with": "fetch",
        }

    def get_cookies_from_browser(self):
        return browser_cookie3.firefox(domain_name='ifunny.co')

    def update_from_browser(self):
        self.cookies = self.get_cookies_from_browser()
        self.x_csrf_token = self.get_csrf_from_cookies()
        self.headers["x-csrf-token"] = self.x_csrf_token

    def session_valid(self):
        res = requests.get("https://ifunny.co/account/smiles", cookies=self.cookies, headers=self.headers, allow_redirects=False)
        print(f"Got status: {res.status_code}")
        return res.status_code == 200

    def get_csrf_from_cookies(self):
        print("Getting x_csrf-token")
        for cookie in self.cookies:
            print(cookie)
            if cookie.name == "x-csrf-token":
                print("Found!")
                return cookie.value
        print("Not found")
        return None

    def wait_for_valid_session(self):
        print("Checking for valid session...")
        while not self.session_valid():
            print("session not valid. try logging in first")
            webbrowser.open("https://ifunny.co/account/smiles")
            input("Press enter to continue...")
            self.update_from_browser()
        print("Looks good!")

    def get_items(self, url):
        urls = []
        res = requests.get(url, cookies=self.cookies, headers=self.headers)
        #print(res)
        #print(res.json())

        json_res = res.json()
        next_token = json_res.get("pagination", {}).get("next", "")

        for item in json_res.get("items", []):
            url = item.get("url")
            urls.append(url)
            print(url)

        print(len(json_res.get("items", [])), "items from this page")
        print(json_res.get("pagination"))
        print("Next token:", next_token)

        return urls, next_token


#https://ifunny.co/api/v1/account/smiles?next=1678975992.919

def load_urls_from_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read().splitlines()
    except:
        print(f"File doesn't exist: {filename}")
        return []

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
    ifunny = iFunnyAPI()
    ifunny.wait_for_valid_session()
    print()

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
        urls, next_token = ifunny.get_items(next_url)
        next_url = base_url + next_token

        for url in urls:
            # Don't continue if we're starting to see duplicates
            if url in current_urls_set:
                next_token = None
            else:
                new_item_urls.append(url)


    ### Download newly found items

    print(f"\nFound {len(new_item_urls)} new items")
    if new_item_urls:
        print("Downloading them now...")

    for new_url in reversed(new_item_urls):
        url_filename = new_url.split("/")[-1]
        dst = output_dir / f"{next_id} {url_filename}"
        print(f"Downloading {new_url} as {dst}")
        urlretrieve(new_url, dst)

        append_url_to_file(script_dir / "urls.txt", new_url)
        next_id += 1

    print("Done!")



if __name__ == "__main__":
    pass
    main()


































