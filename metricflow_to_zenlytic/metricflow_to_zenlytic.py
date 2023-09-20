import yaml
from glob import glob
import argparse

def main():
    parser = argparse.ArgumentParser(description='Convert Metricflow to Zenlytic.')
    parser.add_argument('project_name', type=str, help='The name of the Metricflow project.')
    args = parser.parse_args()

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

        # map yaml to zenlytic
        for key, value in map.items():
            keys = key.split(".")
            for semantic_model in yaml_data[keys[0]]:
                if keys[1] in semantic_model and value is not None:
                    zenlytic_data[value] = semantic_model[value]

        # dimensions to fields
        for dimension in yaml_data["semantic_models"][0]["dimensions"]:
            if "name" in dimension:
                zenlytic_data["fields"].append({
                    "name": dimension["name"],
                    "field_type": "dimension",
                    "sql": dimension["expr"] if "expr" in dimension else None,
                    # "type": dimension["type"], # does not map 1:1
                })

        # metrics to measures
        for metric in yaml_data["metrics"]:
            if "name" in metric:
                zenlytic_data["fields"].append({
                    "name": metric["name"],
                    "field_type": "measure",
                    "sql": metric["expr"] if "expr" in metric else None,
                    # "type": metric["type"], # does not map 1:1
                })

        print(zenlytic_data)

        # convert zenlytic data to yaml
        zenlytic_yaml = yaml.dump(zenlytic_data)

        print(zenlytic_yaml)
    
    # for each directory in project_name/models
    for model in glob(args.project_name + '/models/*/*.yml'):
        if "staging" in model:
            continue
        print(model)
        convert_yml(model)

if __name__=="__main__":
    main()