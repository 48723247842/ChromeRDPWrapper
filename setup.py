import setuptools
import pathlib
import pkg_resources

# pipreqs ./chrome_rdp_wrapper

# https://stackoverflow.com/a/59971469
with pathlib.Path('./chrome_rdp_wrapper/requirements.txt').open() as requirements_txt:
	install_requires = [
		str(requirement)
		for requirement
		in pkg_resources.parse_requirements(requirements_txt)
	]

setuptools.setup(
	name="chrome_rdp_wrapper",
	version="0.0.2",
	author="7435171",
	author_email="48723247842@protonmail.com",
	description="Chrome RDP Wrapper",
	url="https://github.com/48723247842/ChromeRDPWrapper",
	packages=setuptools.find_packages() ,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.8',
	install_requires=install_requires
)