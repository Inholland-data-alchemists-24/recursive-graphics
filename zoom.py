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
from tkinter import messagebox

# Global variables
zoom_count = 0
MAX_ZOOM = 7
season_changed = False  # New global flag to track if season was changed

def start_pan(event: tk.Event):
    """Marks the starting point for panning."""
    canvas: tk.Canvas = event.widget
    canvas.scan_mark(event.x, event.y)


def do_pan(event: tk.Event):
    """Drags the canvas to the new position."""
    canvas: tk.Canvas = event.widget
    canvas.scan_dragto(event.x, event.y, gain=1)


def reset_zoom(canvas: tk.Canvas):
    """Resets the canvas zoom to its default state and resets zoom count."""
    global zoom_count
    canvas.scale("all", 0, 0, 1.0, 1.0)  # Reset scale
    canvas.configure(scrollregion=canvas.bbox("all"))  # Reset view to include all items
    zoom_count = 0  # Reset zoom count

def zoom(event: tk.Event):
    """Zooms in or out on the canvas, with a limit."""
    global zoom_count, season_changed
    canvas: tk.Canvas = event.widget  # Get the canvas instance from the event

    # If a season change occurred, reset zoom
    if season_changed:
        reset_zoom(canvas)  # Reset zoom to default
        season_changed = False  # Reset the flag
        return

    # Check if zoom limit is reached
    if zoom_count >= MAX_ZOOM and event.delta > 0:
        messagebox.showwarning("Zoom Limit Reached", "You can't zoom in more than 7 times.")
        return
    elif zoom_count <= -MAX_ZOOM and event.delta < 0:
        messagebox.showwarning("Zoom Limit Reached", "You can't zoom out more than 7 times.")
        return

    # Zoom in or out
    scale = 1.1 if event.delta > 0 else 0.9
    canvas.scale("all", canvas.canvasx(event.x), canvas.canvasy(event.y), scale, scale)

    # Update zoom count
    zoom_count += 1 if event.delta > 0 else -1

def bind_canvas_zoom_events(canvas: tk.Canvas):
    """
    Binds mouse events to the pan and zoom events on the canvas.
    """
    canvas.bind("<MouseWheel>", zoom)
    canvas.bind("<ButtonPress-1>", start_pan)
    canvas.bind("<B1-Motion>", do_pan)
