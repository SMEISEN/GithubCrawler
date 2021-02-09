import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from github import Github
from datetime import timedelta, date


if __name__ == '__main__':
    
    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    g = Github(GITHUB_TOKEN)

    repo = g.get_repo('hyperopt/hyperopt')
    stars = repo.get_stargazers_with_dates()
    commits = repo.get_commits().reversed

    this_day = None
    count = 0
    dates = []
    counts = []
    for i, star in enumerate(stars):
        starred_at = date(
            star.starred_at.year,
            star.starred_at.month,
            star.starred_at.day
        )
        
        if starred_at != this_day:
            dates.append(this_day)
            if len(counts) > 0:
                counts.append(counts[-1] + count)
            else:
                counts.append(count)

            this_day = starred_at
            count = 1
        else:
            count += 1
    if starred_at != this_day:
        dates.append(this_day)
        counts.append(counts[-1] + count)
    dates.pop(0)
    counts.pop(0)

    df = pd.DataFrame(counts, index =dates, columns =['Stars'])
    df.plot()
    plt.show()

    this_day = None
    count = 0
    dates = []
    counts = []
    for i, commit in enumerate(commits):
        last_modified = date(
            commit.commit.author.date.year,
            commit.commit.author.date.month,
            commit.commit.author.date.day
        )
        
        if last_modified != this_day:
            dates.append(this_day)
            if len(counts) > 0:
                counts.append(counts[-1] + count)
            else:
                counts.append(count)

            this_day = last_modified
            count = 1
        else:
            count += 1
    if last_modified != this_day:
        dates.append(this_day)
        counts.append(counts[-1] + count)
    
    dates.pop(0)
    counts.pop(0)

    df = pd.DataFrame(counts, index =dates, columns =['Commits'])
    df.plot()
    plt.show()
