

all:
	python update_project_questionnaire.py
	python extract_project_information.py ../data/docathon_project_registration.csv
	python fetch_project_commits.py .downloaded_projects
	python plot_commits.py
	python add_images_to_md.py
