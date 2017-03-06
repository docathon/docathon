#! /bin/bash

set -e

echo "Fetch github commits for projects"
pushd src/watchtower
# Generate project pages + images
python plot_project_commits.py
python create_project_pages.py
python add_images_to_md.py
python create_projects_summary.py

# Generate user summary page
python plot_user_activity.py

# General stats page
python create_stats_page.py
python move_project_pages.py
python plot_global_activity.py
popd

echo "Build blog"
cd blog
make html
cd ..
doctr deploy --deploy-repo BIDS/docathon --built-docs blog/output --gh-pages-docs='.'

