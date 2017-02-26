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
parser.add_argument("--since", "-s", default="2017-01-01",
                    help="Date from which to search, YYYY-MM-DD")

args = parser.parse_args()

# Generate the github API user:token pair
# auth_user = args.auth_user
# auth_token = get_API_token(args.auth_token)
# auth = ':'.join([auth_user, auth_token])
# XXX should fix this to have choldgraf's technic work on travis
auth = get_API_token(args.auth)
print(auth)

per_page = args.per_page,
max_pages = args.max_pages
since = args.since

# Load data from google drive questionnaire
info = pd.read_csv(args.filename).values

# Iterate projects and retrieve its latest info
print('Updating commits for %s projects' % len(info))
downloaded_commits = []
exceptions = []
for user, project in info:
    try:
        commits_.update_commits(user, project, auth,
                                since=since)
    except:
        exceptions.append(project)

print('Finished updating commits.\nFailed for: {}'.format(exceptions))
