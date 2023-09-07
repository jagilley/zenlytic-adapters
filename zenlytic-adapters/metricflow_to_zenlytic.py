import yaml

with open("zenlytic-adapters/examples/metricflow/revenue.yml", 'r') as stream:
    try:
        yaml_data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print(yaml_data)
# {'semantic_models': [{'name': 'orders', 'description': 'A model containing order data. The grain of the table is the order id.\n', 

map = {
    "semantic_models.name": "name",
    "semantic_models.description": "description",
}

zenlytic_data = {}

for key, value in map.items():
    keys = key.split(".")
    for semantic_model in yaml_data[keys[0]]:
        if keys[1] in semantic_model:
            zenlytic_data[value] = semantic_model[value]

print(zenlytic_data)