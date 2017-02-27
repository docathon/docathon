import pandas as pd
from tqdm import tqdm
import os.path as op

informations = pd.read_csv(".downloaded_projects").values
path_root = op.abspath('.')
exceptions = []
for user, project in tqdm(informations):
    filename = project.replace(" ", "_").lower()
    try:
        with open('build/{}.md'.format(filename), 'a') as ff:
            path_img_read = 'build/images/{}.png'.format(project)
            if not op.exists(path_img_read):
                print('Skipping {}'.format(project))
                continue
            path_img_write = 'images/{}.png'.format(project)
            ff.writelines(
                '\n\n# Activity\n---\n![]({})'.format(path_img_write))
    except:
        exceptions.append(project)
print('Finished inserting images.\nExceptions: {}'.format(exceptions))
