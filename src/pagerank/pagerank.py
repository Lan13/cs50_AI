import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pages_name = []     # this is total pages
    for key in corpus.keys():
        pages_name.append(key)
    pages_count = len(pages_name)
    transition_probability = {}
    outgoing_links = corpus[page]   # this is a set representing all the linking page to "page"
    outgoing_count = len(outgoing_links)
    if outgoing_count == 0:
        for name in pages_name:
            transition_probability[name] = 1 / pages_count
    else:
        total_count = outgoing_count + 1    # calculate current total linked pages(include itself)
        transition_probability[page] = (1 - damping_factor) / total_count
        for name in outgoing_links:
            transition_probability[name] = (1 - damping_factor) / total_count + damping_factor / outgoing_count
    return transition_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages_name = []     # this is total pages
    for key in corpus.keys():
        pages_name.append(key)
    pages_count = len(pages_name)
    remain_times = n
    samples = []        # samples we have sampled from transition model
    start_sample = pages_name[random.randint(0, pages_count - 1)]
    samples.append(start_sample)
    remain_times = n - 1
    while remain_times > 0:     # sample by transition_model
        last_sample = samples[-1]   # transition model is a Markov chain so we need last sample
        transition_probability = transition_model(corpus, last_sample,damping_factor)
        probability = random.random()
        total_value = 0
        for item in transition_probability.items():
            key, value = item
            total_value = total_value + value
            if probability <= total_value:
                samples.append(key)
                break
        remain_times = remain_times - 1
    pagerank = dict()
    for page in samples:        # sample's counting
        if page in pagerank:
            pagerank[page] += 1
        else:
            pagerank[page] = 1
    for item in pagerank.items():   # normalized to 1
        key, value = item
        pagerank[key] = value / n
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages_name = []     # this is total pages
    numlinks = dict()
    for key in corpus.keys():
        pages_name.append(key)
        numlinks[key] = len(corpus[key])
    pages_count = len(pages_name)

    pagerank = dict()
    for page in pages_name:
        pagerank[page] = 1 / pages_count
    
    flag = True
    while flag:
        flag = False
        pagerank_new = {}
        for item in pagerank.items():
            key, value = item
            x = 0
            for i in pagerank.keys():
                if key in corpus[i]:
                    if numlinks[i] > 0:
                        x = x + (pagerank[i] / numlinks[i])
                    else:
                        x = x + (pagerank[i] / pages_count)
            pagerank_new[key] = (1 - damping_factor) / pages_count + damping_factor * x
            if abs(pagerank_new[key] - value) > 1e-3:
                flag = True
        for item in pagerank.items():
            key, value = item
            pagerank[key] = pagerank_new[key]
    
    probability_sum = sum([pagerank[key] for key in pagerank.keys()])   # normalized to 1
    for item in pagerank.items():
        key, value = item
        pagerank[key] = value / probability_sum

    return pagerank


if __name__ == "__main__":
    main()
