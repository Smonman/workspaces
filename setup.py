from setuptools import setup


def readfile(filename):
    with open(filename, "r+") as f:
        return f.read()


setup(
    name="workspaces",
    version="1.0.0",
    packages=[""],
    url="https://github.com/Smonman/workspaces",
    license=readfile("LICENSE"),
    author="Simon Josef Kreuzpointner",
    author_email="simonkreuzpointner@gmail.com",
    description="Let's you set up workspaces, which can then be opened in the blink of an eye.",
    long_description=readfile("README.md"),
    scripts=["workspaces.py"],
    entry_points={
        "console_scripts": [
            "workspaces = workspaces:main"
        ]
    },
)
