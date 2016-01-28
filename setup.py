from setuptools import setup,find_packages
try:
    import pypandoc
    description = pypandoc.convert('tgbot/README.md','rst')
except (IOError, ImportError):
    description = ''
requirements = ["uwsgidecorators >= 1.1.0","requests >= 2.7.0",
                        "pytz >= 2015.4","feedparser >= 5.2.1",
                        "redis >= 2.10.3","setuptools >= 18.3.1"]
setup(name="tgbot",
      version = "0.32",
      description="Framework to build a Telegram Bot based on a UWSGI Server",
      author="Thomas Eberle",
      author_email="Thomas@tommyelroy.com",
      url="https://github.com/T-Eberle/tgbot/",
      license="The MIT License (MIT)",
      keywords="tgbot bot",
      packages=find_packages(exclude=["example","dist"]),
      package_data ={"":["*.ini","*.md","*.txt"]},
      long_description=description,
      install_requires=requirements,
      setup_requires=requirements,
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Operating System :: Unix",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Topic :: Internet :: WWW/HTTP :: WSGI :: Server"]
      )