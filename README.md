## Pagerank
This project contains two implementations of the pagerank algorithm. It is a part of Harvards [CS50AI]([url](https://cs50.harvard.edu/ai/2024/)) course.
#### Usage:
- Open the command prompt, navigate to the appropriate folder
- Execute the command ```python pagerank.py corpus1``` to calculate the ranking for the included example corpus 1.
#### Contained files:
- ```corpus0/1/2```: Example corpi of interconnected webpages.
- ```pagerank.py```: All code is implemented here:
    - The function ```sample_pagerank``` estimates the website relevance by randomly sampling among the webpages and then calculating the probability of reaching each other page.
    - The function ```iterate_pagerank``` iteratively calculates the page rank.


