# GithubCrawler
Web crawler for GitHub repositories to walk through a queue of repository names and collect information about them.

The crawler receives a list of repository names, e.g.,  `["scikit-learn/scikit-learn", "hyperopt/hyperopt"]`.
It walks this list and scans the repositories to extract community features, e.g., stars, forks, used by, contributers, latest commit, a "activity"-metric, etc..
By default, the crawler collects all features. Specific features can be turned off in the initialization ,e.g., `crawler = GithubCrawler(stars=false)`
It stores these features into `pandas.DataFrame` and writes them into a `.csv`-file.

| Repository                | Stars | Forks | ... |
|---------------------------|-------|-------|-----|
| scikit-learn/scikit-learn | 44321 | 20921 | ... |
| ... | ... | ... | ... |
