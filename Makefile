.PHONY: dashboard, tests

dashboard:
	streamlit run EDA/🏠_EDA_home.py

tests:
	pytest -v

resampling:
	python samsara/01-resampling.py -r $(r) -i $(i)
