# Zenlytic Adapters

Utilities for converting semantic layer YAML files to Zenlytic's format.

## Steps for usage:
1. Clone this repo in a valid dbt project
1. Run `dbt parse` to generate model yaml files in Metricflow format, if you haven't already. They should live in your dbt project's `models` directory.
1. `cd` into the newly cloned repo
1. Run `python3 -m pip install .`
1. `cd` back into the dbt project
1. Run `mf_to_zen --project_name .`
1. You should now see a `views` directory in your dbt project containing your Metricflow semantic models represented as Zenlytic views.

## To test
`pytest`