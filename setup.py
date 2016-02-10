import os
from distutils.core import setup

# Get version and release info, which is all stored in shablona/version.py
ver_file = os.path.join('shablona', 'version.py')
with open(ver_file) as f:
    exec(f.read())

opts = dict(name="John",
            maintainer="my project for UWSEDS",
            packages=['myproject','myproject.tests'],


if __name__ == '__main__':
    setup(**opts)
