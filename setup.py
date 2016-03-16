from setuptools import setup

setup(
    name='taxtool',
    version='0.0.1',
    packages=['complex', 'complex.commands'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        taxtool=complex.cli:cli
    ''',
)
