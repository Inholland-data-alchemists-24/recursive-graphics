"""
Main module for the application.

This module initializes the main application window, sets up the canvas,
adds sliders for various parameters, and binds events for canvas zooming, sliders and fullscreen.
"""
import tkinter as tk

from draw_on_canvas import draw_squares
from sliders import (
    create_sliders, repopulate_sliders, calc_optimal_num_columns, calc_max_num_columns
)
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

# Set the initial, non-zoomed size of the window:
# Let the OS determine the initial size, or set it manually, e.g. 1200x720 pixels.
window.geometry("1200x720")
# to let the OS determine the initial size - comment the above line

# Initial fullscreen mode (to enable, uncomment one of the following):
# 1. fullscreen(with the top bar):
# window.state("zoomed")
# 2. fullscreen(without the top bar):
# window.attributes("-fullscreen", True)

# Add a canvas for the fractal display
# ====================================
canvas = tk.Canvas(window, bg="white")
canvas.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="nsew")
bind_canvas_zoom_events(canvas)

# Demo of the zoom feature: draw squares on the canvas
draw_squares(canvas, 8, 50)

# Add a frame for the sliders below the canvas
# ============================================
slider_frame = tk.Frame(window)
slider_frame.x_padding = 20  # CONFIG
slider_frame.grid(row=1, column=0, columnspan=1, padx=slider_frame.x_padding, pady=(0, 6), sticky="ew")

# CONFIG: Define parameters of each of the sliders
each_slider = {"x_padding": 0, "y_padding": 7, "minimum_width": 150}  # CONFIG
slider_data = [
    ("Trunk's Length", 10, 200, 1),
    ("Branch Splits", 2, 7, 1),
    ("Length Ratio", 0.2, 1.2, 0.01),
    ("Angle Between Branches", 0, 180, 1),
    ("Iterations", 1, 9, 1),
    ("Angle Offset", -45, 45, 1),
    ("Trunk's Color", 0, 360, 1),
    ("Leaf Color", 0, 360, 1)
] # CONFIG
num_sliders = len(slider_data)

# Get the rendered window width (works both with intrinsic or explicit window width)
window.update_idletasks()

# Calculate the number of sliders that can fit in a row
max_sliders_in_row = calc_max_num_columns(
    window.winfo_width(), slider_frame.x_padding, each_slider["minimum_width"], each_slider["x_padding"]
)
optimal_num_of_slider_columns = calc_optimal_num_columns(num_sliders, max_sliders_in_row)

# Create sliders with the initial layout
sliders = create_sliders(
    slider_frame, slider_data, optimal_num_of_slider_columns, each_slider["x_padding"], each_slider["y_padding"]
)

# Set up the response to resizing the window: rearranging the sliders
# ===================================================================
previous_window_width = window.winfo_width()

def on_window_config(event):
    global previous_window_width
    if previous_window_width == window.winfo_width():
        return
    previous_window_width = window.winfo_width()
    update_slider_frame()


def update_slider_frame():
    # Recalculate the number of columns based on the new window width
    global max_sliders_in_row, optimal_num_of_slider_columns
    max_sliders_in_row = calc_max_num_columns(
        window.winfo_width(), slider_frame.x_padding, each_slider["minimum_width"], each_slider["x_padding"]
    )
    optimal_num_of_slider_columns = calc_optimal_num_columns(num_sliders, max_sliders_in_row)
    if optimal_num_of_slider_columns == slider_frame.grid_size()[0]:
        return
    if optimal_num_of_slider_columns > slider_frame.grid_size()[0]:
        for i in range(slider_frame.grid_size()[0], optimal_num_of_slider_columns):
            slider_frame.columnconfigure(i, weight=1)
    elif optimal_num_of_slider_columns < slider_frame.grid_size()[0]:
        for i in range(optimal_num_of_slider_columns, slider_frame.grid_size()[0]):
            slider_frame.columnconfigure(i, weight=0)
    # Repopulate all sliders
    repopulate_sliders(sliders, optimal_num_of_slider_columns)


# Handle window resizing: bind the window configure event to the handler `on_window_config`.
window.bind('<Configure>', on_window_config)

# Run the Tkinter event loop
# ==========================
window.mainloop()
window.destroy()  # Close the window after the event loop ends (on window.quit())
