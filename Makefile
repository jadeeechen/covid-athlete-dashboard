# use bash for shell commands
SHELL := /bin/bash

# paths
RAW_DATA = data/raw/Athlete_Non-Athlete.csv
PROCESSED_DIR = data/processed
OUTPUT_HTML = index.html

# default target
.PHONY: all
all: run

# run the full pipeline in order:
# 1. download raw data only if missing
# 2. preprocess data
# 3. build dashboard html
.PHONY: run
run:
	@if [ ! -f $(RAW_DATA) ]; then \
		echo "downloading raw data..."; \
		python src/m01_download_data.py; \
	else \
		echo "raw data exists, skipping download"; \
	fi
	python src/m02_data_preprocessing.py
	python src/m11_dashboard.py

# explicitly run download step
.PHONY: download
download:
	python src/m01_download_data.py

# run only preprocessing
.PHONY: preprocess
preprocess:
	python src/m02_data_preprocessing.py

# run only dashboard
.PHONY: dashboard
dashboard:
	python src/m11_dashboard.py

# remove generated dashboard html
.PHONY: clean
clean:
	rm -f $(OUTPUT_HTML)

# remove all generated files
.PHONY: clean-all
clean-all:
	rm -f $(PROCESSED_DIR)/*.csv
	rm -f $(RAW_DATA)
	rm -f $(OUTPUT_HTML)