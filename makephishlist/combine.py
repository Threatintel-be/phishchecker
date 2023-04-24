#!/usr/bin/python3
with open('phishurls.txt', 'r') as f1, open('phishurl.txt', 'r') as f2, open('phish_urls.txt', 'w') as out_file:
    # Combine contents of both files and write to urls.txt
    out_file.writelines(set(f1.readlines() + f2.readlines()))

