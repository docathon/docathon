#! /bin/bash

set -e

echo "Fetch github commits for projects"
pushd src/watchtower
python fetch_project_commits.py .downloaded_projects
python plot_commits.py
popd

echo "Build blog"
cd blog
make html
cd ..
# doctr deploy --deploy-repo BIDS/docathon --built-docs blog/output --gh-pages-docs='.'

