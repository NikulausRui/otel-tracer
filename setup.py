import ssl
import os.path
from setuptools import setup, find_packages

script_path = os.path.dirname(__file__)

requirment_path = os.path.join(script_path, 'requirements.txt')
with open(requirment_path, 'r') as f:
    install_requires = f.read().splitlines()

try:
    _create_unverified_https_context = ssl._create_unverified_context

except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

setup(
    include_package_data=True,
    packages=find_packages(),
    install_requires=install_requires,
    name='otel_tracer',
    version='0.0.1',
    description="common python utilities for VxRail",
    author="VxRail",
    license="ToBeDone",
    long_description="""
    otel tracing
    """,
    platforms="python3",
)
