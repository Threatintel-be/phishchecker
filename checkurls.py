import re

input_file = "verified_phish_urls.txt"
output_file = "valid_phish_urls.txt"

# Regular expression to check for a valid URL format
url_pattern = re.compile(r'^https?://[\w\-\.]+\.[a-zA-Z]{2,}(?:\/[\w\/]*)*$')

valid_urls = []

with open(input_file, 'r') as f:
    for line in f:
        url = line.strip()
        if url_pattern.match(url):
            valid_urls.append(url)

with open(output_file, 'w') as f:
    for url in valid_urls:
        f.write(url + '\n')

print(f"Valid URLs written to {output_file}")

