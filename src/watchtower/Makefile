

all: csv plots

csv:
	python update_questionnaires.py
	python update_project_database.py ../data/docathon_project_registration.csv --since 2017-02-20
	python update_user_database.py ../data/docathon_user_registration.csv --since 2017-02-20
	python generate_projects_list.py
	python extract_projects_information.py ../data/docathon_project_registration.csv
	python calculate_user_commits.py
	python calculate_project_commits.py
	python update_diff_stats.py

plots:
	python plot_global_activity.py
	python plot_project_commits.py
	python plot_user_activity.py
