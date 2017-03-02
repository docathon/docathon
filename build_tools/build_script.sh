#! /bin/bash

set -e

echo "Fetch github commits for projects"
pushd src/watchtower
python update_project_questionnaire.py
python extract_project_information.py ../data/docathon_project_registration.csv
python fetch_project_commits.py ../watchtower/.downloaded_projects
python plot_commits.py 
python add_images_to_md.py
python create_projects_summary.py
python move_project_pages.py
python fetch_user_activity.py ../data/docathon_user_registration.csv
python calculate_user_commits.py
python plot_user_activity.py
popd

echo "Build blog"
cd blog
make html
cd ..
doctr deploy --deploy-repo BIDS/docathon --built-docs blog/output --gh-pages-docs='.'

