import requests
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, dest="url", help="URL to send your request")
    values = parser.parse_args()

    if not values.url:
        parser.error("[-] Please specify the URL, use --help for more information")
    else:
        return values

def request(url):
    result = None

    try:
        result = requests.post(url)
        if(result):
            raise Exception("Unexpected error occured")
        else:
            return result
    except:
        return Exception("Error making request")

def main(url):
    print(request(url))

if __name__ == "__main__":
        url = get_arguments()
        main(url)