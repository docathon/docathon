#! /bin/bash
# This script is meant to be called by the install step for Travis.

set -e

pip install 'pelican<3.7' markdown
pip install doctr
pip install pandas matplotlib numpy tqdm
pip install git+git://github.com/NelleV/watchtower
