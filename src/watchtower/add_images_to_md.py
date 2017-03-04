import pandas as pd
from tqdm import tqdm
import os.path as op

projects = pd.read_csv(".project_info.csv")
path_root = op.abspath('.')
exceptions = []
for ix, project in tqdm(projects.iterrows()):
    if not isinstance(project['github_org'], str):
        continue
    org, repo = project['github_org'].split('/')[-2:]
    filename = repo.replace(" ", "_").lower()
    try:
        with open('build/{}.md'.format(filename), 'a') as ff:
            path_img_read = 'build/images/{}.png'.format(repo)
            if not op.exists(path_img_read):
                raise ValueError("path doesn't exist for {}".format(repo))
            path_img_write = 'images/{}.png'.format(repo)
            ff.writelines(
                '\n\n# Activity\n---\n![]({})'.format(path_img_write))
    except Exception as ee:
        exceptions.append(ee)
print('Finished inserting images.\nExceptions: {}'.format(exceptions))
