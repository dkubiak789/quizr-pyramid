import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'setuptools',
    'pyramid>=1.3',
    'SQLAlchemy',
    'transaction',
    'pyramid_chameleon',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_exclog',
    'zope.sqlalchemy',
    'pyramid_simpleform',
    'cryptacular',
    'waitress',
    'pycrypto',
    'webtest',
    ]

if sys.version_info[:3] < (2,5,0):
    raise RuntimeError('This application requires Python 2.6+')

setup(name='quizr',
      version='0.1.0',
      description='A quiz application (in Pyramid).',
      long_description=README,
      classifiers=[
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author="Wojciech Lichota",
      author_email="wojciech@lichota.pl",
      url='https://github.com/sargo/quizr-pyramid',
      license="MIT License",
      keywords='web wsgi pyramid quiz quizr',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='quizr.tests',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = quizr:main
      [console_scripts]
      initialize_quizr_db = quizr.scripts.initializedb:main
      """,
      )

