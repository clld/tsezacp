from setuptools import setup, find_packages

requires = [
    'clld',
    'clldmpg',
    ]

setup(name='tsezacp',
      version='0.0',
      description='tsezacp',
      long_description='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="tsezacp",
      entry_points="""\
[paste.app_factory]
main = tsezacp:main
""",
      )
