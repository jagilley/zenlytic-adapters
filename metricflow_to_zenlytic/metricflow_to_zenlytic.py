import yaml
from glob import glob
import argparse
import os

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

        map = {
            "semantic_models.name": "name",
            "semantic_models.description": "description",
            # "semantic_models.model": None,
        }

        zenlytic_data = {
            "fields": [],
            "identifiers": [],
        }

        # map yaml to zenlytic
        for key, value in map.items():
            keys = key.split(".")
            for semantic_model in yaml_data[keys[0]]:
                if keys[1] in semantic_model and value is not None:
                    zenlytic_data[value] = semantic_model[value].strip()
                else:
                    zenlytic_data[value] = None

        # dimensions to fields.dimensions
        for dimension in yaml_data["semantic_models"][0]["dimensions"]:
            field_dict = {
                "name": dimension["name"],
                "sql": dimension["expr"] if "expr" in dimension else None,
            }
            if dimension['type'] == "time":
                field_dict["field_type"] = "dimension_group"
                field_dict["type"] = "time"
            elif dimension["type"] == "categorical":
                field_dict["field_type"] = "dimension"
                field_dict["type"] = "string"

            # handle mf type_params?
            zenlytic_data["fields"].append(field_dict)

        # metrics to measures
        if "metrics" in yaml_data:
            for metric in yaml_data["metrics"]:
                metric_dict = {
                    "name": metric["name"],
                    "field_type": "measure",
                    "sql": metric["expr"] if "expr" in metric else None,
                    "type": metric["agg"] if "agg" in metric else None, # not all types map 1:1
                    "label": metric["label"],
                }

                zenlytic_data["fields"].append(metric_dict)

        # entities to identifiers
        for entity in yaml_data["semantic_models"][0]["entities"]:
            if "name" in entity:
                zenlytic_data["identifiers"].append({
                    "name": entity["name"],
                    "type": entity["type"] if entity["type"] != "unique" else "primary",
                    "sql": entity["expr"] if "expr" in entity else None,
                    # "type": entity["type"], # does not map 1:1
                })

        # print(zenlytic_data)

        # convert zenlytic data to yaml
        zenlytic_yaml = yaml.dump(zenlytic_data)

        return zenlytic_yaml
    
    # for each directory in project_name/models
    for model in glob(args.project_name + '/models/*/*.yml'):
        if "staging" in model:
            continue
        print(model)
        zen_yml = convert_yml(model)
        # make a directory called views, if it doesn't already exist
        views_dir = args.project_name + "/views"
        if not os.path.exists(views_dir):
            os.makedirs(views_dir)
        # write the yaml to views/model_name.yml
        with open(views_dir + "/" + (os.path.basename(model).split(".yml")[0] + "_view.yml"), "w") as f:
            f.write(zen_yml)

if __name__=="__main__":
    main()