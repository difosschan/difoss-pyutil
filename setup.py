try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='difoss_pyutil',
    version='0.1.3',
    py_modules=['difoss_pyutil'],
    packages=find_packages(exclude=['build',]),
    install_requires=[
        'Click',
        'GitPython',
    ],
    entry_points={
        'console_scripts': {
            "my.diff = main:cmd_diff",
            "df.cmd = main:main"
        },
    },
)
