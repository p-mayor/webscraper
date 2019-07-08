#!/usr/bin/python

import argparse
import requests
import re
from bs4 import BeautifulSoup


def create_parser():
    """Creates and returns an argparse cmd line option parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url to be scraped")
    return parser


def main():
    args = create_parser().parse_args()
    r = requests.get(args.url)
    matchURLS = re.finditer(r'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r.text)
    matchEmails = re.finditer(r'''(?:[a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''', r.text)
    matchPhones = re.finditer(r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?', r.text)
    URL_list = []
    email_list = []
    phone_list = []
    for i in matchURLS:
        URL_list.append(i.group(0))
    for j in matchEmails:
        email_list.append(str(j.group(0)))
    
    for k in matchPhones:
        phone_list.append(str(k.group(1)+'-'+k.group(2)+'-'+k.group(3)))

    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('script'):
        if link.get('src'):
            URL_list.append((link.get('src')))
    for link in soup.find_all('a'):
        if link.get('href'):
            URL_list.append((link.get('href')))
    for link in soup.find_all('img'):
        if link.get('src'):
            URL_list.append((link.get('src')))
    
    # print(soup.prettify())
    print("\nPhone Numbers:")
    phone_set = set(phone_list)
    print("\n".join(phone_set))
    print("\nEmails:")
    email_set = set(email_list)
    print("\n".join(email_set))
    print('\n\nURLs:')
    URL_set = set(URL_list)
    print("\n".join(URL_set))


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main()
