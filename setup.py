from setuptools import setup, find_packages

setup(
    name='difoss_pyutil',
    version='0.1.4',
    py_modules=['difoss_pyutil'],
    packages=find_packages(),
    install_requires=[
        'Click',
        'GitPython',
    ],
    entry_points={
        'console_scripts': {
            "df.cmd = difoss_pyutil.__main__:main"
        },
    },
)
