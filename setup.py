from setuptools import setup, find_packages

setup(
    name='difoss-pyutil',
    version='0.1.0',
    packages=[*find_packages(), '.'],
    install_requires=[
        'Click',
        'GitPython',
    ],
    entry_points={
        'console_scripts': {
            "my.diff=diff:dir_diff",
            "dfpy=diff:main"
        },
    },
)
