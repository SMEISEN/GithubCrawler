import os
from dotenv import load_dotenv
from ghcrawler import GHcrawler


if __name__ == '__main__':
    
    load_dotenv()
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

    ghc = GHcrawler(token=GITHUB_TOKEN)
    ghc.fetch_data()
    ghc.plot()

    results = ghc.report
    print(results)
