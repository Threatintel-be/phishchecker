#!/usr/bin/python3
import requests
import zipfile

# Download the Tranco list file
url = "https://tranco-list.s3.amazonaws.com/tranco_7PWQX-1m.csv.zip"
r = requests.get(url)
with open("top-1m.csv.zip", "wb") as f:
    f.write(r.content)

# Extract domain names and format them
with zipfile.ZipFile("top-1m.csv.zip", "r") as z:
    z.extractall()

with open("top-1m.csv") as f:
    domains = [line.split(",")[1].strip() for line in f]

formatted_domains = ["https://www." + domain for domain in domains]

# Write formatted domains to a file
with open("formatted_domains.txt", "w") as f:
    for domain in formatted_domains:
        f.write(domain + "\n")

