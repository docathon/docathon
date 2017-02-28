import shutil as sh
from glob import glob
import os.path as op
import os

path_projects = '../../blog/content/pages/projects/'
if not op.exists(path_projects):
    os.makedirs(path_projects)

for project in glob('build/*.md'):
    name = op.basename(project)
    sh.copy(project, path_projects + name)

if op.exists(path_projects + 'images'):
    sh.rmtree(path_projects + 'images')

sh.copytree('build/images', path_projects + 'images')
print('Finished copying pages.')
