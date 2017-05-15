Release Notes
-------------

1.5.0 (2017-05-15)
------------------

* Add environment variables for GitLab CI.

  * Thanks to `@tinproject <https://github.com/tinproject>`_ for the PR

1.4.0 (2017-05-04)
------------------

* Allow additional metadata to be specified on the command-line.

  * Thanks to `@BeyondEvil <https://github.com/BeyondEvil>`_ for the PR

1.3.0 (2017-03-01)
------------------

* Display initial metadata in report header.
* Update metadata when running with xdist processes instead of overwriting.

1.2.0 (2017-02-24)
------------------

* Added environment variables for AppVeyor and CircleCI.
* Try to run ``pytest_configure`` first so that other plugins can contribute to
  the metadata.

1.1.0 (2017-02-16)
------------------

* Moved pytest related packages into 'Packages' as a dictionary.
* Changed installed plugins from a list to a dictionary.

1.0.0 (2017-02-16)
------------------

* Initial release
