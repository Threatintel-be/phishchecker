#!/usr/bin/python3
with open('formatted_domains.txt', 'r') as f1, open('majestic_urls.txt', 'r') as f2, open('urls.txt', 'w') as out_file:
    # Combine contents of both files and write to urls.txt
    out_file.writelines(set(f1.readlines() + f2.readlines()))

