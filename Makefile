install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint src/dtmf.py

test:
	pytest
