from setuptools import setup

setup(
    name='forja',
    version='0.0.1',
    packages=['forja'],
    entry_points={
        'console_scripts': ['forja = forja.__main__:main']
        },
    )

