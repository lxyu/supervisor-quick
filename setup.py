from setuptools import setup

setup(
    name="supervisor-quick",
    version="0.1.4",
    description="Bypass supervisor's nasty callbacks stack and make it quick!",
    author="Lx Yu",
    author_email="i@lxyu.net",
    py_modules=["supervisor_quick", ],
    package_data={"": ["LICENSE"], },
    url="http://lxyu.github.io/supervisor-quick/",
    license="MIT",
    long_description=open("README.rst").read(),
    install_requires=[
        "supervisor",
    ],
)
