import argparse
import pandas as pd
from watchtower.handlers_ import UserDatabase


def parse_name(name):
    if not isinstance(name, str):
        return None
    else:
        name = name.split('/')[-1]
        return name

parser = argparse.ArgumentParser()
parser.add_argument("filename",
                    help=("CSV file containing the user "
                          "registration information."))
parser.add_argument("--outdir", "-o", default="build")
args = parser.parse_args()

db = UserDatabase(auth='GITHUB_API')

users = pd.read_csv(args.filename)
names = [parse_name(name)
         for name in users['GitHub User Name'].values]
for name in names:
    if name is None:
        continue
    db.update_user(name)
