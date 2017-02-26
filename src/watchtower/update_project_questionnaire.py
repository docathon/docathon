"""Update the project registration CSV with the latest version on dropbox"""
import mne
url = "https://www.dropbox.com/s/0xendp6g404ntzh/Docathon%20Project%20registration%20%28Responses%29%20-%20Form%20Responses%201.csv?dl=0"
url = url.replace('www.dropbox.com', 'dl.dropboxusercontent.com')
mne.utils._fetch_file(url, '../data/docathon_project_registration.csv')
