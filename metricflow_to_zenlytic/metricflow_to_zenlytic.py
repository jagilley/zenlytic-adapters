import yaml
from glob import glob
import argparse
import os
import re

parser = argparse.ArgumentParser(description='Convert Metricflow to Zenlytic.')
parser.add_argument('project_name', type=str, help='The name of the Metricflow project.')
args = parser.parse_args()

def convert_mf_yml_to_dict(yml_path):
    with open(yml_path, 'r') as stream:
        try:
            yaml_data = yaml.safe_load(stream)
            return yaml_data
        except yaml.YAMLError as exc:
            print(exc)
    return None

def extract_inner_text(s):
    match = re.search(r"ref\('(.*)'\)", s)
    if match:
        return match.group(1)
    return None

def mf_dict_to_zen_views(yaml_data):
    zen_fields = []
    for i, semantic_model in enumerate(yaml_data["semantic_models"]):
        zenlytic_data = {
            "fields": [],
            "identifiers": [],
        }

        # get view-level values
        zenlytic_data['name'] = yaml_data['semantic_models'][i]['name']
        zenlytic_data['description'] = yaml_data['semantic_models'][i]['description']
        zenlytic_data['default_date'] = yaml_data['semantic_models'][i]['defaults']['agg_time_dimension']

        zenlytic_data["model_name"] = extract_inner_text(yaml_data['semantic_models'][i]["model"])

        # dimensions to fields.dimensions
        for dimension in yaml_data['semantic_models'][i]["dimensions"]:
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
                if "agg_time_dimension" in metric:
                    metric_dict["canon_time"] = metric["agg_time_dimension"]
                if "meta" in metric:
                    metric_dict["extra"] = metric["meta"]

                zenlytic_data["fields"].append(metric_dict)

        # entities to identifiers
        for entity in yaml_data['semantic_models'][i]["entities"]:
            if "name" in entity:
                zenlytic_data["identifiers"].append({
                    "name": entity["name"],
                    "type": entity["type"] if entity["type"] != "unique" else "primary",
                    "sql": entity["expr"] if "expr" in entity else None,
                    # "type": entity["type"], # does not map 1:1
                })
        
        zen_fields.append(zenlytic_data)
    
    return zen_fields

def zen_views_to_yaml(zenlytic_data):
    views_dir = args.project_name + "/views"
    if not os.path.exists(views_dir):
        os.makedirs(views_dir)
    for zen_view in zenlytic_data:
        # write the yaml to views/model_name.yml
        with open(views_dir + "/" + zen_view["name"] + ".yml", 'w') as outfile:
            yaml.dump(zen_view, outfile, default_flow_style=False)

def main():
    # for each directory in project_name/models
    for model in glob(args.project_name + '/models/*/*.yml'):
        if "staging" in model:
            continue
        print(model)
        # convert the yaml to a dictionary
        mf_yml = convert_mf_yml_to_dict(model)
        # convert the dictionary to zenlytic views
        zen_views = mf_dict_to_zen_views(mf_yml)
        # convert the zenlytic views to yaml
        zen_views_to_yaml(zen_views)

if __name__=="__main__":
    main()