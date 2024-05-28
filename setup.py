from setuptools import setup

INSTALL_REQUIRES = [
    'numpy>=1.25.2',
    'pandas>=2.0.3',
    'opencv-python>=4.8.0',
]
PACKAGES = ['akikenTools']
PACKAGES_DIR = {'akikenTools': 'src/akikenTools'}
CLASSIFIERS = [
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
]

setup(
    name='akikenTools',
    author='Toma Nagano',
    author_email='res.t.nagano@gmail.com',
    description='This is Akiyama laboratory ( in National Institute of Technology Nagano College ) toolbox library.',
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    version='1.0.0',
    python_requires='>=3.10.12',
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    package_dir=PACKAGES_DIR,
    classifiers=CLASSIFIERS
)
