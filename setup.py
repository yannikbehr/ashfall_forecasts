from setuptools import setup, find_packages

####################################################################
#                    CONFIGURATION
####################################################################

# do the build/install
setup(
    name="lh_sampling",
    version="0.0.1",
    description="Python package to Latin Hypercube samples.",
    long_description="Python package to compute Latin Hypercube samples.",
    author="Yannik Behr",
    author_email="y.behr@gns.cri.nz",
    url="",
    license="GPL v3",
    package_dir={'': 'src'},
    packages=['lh_sampling'],
    package_data={'lh_sampling': ['data/*.csv']},
)
