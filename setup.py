from setuptools import setup, find_packages

setup(
    name='django-debug-logging',
    version=__import__('debug_logging').__version__,
    description='A plugin for django_debug_toolbar that logs results to the database for aggregated review.',
    long_description=open('README.rst').read(),
    author='Brandon Konkle',
    author_email='brandon@lincolnloop.com',
    url='http://lincolnloop.github.com/django-debug-logging/',
    download_url='http://github.com/lincolnloop/django-debug-logging/downloads',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
    install_requires=['django-debug-toolbar', 'nexus'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
