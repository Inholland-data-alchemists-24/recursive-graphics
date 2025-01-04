import tkinter as tk
from fractal_funcs import fractal_canopy
from zoom import bind_canvas_zoom_events

def center_window_on_screen(window_: tk.Tk | tk.Toplevel) -> None:
    window_.update_idletasks()
    screen_width = window_.winfo_screenwidth()  # the width of the screen
    screen_height = window_.winfo_screenheight()  # the height of the screen
    width = window_.winfo_width()  # the width of the window
    height = window_.winfo_height()  # the height of the window
    # Calculate the center of the screen and position top-left corner of the window
    x = (screen_width // 2) - (width // 2)  # position left-side of the window
    y = (screen_height // 2) - (height // 2) - 16  # position top of the window adjusted for the height of the taskbar.
    window_.geometry(f'{width}x{height}+{x}+{y}')

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

center_window_on_screen(window)

    # Add a canvas for the fractal display
    # ====================================
canvas = tk.Canvas(window, bg="white")
canvas.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky="nsew")
bind_canvas_zoom_events(canvas)

# Demo of the zoom feature: draw squares on the canvas
color_tuple = ("#0000FF", "#FFA500")
    # draw a fractal canopy
fractal_canopy(canvas, 250, 500,
                n_iters=5, init_length=200,
                n_splits=4, angle_delta=180,
                off_angle=0, length_ratio=0.3,
                wave_amp=0, width=20,
                width_ratio=0.6, color=color_tuple)

slider_var1 = tk.IntVar()
slider_var2 = tk.IntVar()
slider_var3 = tk.DoubleVar()
slider_var4 = tk.IntVar()
slider_var5 = tk.IntVar()
slider_var6 = tk.IntVar()
slider_var7 = tk.IntVar()
slider_var8 = tk.IntVar() 

slider_frame = tk.Frame(window)
slider_frame.grid(row=1, column=0, sticky="ew")

sliders = [
    tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var1),
    tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var2),
    tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var3),
    tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var4),
    tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var5),
    tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var6),
    tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var7),
    tk.Scale(slider_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var8)
]

labels = [
    tk.Label(window, text="Slider 1"),
    tk.Label(window, text="Slider 2"),
    tk.Label(window, text="Slider 3"),
    tk.Label(window, text="Slider 4"),
    tk.Label(window, text="Slider 5"),
    tk.Label(window, text="Slider 6"),
    tk.Label(window, text="Slider 7"),
    tk.Label(window, text="Slider 8")
]

sliders = [
    tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var1),
    tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var2),
    tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var3),
    tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var4),
    tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var5),
    tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var6),
    tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var7),
    tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, variable=slider_var8)
]

# Create a frame for the sliders
slider_frame = tk.Frame(window)
slider_frame.grid(row=1, column=0, sticky="nsew")

# Grid labels and sliders in a 2-column layout
for i, label in enumerate(labels):
    label.grid(row=i, column=0, sticky="w")
    sliders[i].grid(row=i, column=1, sticky="e")

# Configure window to expand with canvas
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Center the slider frame vertically and horizontally
slider_frame.grid_configure(pady=(20, 20))
slider_frame.grid_columnconfigure(0, weight=1)
slider_frame.grid_rowconfigure(len(labels), weight=1)

window.mainloop()