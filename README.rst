==============
click-skeleton
==============
+---------------+-----------------+
|     Tools     |      Result     |
+===============+=================+
|     Coverage  |   |coverage|    |
+---------------+-----------------+

.. |coverage| image:: https://github.com/AdrienPensart/click-skeleton/blob/master/doc/coverage.svg
   :alt: Coverage badge

Description
-----------
Library to build a CLI with a well defined skeleton and helpers, including :

- completion
- real --help eagerness
- help and version colors
- readme generation
- -V / --version / version subcommand
- -h / --help / help subcommand
- subgroup creation and registering made easier

EXAMPLE CLI
-----------


Commands
--------
.. code-block::

  Usage: example-cli [OPTIONS] COMMAND [ARGS]...

    Simple CLI example

  Options:
    --global-example TEXT  A global option
    --option-one TEXT      First option
    --option-two TEXT      Second option
    -V, --version          Show the version and exit.
    -h, --help             Show this message and exit.

  Commands:
    abort                      Generates an exception
    expanded-path              Expand option path
    help                       Print help
    readme (doc)               Generates a README.rst
    subgroup (subgroup-alias)  A sub group
    version                    Print version

example-cli abort
*****************
.. code-block::

  Usage: example-cli abort [OPTIONS]

    Generates an exception on purpose (test)

  Options:
    -h, --help  Show this message and exit.

example-cli expanded-path
*************************
.. code-block::

  Usage: example-cli expanded-path [OPTIONS]

    Command with expanded path option

  Options:
    --file PATH  File path which expands
    -h, --help   Show this message and exit.

example-cli help
****************
.. code-block::

  Usage: example-cli help [OPTIONS]

    Print help

  Options:
    -h, --help  Show this message and exit.

example-cli readme
******************
.. code-block::

  Usage: example-cli readme [OPTIONS]

    Uses gen_doc click-skeleton helper to generates a complete readme

  Options:
    --output [rst|markdown]  README output format  [default: rst]
    -h, --help               Show this message and exit.

example-cli subgroup
********************
.. code-block::

  Usage: example-cli subgroup [OPTIONS] COMMAND [ARGS]...

    I am a subgroup!

  Options:
    -h, --help  Show this message and exit.

  Commands:
    help        Print help
    subcommand  A sub command

example-cli subgroup subcommand
*******************************
.. code-block::

  Usage: example-cli subgroup subcommand [OPTIONS]

    I am a subcommand!

  Options:
    --myoptions TEXT  A splitted option
    -h, --help        Show this message and exit.

example-cli version
*******************
.. code-block::

  Usage: example-cli version [OPTIONS]

    Print version, equivalent to -V and --version

  Options:
    -h, --help  Show this message and exit.
