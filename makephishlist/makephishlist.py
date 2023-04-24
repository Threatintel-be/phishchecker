import requests

# Define the URLs of the feeds we want to download
feed_urls = [
    "https://openphish.com/feed.txt",
    "https://urlhaus.abuse.ch/downloads/text/",
]

# Define the output file name
output_file = "phishurls.txt"

# Create a set to store the unique URLs we find
urls = set()

# Loop through the feed URLs and download each one
for feed_url in feed_urls:
    response = requests.get(feed_url)
    
    # If the response was successful, process the content
    if response.status_code == 200:
        # Split the content into lines and add each line as a URL to the set
        for line in response.text.splitlines():
            urls.add(line.strip())

# Write the URLs to the output file
with open(output_file, "w") as f:
    f.write("\n".join(urls))

