# MP1 Data Pipeline

This project provides a configurable pipeline that loads, validates, cleans, and saves data. The `pipeline.py` script coordinates the workflow using command-line arguments for the input, output, configuration, and logging level. The `src/data_loaders.py` module loads CSV, JSON, and YAML files, while `src/data_validator.py` checks required columns and removes invalid numeric values. The `src/data_processor.py` module removes duplicates, handles missing values, removes outliers, and creates a cleaning report. The `src/data_output.py` module creates output directories and saves the cleaned data as CSV without an index. Shared logging and file validation functions live in `src/utils.py`, and `src/__init__.py` exposes the functions used by the pipeline. Configuration is stored in `config/config.yaml`, sample inputs are in `fixtures/`, and generated files are saved under the Git-ignored `output/` directory.

## Run the pipeline

With the virtual environment active, run from the directory containing `pipeline.py`. If you are at the repository root, first run `cd MP1-DATA-PIPELINE`.

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Sample result

The sample contains 100 rows. Validation removes two rows with invalid ratings, leaving 98 rows. Cleaning removes two duplicates, two rows with missing values, and two rating outliers. The resulting 92 rows are saved to `output/clean.csv`.

```text
Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```