dcclog
======

``dcclog`` is a simple wrapper around the python logging module that makes it easy to colorize and encrypt log messages.

Installation
============

From pypi:
~~~~~~~~~~

.. code-block:: console

    $ pip install dcclog

with built-in ciphers:
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    $ pip install 'dcclog[cipher]'

From github:
~~~~~~~~~~~~

.. code-block:: console

    $ git clone https://github.com/jamazi/dcclog.git
    $ cd dcclog
    $ pip install '.[all]'

How To use dcclog
==================

.. code-block:: python

    import dcclog

    dcclog.default_config()
    logger = dcclog.getLogger(name=__name__)

    logger.error("error message.")
    logger.warning("warning message.")
    logger.info("info message.")
    logger.debug("debug message.")


    @dcclog.log
    def logged_function(x: int, y: int) -> int:
        return x + y


    logged_function(4, 6)



or with RSA encryption:

.. code-block:: python

    import dcclog
    from dcclog.cipher.rsa import RSAEncryption

    dcclog.default_config(
        level=dcclog.INFO,
        filename=".logs/app.log",
        cipher=RSAEncryption("pubkey.pem"),
    )
    logger = dcclog.getLogger(name=__name__)

    logger.error("error message.")
    logger.warning("warning message.")
    logger.info("info message.")
    logger.debug("debug message.")


    @dcclog.log
    def logged_function(x: int, y: int) -> int:
        return x + y


    logged_function(4, 6)