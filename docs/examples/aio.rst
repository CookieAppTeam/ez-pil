Asyncio Support
===========================
Demonstration on how to use the AioEditor to edit images asynchronously.

.. code-block:: python3

    from ez_pil import AioEditor

    editor = AioEditor(your_image)
    editor.rectangle((0, 0), width=100, height=100, color="black")

    img = await editor.execute() # returns Editor
    # now use `img` in the old way
