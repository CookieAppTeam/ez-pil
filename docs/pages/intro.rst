Introduction
============
This is the documentation for ez-pil, A python library built on top of PIL to easily edit images.

Prerequisties
-------------
Python 3.9 or higher is required.

Installing
-----------

Install directly from PyPI: ::

    python3 -m pip install -U ez-pil

If you are using Windows, then the following should be used instead: ::

    py -3 -m pip install -U ez-pil

Basic Concepts
--------------
A quick example of how ez-pil works

.. code-block:: python3

    from ez_pil import Editor, Canvas

    board = Canvas(width=500, height=500)
    editor = Editor(board)

    editor.text((10, 10), "Hello World")
    editor.show() # .save() to save the image
