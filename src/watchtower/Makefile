

all:
	python update_questionnaires.py
	python update_project_database.py ../data/docathon_project_registration.csv
	python update_user_database.py ../data/docathon_user_registration.csv
	python extract_projects_information.py ../data/docathon_project_registration.csv
	python calculate_user_commits.py
	python calculate_project_commits.py
