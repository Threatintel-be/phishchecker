#!/usr/bin/env python3

import requests
from concurrent.futures import ThreadPoolExecutor
import socket

# Set the DNS resolver to 8.8.8.8
dns_resolver = '8.8.8.8'
resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
resolver.connect((dns_resolver, 53))
resolver_ip = resolver.getsockname()[0]
resolver.close()
print("Using DNS resolver {}".format(resolver_ip), flush=True)


# Define ANSI escape codes for console output colors
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'


def check_url(url):
    if url in open('verified_urls.txt').read() or url in open('removed.txt').read():
        print("Skipping {} (already verified or removed)".format(url), flush=True)
        return

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("{}{} is active{}".format(GREEN, url, RESET), flush=True)
            with open('verified_phish_urls.txt', 'a') as f:
                f.write(url + '\n')
                f.flush()
        else:
            print("{}{} returned a {} status code{}".format(RED, url, response.status_code, RESET), flush=True)
            with open('phish_removed.txt', 'a') as f:
                f.write(url + '\n')
                f.flush()
    except:
        print("{}{} is not active{}".format(RED, url, RESET), flush=True)
        with open('phish_removed.txt', 'a') as f:
            f.write(url + '\n')
            f.flush()

if __name__ == '__main__':
    with open('phish_urls.txt') as f:
        urls = f.read().splitlines()

    with ThreadPoolExecutor(max_workers=500) as executor:
        executor.map(check_url, urls)

