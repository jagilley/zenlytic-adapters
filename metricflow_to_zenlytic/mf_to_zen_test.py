from .metricflow_to_zenlytic import convert_mf_yml_to_dict, mf_dict_to_zen_views, zen_views_to_yaml
import yaml
import os

def test_main():
    test_mf_yml = "metricflow_to_zenlytic/examples/metricflow/customers.yml"
    test_zen_yml = "metricflow_to_zenlytic/examples/zenlytic/views/customers.yml"

    # convert the yaml to a dictionary
    mf_yml = convert_mf_yml_to_dict(test_mf_yml)
    # convert the dictionary to zenlytic views
    zen_views = mf_dict_to_zen_views(mf_yml)
    # convert the zenlytic views to yaml
    views = zen_views_to_yaml(zen_views, "examples/zenlytic", write_to_file=False)

    # read test_zen_yml
    with open(test_zen_yml, 'r') as f:
        zen_yml = f.read()

    # assert that zen_yml equals one of the views
    print(zen_yml)
    print("---")
    print(views[0])
    assert zen_yml in views

if __name__=="__main__":
    test_main()