import csv
import urllib.request

url = 'http://data.phishtank.com/data/online-valid.csv'

# Download the CSV file and save it as a temporary file
urllib.request.urlretrieve(url, 'temp.csv')

# Open the temporary file and read the CSV data
with open('temp.csv', 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    # Extract the URLs from the CSV data and write them to the output file
    with open('phishurl.txt', 'w') as outfile:
        for row in csvreader:
            url = row['url'].strip()
            if url.startswith('http') or url.startswith('https'):
                outfile.write(url + '\n')

# Delete the temporary file
import os
os.remove('temp.csv')

