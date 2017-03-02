"""Update the project registration CSV with the latest version on dropbox"""
import mne

# Projects
url_proj = "https://www.dropbox.com/s/0xendp6g404ntzh/Docathon%20Project%20registration%20%28Responses%29%20-%20Form%20Responses%201.csv?dl=0"
url_proj = url_proj.replace('www.dropbox.com', 'dl.dropboxusercontent.com')
mne.utils._fetch_file(url_proj, '../data/docathon_project_registration.csv')

# Users
url_user = "https://www.dropbox.com/s/a5sa8wlxw7bbake/Docathon%20User%20registration%20form%20%28Responses%29%20-%20Form%20Responses%201.csv?dl=0"
url_user = url_user.replace('www.dropbox.com', 'dl.dropboxusercontent.com')
mne.utils._fetch_file(url_user, '../data/docathon_user_registration.csv')
print('Finished downloading files...')
