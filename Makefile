.PHONY: dashboard, tests

dashboard:
	streamlit run EDA/🏠_EDA_home.py

tests:
	pytest -v

resampling:
	python samsara/01-resampling.py -r $(r) -i $(i)

split:
	python samsara/02-split_data.py -r $(r) -i $(i)

train:
	python samsara/03-train.py 
