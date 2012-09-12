"""
MORSE
=====

__The Modular OpenRobots Simulation Engine__

MORSE is a Blender-based robotic simulator.
"""
import os
from setuptools import setup, find_packages, Extension
from subprocess import Popen, PIPE

def popcmd(cmd):
    """ Execute :param cmd: and return the first line from stdout """
    try:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        p.stderr.close()
        line = p.stdout.readlines()[0]
        if type(line) is str:
            return line.strip()
        else:
            return line.strip().decode(encoding='utf-8', errors='replace')
    except:
        return None

def get_version(path='src/morse/version.py'):
    """ Get git version from describe and write to :param path: """
    version = popcmd(['git', 'describe', '--abbrev=4'])
    if version:
        # Check if the repo is in sync with remote
        if popcmd(['git', 'diff-index', '--name-only', 'HEAD']):
            version += '-dirty'
        # Write in version.py
        with open(path, 'w') as f:
            f.write("VERSION = '%s'"%str(version))
        return version
    # if no git version available (tarball)
    # read from existing version.py file
    with open(path) as f:
        tmp = {}
        exec(f.read(), tmp)
        version = tmp['VERSION']
    return version

def get_data_files(dest_dir='share/morse/data', data_dir='data'):
    """ Build distutils/setuptools data_files by scanning :param data_dir: """
    dir_files = []
    data_files = []
    for f in os.listdir(data_dir):
        path = os.path.join(data_dir, f)
        if os.path.isfile(path):
            dir_files.append(path)
        else:
            data_files.extend(get_data_files(os.path.join(dest_dir, f), path))
    data_files.append((dest_dir, dir_files))
    return data_files

data_files = get_data_files('share/morse/data', 'data')
data_files.extend(get_data_files('share/morse/examples', 'examples'))
data_files.extend(get_data_files('share/morse/addons', 'addons'))

setup(
    name = 'MORSE',
    version = get_version(),
    packages = find_packages('src'),
    package_dir = {'morse': 'src/morse'},
    # Build our C modules
    ext_modules = [
        Extension('morse.modifiers.gaussian', ['src/morse/modifiers/gaussian.c']),
        Extension('morse.sensors.zBuffTo3D', ['src/morse/sensors/zBuffTo3Dmodule.c'])
    ],
    # TODO package_data requires data to be in the src/morse folder
    #package_data = {'': ['data/*/*.blend']},
    # distutils data_files seems to work with setuptools
    data_files = data_files,
    # Wrap morse.main.main in generated /usr/local/bin/morse script
    entry_points = {'console_scripts': ['morse = morse.main:main']},
    zip_safe = False,
    # Optional
    author = 'LAAS-CNRS',
    author_email = 'morse-dev@laas.fr',
    platforms = 'any',
    url = 'http://morse.openrobots.org',
    download_url = 'https://github.com/laas/morse',
    keywords = ['MORSE'],
    classifiers = [
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering"
    ],
    description = "The Modular OpenRobots Simulation Engine",
    long_description = __doc__,
    license = 'BSD'
)
