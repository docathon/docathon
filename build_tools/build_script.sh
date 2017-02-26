#! /bin/bash

set -e

echo "Fetch github commits for projects"
pushd src/watchtower
python update_project_questionnaire.py
python extract_project_information.py ../data/docathon_project_registration.csv
python plot_commits.py 
python fetch_project_commits.py ../watchtower/.downloaded_projects
python add_images_to_md.py
python move_project_pages.py
popd

echo "Build blog"
cd blog
make html
cd ..
doctr deploy --deploy-repo BIDS/docathon --built-docs blog/output --gh-pages-docs='.'

