from setuptools import setup, find_packages

setup(
    name='metricflow_to_zenlytic',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mf_to_zen = metricflow_to_zenlytic.metricflow_to_zenlytic:main',
        ],
    },
)