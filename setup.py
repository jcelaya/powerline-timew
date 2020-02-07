# vim:fileencoding=utf-8:noet

from setuptools import setup

setup(
    name         = 'powerline-timew',
    description  = 'A Powerline segment for showing the time spent today in a task',
    version      = '0.1',
    keywords     = 'powerline timew',
    license      = 'MIT',
    author       = 'Javier Celaya',
    author_email = 'jcelaya@gmail.com',
    url          = 'https://github.com/jcelaya/powerline-timew',
    packages     = ['powerline_timew'],
    classifiers  = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Terminals'
    ]
)
