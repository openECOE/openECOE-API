# Build project
.PHONY = build
build:
	python3 -m venv env
	pip3 install -r requirements.txt

# Install dependencies
.PHONY = deps
deps:
	pip3 install -r requirements.txt

# Run tests
.PHONY = test
test:
	python3 -m unittest discover -s ./tests -p '*Test.py'

# Run manage app
.PHONY = run/manage
run/manage:
	python3 main.py --service manage

# Run photostore app
.PHONY = run/photostore
run/photostore:
	python3 main.py --service photostore