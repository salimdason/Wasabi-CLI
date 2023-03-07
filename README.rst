=========
WasabiCLI
=========


.. image:: https://img.shields.io/pypi/v/wasabicli.svg
        :target: https://pypi.python.org/pypi/wasabicli

.. image:: https://img.shields.io/travis/salimdason/wasabicli.svg
        :target: https://travis-ci.com/salimdason/wasabicli

.. image:: https://readthedocs.org/projects/wasabicli/badge/?version=latest
        :target: https://wasabicli.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



.. image:: https://pyup.io/repos/github/salimdason/wasabicli/shield.svg
     :target: https://pyup.io/repos/github/salimdason/wasabicli/
     :alt: Updates



CLI application for management of versioned Wasabi S3 buckets. This should also in theory work for AWS S3 buckets.



* Free software: GNU General Public License v3
* Documentation: https://wasabi-cli.readthedocs.io/en/latest/index.html



Features
--------
1. Delete only non-current objects
2. Delete both current and non-current objects
3. Purge delete markers from bucket
4. Delete bucket (Runs all commands above to ensure bucket is empty before deletion)

