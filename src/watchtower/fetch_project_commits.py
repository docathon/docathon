import argparse
import numpy as np
from watchtower import commits_
from watchtower._config import get_API_token

parser = argparse.ArgumentParser()
parser.add_argument("filename")
parser.add_argument("--auth_user", default='GITHUB_API_USER')
parser.add_argument("--auth_token", default='GITHUB_API_TOKEN')
parser.add_argument("--outdir", "-o", default="build")
parser.add_argument("--per_page", "-n", default=100)
parser.add_argument("--max_pages", "-m", default=100)
parser.add_argument("--since", "-s", default="2017-01-01",
                    help="Date from which to search, YYYY-MM-DD")

args = parser.parse_args()

# Generate the github API user:token pair
auth_user = args.auth_user
auth_token = get_API_token(args.auth_token)
auth = ':'.join([auth_user, auth_token])

per_page = args.per_page,
max_pages = args.max_pages
since = args.since

# Load data from google drive questionnaire
users, projects = np.loadtxt(args.filename, dtype=bytes).T

# Iterate projects and retrieve its latest info
print('Updating commits for %s projects' % len(users))
downloaded_commits = []
exceptions = []
for user, project in zip(users, projects):
    commits_.update_commits(user.decode(), project.decode(), auth,
                            since=since)

print('Finished updating commits.')
