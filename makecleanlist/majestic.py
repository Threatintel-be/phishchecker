#!/usr/bin/python3
import requests
import csv

# URL for the Majestic Million CSV file
url = "https://downloads.majestic.com/majestic_million.csv"

# Download the CSV file
response = requests.get(url)

# Split the CSV content into rows
rows = csv.reader(response.content.decode("utf-8").splitlines())

# Skip the header row
next(rows)

# Extract domain names and transform them into URLs
urls = ["https://www." + row[2] for row in rows]

# Save the URLs to a file
with open("majestic_urls.txt", "w") as f:
    f.write("\n".join(urls))

