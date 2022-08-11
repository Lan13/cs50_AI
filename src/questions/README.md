# Problem In This Project

In this project you will find that you need to install `stopwords` in `nltk_data`. You can try to do like this:

```bash
cd ~
mkdir nltk_data && cd nltk_data/ && mkdir corpora && cd corpora/
wget https://github.com/nltk/nltk_data/blob/gh-pages/packages/corpora/stopwords.zip
unzip stopwords.zip && rm stopwords.zip
```

Also you can unzip it in other available path in `nltk.data.path`.