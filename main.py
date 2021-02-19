import os
from dotenv import load_dotenv
from ghcrawler import GHcrawler


if __name__ == '__main__':
    
    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    repos = ['automl/SMAC3', 'hyperopt/hyperopt']
    ghc = GHcrawler(repositories=repos, token=GITHUB_TOKEN)
    ghc.fetch_data()
    ghc.plot()
    ghc.calculate_stats()

    results = ghc.report
    print(results)
