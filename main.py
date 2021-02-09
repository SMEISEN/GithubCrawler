import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from github import Github
from datetime import timedelta


if __name__ == '__main__':
    
    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    g = Github(GITHUB_TOKEN)

    repo = g.get_repo('hyperopt/hyperopt')
    stars = repo.get_stargazers_with_dates()

    this_day = ''
    count = 0
    dates = []
    counts = []
    for i, star in enumerate(stars):
        starred_at = star.raw_data['starred_at']
        
        if starred_at[:10] != this_day:
            dates.append(this_day)
            if len(counts) > 0:
                counts.append(counts[-1] + count)
            else:
                counts.append(count)

            this_day = starred_at[:10]
            count = 1
        else:
            count += 1
    dates.pop(0)
    counts.pop(0)

    df = pd.DataFrame(counts, index =dates, columns =['Stars'])
    plt.figure()
    df.plot()
    plt.show()
