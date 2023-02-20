import requests
import argparse
import base64

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--u", "--url", dest="url", help="URL to send your Request", type=str, required=True)
    parser.add_argument("--r", "--request", dest="request", help="Request type", type=str, required=True)
    parser.add_argument("--h", "--headers", dest="headers", help="Headers of request", type=list)
    values = parser.parse_args()

    if not values.url:
        parser.error("[-] Please specify the URL, use --help for more information")
    else:
        return values

def get_headers(headers:str):
    json_headers={}

    for header in headers:
        head, value = header.split(":")
        json_headers.update(head+":"+value)

    return  json_headers

def send_post_request(url:str,header:list=None,data_values:str=None):
    return requests.post(url,headers=header, data=data_values)

def send_get_request(url,header=None,data_values=None):
    return requests.get(url,headers=header, data=data_values)

def encode_base64(string:str):
    string_bytes = string.encode('ascii')
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode('ascii').replace("==", "")

    return base64_string

def request_data():
    # Create request data
    return None

def request(values):
    result = None
    data = request_data()

    try:
        if values.request == "POST":
            result = send_post_request(values.url, values.headers, data)
        elif values.request == "GET":
            result = send_get_request(values.url, values.headers, data)
        if(result):
            raise Exception("Unexpected error occured")
        else:
            return result
    except:
        return Exception("Error making request")

def main(values):
    print(request(values))

if __name__ == "__main__":
        values = get_arguments()
        main(values)