#! /bin/bash

set -e

echo "Fetch github commits for projects"
pushd src/watchtower
python update_project_questionnaire.py
python fetch_project_commits.py ../watchtower/.downloaded_projects
python plot_commits.py 
python add_images_to_md.py
python create_projects_summary.py
python move_project_pages.py
python calculate_user_commits.py
python plot_user_activity.py
popd

echo "Build blog"
cd blog
make html
cd ..
doctr deploy --deploy-repo BIDS/docathon --built-docs blog/output --gh-pages-docs='.'

