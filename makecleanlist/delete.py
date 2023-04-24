# Open the files and read the URLs
with open('verified_urls.txt', 'r') as f:
    verified_urls = set(f.read().splitlines())

with open('removed.txt', 'r') as f:
    removed_urls = set(f.read().splitlines())

with open('urls.txt', 'r') as f:
    urls = f.read().splitlines()

# Remove the URLs that appear in the other files and print them out
removed = []
for url in urls:
    if url in verified_urls or url in removed_urls:
        removed.append(url)
    else:
        continue
new_urls = [url for url in urls if url not in verified_urls and url not in removed_urls]

# Print the removed URLs
if removed:
    print("The following URLs have been removed from urls.txt:")
    for url in removed:
        print(url)

# Write the new list of URLs back to urls.txt
with open('urls.txt', 'w') as f:
    f.write('\n'.join(new_urls))

