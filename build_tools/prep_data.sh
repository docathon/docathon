#! /bin/bash

# Scripts to run before pushing to github
set -e

echo "Fetch github commits for projects"
pushd src/watchtower

python extract_project_information.py ../data/docathon_project_registration.csv
python fetch_user_activity.py ../data/docathon_user_registration.csv
