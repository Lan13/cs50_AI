from distutils import dir_util
from email.errors import InvalidMultipartContentTransferEncodingDefect
import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename)) as file:
                files[filename] = file.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = []
    tokenized = nltk.tokenize.word_tokenize(document)
    punctuation = string.punctuation
    stopwords = nltk.corpus.stopwords.words("english")
    for word in tokenized:
        if word not in punctuation and word not in stopwords:
            words.append(word.lower())
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs_value = dict()
    documents_count = len(documents.keys())
    for item in documents.items():
        names, words = item
        flag = []
        for word in words:
            if word not in idfs_value.keys():
                idfs_value[word] = 1
                flag.append(word)
            elif word not in flag:
                idfs_value[word] += 1
                flag.append(word)
    for item in idfs_value.items():
        key, value = item
        idfs_value[key] = math.log(documents_count / value)
    return idfs_value


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = dict()
    for item in files.items():
        file, words = item
        tf_idf = 0
        for word in query:
            if word not in words:
                continue
            tf_idf += (words.count(word) * idfs[word])
        tf_idfs[file] = tf_idf
    return sorted(files.keys(), key=lambda file: tf_idfs[file], reverse=True)[:n]    


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = dict()
    densities = dict()
    for item in sentences.items():
        sentence, words = item
        idf = 0
        density = sum([words.count(x) for x in query])
        for word in query:
            if word not in words:
                continue
            idf += idfs[word]
        scores[sentence] = idf
        densities[sentence] = density / len(words)
    return sorted(sentences.keys(), key=lambda sentence: (scores[sentence], densities[sentence]), reverse=True)[:n]
    

if __name__ == "__main__":
    main()
