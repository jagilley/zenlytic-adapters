import pytest
from .metricflow_to_zenlytic import convert_mf_yml_to_dict, mf_dict_to_zen_views, zen_views_to_yaml
import yaml
import os

@pytest.fixture
def metricflow_path():
    return "metricflow_to_zenlytic/examples/metricflow/"

@pytest.fixture
def zenlytic_path():
    return "metricflow_to_zenlytic/examples/zenlytic/"

def conversion(metricflow_path, zenlytic_path):
    # convert the yaml to a dictionary
    mf_yml = convert_mf_yml_to_dict(metricflow_path)
    # convert the dictionary to zenlytic views
    zen_views = mf_dict_to_zen_views(mf_yml)
    # convert the zenlytic views to yaml
    views = zen_views_to_yaml(zen_views, "examples/zenlytic", write_to_file=False)

    # read test_zen_yml
    with open(zenlytic_path, 'r') as f:
        zen_yml = f.read()

    # assert that zen_yml equals one of the views
    print(zen_yml)
    print("---")
    print(views[0])
    assert zen_yml in views

@pytest.mark.parametrize("metricflow_file, zenlytic_file", [
    ("customers.yml", "views/customers.yml"),
    ("orders.yml", "views/orders.yml"),
    ("order_items.yml", "views/order_items.yml"),
    ("revenue.yml", "views/revenue.yml")
])
def test_all_conversions(metricflow_path, zenlytic_path, metricflow_file, zenlytic_file):
    conversion(metricflow_path + metricflow_file, zenlytic_path + zenlytic_file)