import pandas as pd
import matplotlib.pyplot as plt
from github import Github
from datetime import date, datetime


class GHcrawler:

    def __init__(self, repositories=None, token: str = None):
        if repositories is None:
            self._repositories = ['PyGithub/PyGithub']
        else:
            self._repositories = repositories
        self.report = dict.fromkeys(self._repositories, {
            'star_history': pd.DataFrame(),
            'commit_history': pd.DataFrame(),
            'popularity': None,
            'momentum': None,
            'activity': None
        })

        self._gh = Github(token)

    def fetch_data(self, stars: bool = True, commits: bool = True, verbose: bool = True):

        results = []
        for i, repo_name in enumerate(self._repositories):

            if verbose:
                print(f"\nFetching data from repository \"{repo_name}\", {i + 1}/{len(self._repositories)}")

            repo = self._gh.get_repo(repo_name)
            result = []

            if stars:
                if verbose:
                    print('\nBeginning with fetching stars!')
                    print('this may take some time...')

                stars = repo.get_stargazers_with_dates()
                sc = self._StarCount(stars)
                dates, counts = sc.count()
                df_stars = pd.DataFrame(counts, index=dates, columns=['Stars'])
                df_stars = df_stars.loc[~df_stars.index.duplicated(keep='last')]
                df_stars = df_stars.sort_index()
                result.append(df_stars)
                self.report[repo_name]['star_history'] = df_stars
                if verbose:
                    print('Stars successfully fetched!')

            if commits:
                if verbose:
                    print('\nBeginning with fetching commits!')
                    print('this may take some time...')
                commits = repo.get_commits().reversed
                cc = self._CommitCount(commits)
                dates, counts = cc.count()
                df_commits = pd.DataFrame(counts, index=dates, columns=['Commits'])
                df_commits = df_commits.loc[~df_commits.index.duplicated(keep='last')]
                df_commits = df_commits.sort_index()
                result.append(df_commits)
                self.report[repo_name]['commit_history'] = df_commits
                if verbose:
                    print('Commits successfully fetched!')

            results.append(result)

        if verbose:
            print(f"\nFinished fetching data from {len(self._repositories)} repository/ies")

        return results

    def plot(self):

        for repo_name, repo_data in self.report.items():
            if len(repo_data['star_history']) > 0:
                repo_data['star_history'].plot()
                plt.title(repo_name)
                plt.show()
            if len(repo_data['commit_history']) > 0:
                repo_data['commit_history'].plot()
                plt.title(repo_name)
                plt.show()

    class _BaseCount:

        def __init__(self, counting_object):
            self.counting_object = counting_object

        def count(self):

            counting_day = None
            item_date = None
            count = 0
            dates = []
            counts = []
            for item in self.counting_object:
                item_date = self._get_date(item)

                if item_date != counting_day:
                    dates.append(counting_day)
                    if len(counts) > 0:
                        counts.append(counts[-1] + count)
                    else:
                        counts.append(count)

                    counting_day = item_date
                    count = 1
                else:
                    count += 1
            if item_date != counting_day:
                dates.append(counting_day)
                counts.append(counts[-1] + count)
            dates.pop(0)
            counts.pop(0)

            return dates, counts

        @staticmethod
        def _get_date(item=None):

            if item is None:
                return datetime.utcnow()
            else:
                return None

    class _StarCount(_BaseCount):

        @staticmethod
        def _get_date(star=None):
            current_date = date(
                star.starred_at.year,
                star.starred_at.month,
                star.starred_at.day
            )

            return current_date

    class _CommitCount(_BaseCount):

        @staticmethod
        def _get_date(commit=None):
            current_date = date(
                commit.commit.author.date.year,
                commit.commit.author.date.month,
                commit.commit.author.date.day
            )

            return current_date
