from setuptools import setup, find_packages
import os

version = '3.0pre-alpha'

setup(name='bika.lims',
      version=version,
      description="Bika LIMS",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='bika LIMS',
      author='Bika',
      author_email='support@bikalabs.com',
      url='www.bikalabs.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bika'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.ATExtensions',
          'Products.CMFEditions',
          'plone.app.iterate',
          'reportlab',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
