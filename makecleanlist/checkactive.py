#!/usr/bin/env python3

import requests
import socket
from multiprocessing import Pool

# Set the DNS resolver to 94.140.14.15
dns_resolver = '94.140.14.15'
resolver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
resolver.connect((dns_resolver, 53))
resolver_ip = resolver.getsockname()[0]
resolver.close()
print(f"Using DNS resolver {resolver_ip}")


# Define ANSI escape codes for console output colors
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'


def check_url(url):
    if url in open('verified_urls.txt').read() or url in open('removed.txt').read():
        print(f"Skipping {url} (already verified or removed)")
        return

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"{GREEN}{url} is active{RESET}")
            with open('verified_urls.txt', 'a') as f:
                f.write(url + '\n')
                f.flush()
        else:
            print(f"{RED}{url} returned a {response.status_code} status code{RESET}")
            with open('removed.txt', 'a') as f:
                f.write(url + '\n')
                f.flush()
    except:
        print(f"{RED}{url} is not active{RESET}")
        with open('removed.txt', 'a') as f:
            f.write(url + '\n')
            f.flush()


if __name__ == '__main__':
    with open('urls.txt') as f:
        urls = f.read().splitlines()

    with Pool(processes=10) as pool:
        pool.map(check_url, urls)

