import yaml
from glob import glob

project_name = 'jaffle-sl-template'


def convert_yml(yml_path):
    with open(yml_path, 'r') as stream:
        try:
            yaml_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # print(yaml_data)
    # {'semantic_models': [{'name': 'orders', 'description': 'A model containing order data. The grain of the table is the order id.\n', 

    map = {
        "semantic_models.name": "name",
        "semantic_models.description": "description",
        "semantic_models.model": None,
    }

    zenlytic_data = {
        "fields": [],
    }

    for key, value in map.items():
        keys = key.split(".")
        for semantic_model in yaml_data[keys[0]]:
            if keys[1] in semantic_model and value is not None:
                zenlytic_data[value] = semantic_model[value]

    # handle dimensions
    for dimension in yaml_data["semantic_models"][0]["dimensions"]:
        if "name" in dimension:
            zenlytic_data["fields"].append({
                "name": dimension["name"],
                "field_type": "dimension",
                "sql": dimension["expr"] if "expr" in dimension else None,
                # "type": dimension["type"], # does not map 1:1
            })

    print(zenlytic_data)

    # convert zenlytic data to yaml
    zenlytic_yaml = yaml.dump(zenlytic_data)

    print(zenlytic_yaml)

# for each directory in project_name/models
for model in glob(project_name + '/models/*/*.yml'):
    if "staging" in model:
        continue
    print(model)
    convert_yml(model)