"""
Main module for the application.

This module initializes the main application window, sets up the canvas,
adds sliders for various parameters, and binds events for canvas zooming, sliders and fullscreen.
"""
import tkinter as tk

from sliders import create_sliders

# Main application window
# =======================
window = tk.Tk()
window.title("Fractal Matching Game")
window.grid_columnconfigure(0, weight=1)  # Make all elements of the 0th column of the main window expandable.
# Make the canvas' row expand to fill the window's height and resize with it, the sliders' row stays the same size.
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=0)

# Add a canvas for the fractal display
# ====================================
canvas_width, canvas_height = 500, 440  # canvas size determines the initial size of the window, which fits its content.
canvas = tk.Canvas(window, bg="white", width=canvas_width, height=canvas_height)
canvas.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="nsew")

# Add a frame for the sliders below the canvas
# ============================================
slider_frame = tk.Frame(window)
slider_frame.grid(row=1, column=0, columnspan=1, padx=20, pady=(0, 6), sticky="ew")

# Create sliders for the fractal parameters and place in the frame
# length of each slider: (canvas' width - frame's x padding) // num of sliders in a row - slider's x padding
# (500 - 2*20) // 2 - 10 = 220
create_sliders(slider_frame, 5, 6)

# Run the Tkinter event loop
# ==========================
window.mainloop()
window.destroy()  # Close the window after the event loop ends (on window.quit())
