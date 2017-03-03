import argparse
import pandas as pd
from watchtower import commits_
from watchtower._config import get_API_token

parser = argparse.ArgumentParser()
parser.add_argument("filename",
                    help="Path to projects signup questionnaire")
parser.add_argument("--auth", default="GITHUB_API")
parser.add_argument("--outdir", "-o", default="build")
parser.add_argument("--per_page", "-n", default=100)
parser.add_argument("--max_pages", "-m", default=100)
parser.add_argument("--since", "-s", default="2017-02-01",
                    help="Date from which to search, YYYY-MM-DD")

args = parser.parse_args()

# Generate the github API user:token pair
auth = get_API_token(args.auth)

per_page = args.per_page,
max_pages = args.max_pages
since = args.since

# Load data from google drive questionnaire
users = pd.read_csv(args.filename)
usernames = users['GitHub User Name'].values

# Iterate projects and retrieve its latest info
print('Updating commits for %s users' % len(usernames))
exceptions = []
for user in usernames:
    try:
        commits_.update_commits(user, auth=auth, since=since)
    except:
        exceptions.append(user)

print('Finished updating commits.\nFailed for: {}'.format(exceptions))
