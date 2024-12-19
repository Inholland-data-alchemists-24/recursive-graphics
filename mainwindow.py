"""
Main module for the application.

This module initializes the main application window, sets up the canvas,
adds sliders for various parameters, and binds events for canvas zooming, sliders and fullscreen.
"""
import tkinter as tk

from draw_on_canvas import draw_squares
from sliders import create_sliders
from zoom import bind_canvas_zoom_events

# Main application window
# =======================
window = tk.Tk()
window.title("Fractal Matching Game")
window.grid_columnconfigure(0, weight=1)  # Make all elements of the 0th column of the main window expandable.
# Make the canvas' row expand to fill the window's height and resize with it, the sliders' row stays the same size.
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=0)

# Keybindings for the window to toggle fullscreen, exit fullscreen and quit the application
window.bind('<F11>', lambda event: (window.attributes("-fullscreen", True)))
window.bind('<Escape>', lambda event: (window.attributes("-fullscreen", False)))
window.bind('<Control-q>', lambda event: (window.quit()))

# Add a canvas for the fractal display
# ====================================
canvas_width, canvas_height = 500, 440  # canvas size determines the initial size of the window, which fits its content.
canvas = tk.Canvas(window, bg="white", width=canvas_width, height=canvas_height)
canvas.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="nsew")
bind_canvas_zoom_events(canvas)

# Demo of the zoom feature: draw squares on the canvas
draw_squares(canvas, 8, 50)

# Add a frame for the sliders below the canvas
# ============================================
slider_frame = tk.Frame(window)
slider_frame.grid(row=1, column=0, columnspan=1, padx=20, pady=(0, 6), sticky="ew")

# Create sliders for the fractal parameters and place in the frame
slider_data = [
    ("Trunk's Length", 10, 200, 1),
    ("Branch Splits", 2, 7, 1),
    ("Length Ratio", 0.2, 1.2, 0.01),
    ("Angle Between Branches", 0, 180, 1),
    ("Iterations", 1, 9, 1),
    ("Angle Offset", -45, 45, 1),
    ("Trunk's Color", 0, 360, 1),
    ("Leaf Color", 0, 360, 1)
]
# Enough to specify the number of columns for the sliders. This feature will help populating the sliders automatically.
create_sliders(slider_frame, slider_data, 2, 5, 6)

# Run the Tkinter event loop
# ==========================
window.mainloop()
window.destroy()  # Close the window after the event loop ends (on window.quit())
