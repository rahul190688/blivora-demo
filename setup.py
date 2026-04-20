from setuptools import setup, find_packages

with open("requirements.txt") as f:
	requirements = f.read().splitlines()

setup(
	name="blivora_demo",
	version="0.0.1",
	description="Custom Ticketing System for Apex Analytix",
	author="Rahul Kumar",
	author_email="rk190688@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=requirements
)
