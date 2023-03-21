# ifunny-downloader

download all liked posts from your ifunny account

## Running the script

* Install python3
* Clone the repository
* Install requirements: `pip3 install -r requirements.txt`
* Login to your ifunny account in a browser. I used firefox and this script assumes you use firefox. You should be able to modify it to use other browsers if you want though by changing line 10 in the script
* Open your browsers developer tools and go to the network tab. Navigate to `https://ifunny.co/account/smiles` 
* Find the request in the list which should be near the bottom of `https://ifunny.co/api/v1/news?limit=10`. Click this request and copy the `x-csrf-token` from the request headers. Open the script and put this value in the headers near the top of the script. This value and `User-Agent` seemed to be the only ones that were required. You should only have to modify `x-csrf-token` though.
* Run the script with `python3 download_likes.py`
* Files will be saved to the output directory

## Downloading new liked items

Items that you have already downloaded are kept track of in urls.txt. Running the script again will skip over items in that file and only download newly found items. Files are kept in the order that you liked them with 1 being the oldest. You may have to update `x-csrf-token` in the future when the script is run again
