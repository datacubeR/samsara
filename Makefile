.PHONY: dashboard, tests

dashboard:
	streamlit run EDA/🏠_EDA_home.py

tests:
	pytest -v
