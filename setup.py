from setuptools import setup, find_packages
import os

version = '0.1a1'

setup(name='mutt-atlassian',
      version=version,
      description="Integrations of Atlassian products (JIRA, Confluence) for Mutt.",
      # long_description=open("README.txt").read() + "\n" +
      #                  open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='mutt atlassian jira confluence',
      author='Andreas Schiweck',
      author_email='github@rainrider.de',
      url='https://github.com/aschiweck/mutt-atlassian',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['mutt'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'html2text',
          'jira',
          'requests_kerberos',
      ],
      entry_points={
          'console_scripts': [
              'mutt2jira=mutt.atlassian.scripts.mutt2jira:main'
          ],
      }
)
