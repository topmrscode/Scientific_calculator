from setuptools import setup, find_packages
setup(
    name='My Calculator',
    version='1.0',
    description='Phyton 3 Calculator with GUI (Tkinter)',
    author='Laura Baudean',
    author_email='laura.baudean@epitech.eu',
    package_dir={'': 'src'},
    packages = find_packages(), # sert a trouver les differents librairies que l on va importer pour notre projet dans notre ordi
    python_requires='>=2.7, >=3.5',

    use_2to3=True, # permet de convertir python 2 a python 3
)
