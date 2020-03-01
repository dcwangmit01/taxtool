from setuptools import setup

setup(
    name='taxtool',
    version='0.1.0',
    packages=['taxtool', 'taxtool.commands'],
    include_package_data=True,
    install_requires=[
        'click',
        'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        taxtool=taxtool.cli:cli
    ''', )
