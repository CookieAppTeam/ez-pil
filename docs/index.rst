Welcome to EzPIL!
====================================
A python library built on top of PIL to easily edit images.

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Contents

   pages/aio
   ez_pil/modules
   examples/index


Installing
-----------
Python 3.12 or higher is required.

.. code-block::

    pip install ez-pil

Examples
--------
A quick example of how ez-pil works. For more examples, check the :doc:`examples <examples/index>` section.

.. code-block:: python3

    from ez_pil import Editor, Canvas

    board = Canvas(width=500, height=500)
    editor = Editor(board)

    editor.text((10, 10), "Hello World")
    editor.show() # .save() to save the image
