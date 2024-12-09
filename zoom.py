"""
Zoom
====
Module provides zoom functionality for a tkinter canvas.

This module includes callbacks (functions) to start panning, perform panning, and zoom in/out on a tkinter canvas.
It also includes a function to bind these events to the canvas.

Functions:
        start_pan(event): Marks the starting point for panning.
        do_pan(event): Drags the canvas to the new position.
        zoom(event): Zooms in or out on the canvas.
        bind_canvas_zoom_events(canvas): Binds the pan and zoom events to the canvas.

Example:
    import tkinter as tk
    from gui import bind_canvas_zoom_events

    # Create a tkinter window and canvas
    window = tk.Tk()
    canvas = tk.Canvas(window, bg="white", width=600, height=450)
    canvas.pack() # or grid(....)

    # Set the canvas and bind events
    bind_canvas_zoom_events(canvas)

    # Run the tkinter event loop
    window.mainloop()
"""
import tkinter as tk


def start_pan(event: tk.Event):
    """Marks the starting point for panning."""
    canvas: tk.Canvas = event.widget
    canvas.scan_mark(event.x, event.y)


def do_pan(event: tk.Event):
    """Drags the canvas to the new position."""
    canvas: tk.Canvas = event.widget
    canvas.scan_dragto(event.x, event.y, gain=1)


def zoom(event: tk.Event):
    """Zooms in or out on the canvas."""
    canvas: tk.Canvas = event.widget
    scale = 1.1 if event.delta > 0 else 0.9
    canvas.scale("all", canvas.canvasx(event.x), canvas.canvasy(event.y), scale, scale)


def bind_canvas_zoom_events(canvas: tk.Canvas):
    """
    Binds mouse events to the pan and zoom events on the canvas.
    """
    canvas.bind("<MouseWheel>", zoom)
    canvas.bind("<ButtonPress-1>", start_pan)
    canvas.bind("<B1-Motion>", do_pan)
