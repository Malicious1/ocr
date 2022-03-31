# Required for editable installs
# https://discuss.python.org/t/specification-of-editable-installation/1564/
import setuptools

setuptools.setup(name='app', version='1.0',
                 packages= setuptools.find_packages(
                     include=["app", "app*", "evaluation"]
                 ),
                 include_package_data=True,)
