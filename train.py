# Import libraries
import pandas as pd
import numpy as np
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier # import a different algorithm
from sklearn.metrics import accuracy_score, confusion_matrix
import requests
from bs4 import BeautifulSoup
import progressbar # import the library
import re # for regular expressions
import gensim # for Word2Vec vectorizer
import nltk # for natural language processing

# Download the Word2Vec model and the stopwords list
nltk.download('punkt')
nltk.download('stopwords')
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

# Read the files
phish_urls = pd.read_csv("verified_phish_urls.txt", header=None, names=["url"])
safe_urls = pd.read_csv("verified_urls.txt", header=None, names=["url"])

# Label the urls
phish_urls["label"] = 1 # phishing
safe_urls["label"] = 0 # safe

# Concatenate the dataframes
data = pd.concat([phish_urls, safe_urls], ignore_index=True)

# Shuffle the data
data = data.sample(frac=1, random_state=42)

# Define a function to get the content of a website
def get_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.get_text()
        return content
    except:
        return ""

# Define a function to get the domain name of a url
def get_domain(url):
    try:
        domain = re.search(r"(?:https?:\/\/)?(?:www\.)?([^\/]+)", url).group(1)
        return domain
    except:
        return ""

# Define a function to get the length of a url
def get_length(url):
    return len(url)

# Define a function to get the number of dots in a url
def get_dots(url):
    return url.count(".")

# Define a function to get the presence of special characters in a url
def get_special(url):
    special_chars = ["@", "_", "-", "%", "&", "=", "?", "+", "$", "#"]
    for char in special_chars:
        if char in url:
            return 1 # special character found
    return 0 # no special character found

# Define a function to get the title of a website
def get_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string
        return title
    except:
        return ""

# Define a function to get the meta tags of a website
def get_meta(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        meta = soup.find_all("meta")
        meta_text = ""
        for tag in meta:
            meta_text += str(tag)
        return meta_text
    except:
        return ""

# Define a function to get the images of a website
def get_images(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img")
        images_text = ""
        for image in images:
            images_text += str(image)
        return images_text
    except:
        return ""
# Define a function to vectorize text using Word2Vec model
def vectorize(text):
    tokens = nltk.word_tokenize(text) # tokenize the text into words
    tokens = [token for token in tokens if token.isalpha()] # remove non-alphabetic tokens
    tokens = [token.lower() for token in tokens] # convert tokens to lowercase
    stopwords = nltk.corpus.stopwords.words('english') # get the stopwords list
    tokens = [token for token in tokens if token not in stopwords] # remove stopwords from tokens

    vector = np.zeros(300) # initialize an empty vector of size 300 (the dimension of Word2Vec vectors)
    count = 0 # initialize a counter for the number of valid tokens

    for token in tokens: # iterate over the tokens
        if token in model: # check if the token is in the Word2Vec model vocabulary
            vector += model[token] # add the token vector to the vector
            count += 1 # increment the counter

    if count > 0: # check if there is at least one valid token
        vector /= count # average the vector

    return vector # return the vector

# Apply the functions to the urls and store the results in new columns with progress bar
bar = progressbar.ProgressBar(max_value=len(data)) # create a progress bar object
data["content"] = data["url"].apply(get_content)
bar.update(1) # update the progress bar after getting content
data["domain"] = data["url"].apply(get_domain)
bar.update(2) # update the progress bar after getting domain name
data["length"] = data["url"].apply(get_length)
bar.update(3) # update the progress bar after getting length
data["dots"] = data["url"].apply(get_dots)
bar.update(4) # update the progress bar after getting number of dots
data["special"] = data["url"].apply(get_special)
bar.update(5) # update the progress bar after getting presence of special characters
data["title"] = data["url"].apply(get_title)
bar.update(6) # update the progress bar after getting title
data["meta"] = data["url"].apply(get_meta)
bar.update(7) # update the progress bar after getting meta tags
data["images"] = data["url"].apply(get_images)
bar.update(8) # update the progress bar after getting images

# Vectorize the features using Word2Vec model with progress bar
bar.update(9) # update the progress bar before vectorizing features
X_url = np.array([vectorize(url) for url in data["url"]])
X_content = np.array([vectorize(content) for content in data["content"]])
X_domain = np.array([vectorize(domain) for domain in data["domain"]])
X_title = np.array([vectorize(title) for title in data["title"]])
X_meta = np.array([vectorize(meta) for meta in data["meta"]])
X_images = np.array([vectorize(images) for images in data["images"]])

# Concatenate the feature vectors
X = np.concatenate([X_url, X_content, X_domain, X["length"].to_numpy().reshape(-1,1), X["dots"].to_numpy().reshape(-1,1), X["special"].to_numpy().reshape(-1,1), X_title, X_meta, X_images], axis=1)

# Split the data into train and test sets
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest classifier with progress bar # use a different algorithm
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Make predictions on the test set with progress bar
y_pred = []
for i, x in enumerate(X_test):
    y_pred.append(model.predict(x.reshape(1,-1)))
    bar.update(i + 10) # update the progress bar

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
confusion = confusion_matrix(y_test, y_pred)
print("Accuracy:", accuracy)
print("Confusion matrix:")
print(confusion)
