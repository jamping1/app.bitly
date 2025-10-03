import argparse
from urllib.parse import urlparse

import requests
from dotenv import dotenv_values


BITLY_TOKEN = dotenv_values(".env")["BITLY_TOKEN"]


def shorten_link(token, url_to_cut):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {"Authorization": F"Bearer {token}"}
    url_for_request = {
                      "long_url": url_to_cut
                      }
    response = requests.post(url, headers=headers, json=url_for_request)
    response.raise_for_status()
    short_url = response.json()["link"]
    return short_url
    

def get_click_count(token, url_to_check):
    url_parsed = urlparse(url_to_check)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{netloc}/{path}/clicks/summary"
    url = url.format(netloc=url_parsed.netloc, path=url_parsed.path)
    headers = {"Authorization": F"Bearer {token}"}
    params = {
             "units": "-1"
             }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    total_clicks = response.json()["total_clicks"]
    return total_clicks
    

def get_link_status(token, url_to_check):
    url_to_check = urlparse(url_to_check)
    url = "https://api-ssl.bitly.com/v4/bitlinks/{netloc}/{path}"
    url = url.format(netloc=url_to_check.netloc, path=url_to_check.path)
    headers = {"Authorization": F"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    parser = argparse.ArgumentParser(description="Создание или проверка короткой ссылки")
    parser.add_argument("link", help="Ваша ссылка")
    args = parser.parse_args()
    input_url = args.link
    link_status = get_link_status(BITLY_TOKEN, input_url)
    if link_status :
        try:
            total_clicks = get_click_count(BITLY_TOKEN, input_url)
            print("Total clicks:", total_clicks)
        except requests.exceptions.HTTPError as error:
            exit("Can't get data from server:\n{0}".format(error))
    else:
        try:
            short_url = shorten_link(BITLY_TOKEN, input_url)
            return print("Bitlink:", short_url)
        except requests.exceptions.HTTPError as error:
            exit("Can't get data from server:\n{0}".format(error))


if __name__ == "__main__":
    main()
