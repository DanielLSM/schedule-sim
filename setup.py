import re
from setuptools import setup, find_packages
import sys

if sys.version_info.major != 3:
    print('This Python is only compatible with Python 3, but you are running '
          'Python {}. The installation will likely fail.'.format(
              sys.version_info.major))

setup(
    name='schedule-sim',
    packages=[
        package for package in find_packages()
        if package.startswith('baselines')
    ],
    install_requires=[
        'gym', 'pyyaml', 'tqdm', 'joblib', 'dill', 'progressbar2',
        'cloudpickle', 'pyglet'
    ],
    description=
    'A simple simulation for scheduling in markov decision processes',
    author='Daniel',
    url='https://github.com/DanielLSM/schedule-sim/',
    author_email='daniellsmarta@gmail.com',
    version='0.1.5')

# ensure there is some tensorflow build with version above 1.4
import pkg_resources
tf_pkg = None
for tf_pkg_name in [
        'tensorflow', 'tensorflow-gpu', 'tf-nightly', 'tf-nightly-gpu'
]:
    try:
        tf_pkg = pkg_resources.get_distribution(tf_pkg_name)
    except pkg_resources.DistributionNotFound:
        pass
assert tf_pkg is not None, 'TensorFlow needed, of version above 1.4'
from distutils.version import LooseVersion
assert LooseVersion(re.sub(r'-?rc\d+$', '',
                           tf_pkg.version)) >= LooseVersion('1.4.0')
