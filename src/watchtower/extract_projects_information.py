import pandas as pd
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("filename",
                    help=("CSV file containing the project "
                          "registration information."))
args = parser.parse_args()

projects = pd.read_csv(args.filename)
'url', 'github_org', 'name', 'description', ''

rename = {'Documentation URL': 'url', 'Name of the project': 'name',
          'If yes, can you provide the Github url?': 'url_doc',
          'Github organization and project (if applicable)': 'github_org',
          'Description': 'description',
          'Timestamp': 'date',
          'is_github': 'is_github'}
projects = projects.rename(columns=rename)
projects = projects[list(rename.values())]
projects.to_csv('.project_info.csv')
