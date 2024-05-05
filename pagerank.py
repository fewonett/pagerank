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
    
    # calculate probability of random choice:
    unique_values = corpus.keys()
    unique_values_count = len(unique_values)
    within_page_links = corpus[page]
    
    # If the page contains links
    if len (within_page_links) != 0:
        min_pr = (1 - damping_factor)/ unique_values_count
        # Every page in corpus has at least this probability of being selected, thus:
        prob_dict = {key: min_pr for key in unique_values}
    # Calculate "within page probability"
        within_page_pr = damping_factor/ len(within_page_links)
    # Update probability for within page links:
        for i in within_page_links:
            prob_dict[i] = min_pr + within_page_pr
    
    # If there are no links on page:
    else:
        pr = 1/unique_values_count
        prob_dict = {key: pr for key in unique_values}
    return prob_dict
        

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create dictionary 
    unique_values = corpus.keys()
    return_dict = {key: 0 for key in unique_values}
    
    # Pick random page to start
    page = random.sample(list(unique_values),1)[0]    
    # Now loop
    for i in range(1, n +1):
        print(i)
        # Get probability distribution of choice
        dist = transition_model(corpus, page, damping_factor)
        # Update probability in return dict:
        for entry in dist.keys():
            return_dict[entry] = (return_dict[entry]*(i-1) + dist[entry])/(i)
        # Make random choice of next page based on the last pages probability: random.choices((set_to_choose_from), p_dist)
        page = random.choices(list(dist.keys()), list(dist.values()),k=1)[0]
        
    return return_dict



        
            
        

def iterate_pagerank(corpus, damping_factor=0.85, tolerance=0.001):
    num_pages = len(corpus)
    pageranks = {page: 1 / num_pages for page in corpus}
    while True:
        new_pageranks = {}
        converged = True
        for page in corpus:
            new_rank = (1 - damping_factor) / num_pages
            link_sum = 0 
            # Iterate through each page in the corpus and add value to the rank based on link occurrence
            for within_page in corpus:
                # Check if page has no links
                if len(corpus[within_page]) == 0:
                    link_contribution = pageranks[within_page] / num_pages
                    link_sum += link_contribution
                elif page in corpus[within_page]:
                    # Determine the contribution of 'within_page' to 'page''s rank
                    link_contribution = pageranks[within_page] / len(corpus[within_page])
                    link_sum += link_contribution  
            new_rank += damping_factor * link_sum
            new_pageranks[page] = new_rank
            if abs(new_pageranks[page] - pageranks[page]) > tolerance:
                converged = False
        pageranks = new_pageranks
        if converged:
            break
    return pageranks

if __name__ == "__main__":
    main()
