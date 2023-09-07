import yaml

with open("zenlytic-adapters/examples/metricflow/revenue.yml", 'r') as stream:
    try:
        yaml_data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print(yaml_data)