import tkinter as tk
from fractal_funcs import fractal_canopy
from zoom import bind_canvas_zoom_events
import os, sys
import colorsys


while True:

    def show_congratulations(window_: tk.Tk, restart: callable) -> tk.Toplevel:
        """
        Show a congratulatory message window.
        Returns:
            tk.Toplevel: The congratulatory message window.
        """
        congrats_win = tk.Toplevel()
        congrats_win.resizable(False, False)
        congrats_label = tk.Label(congrats_win, text="Congratulations! \n\n "
                                                    'You have matched all the parameters of fractal trees.')
        congrats_label.pack(padx=23, pady=(20, 10))

        exit_button = tk.Button(congrats_win, text="Exit")
        exit_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(25, 15), pady=18)
        # bind the exit button to close the window
        exit_button.bind("<Button-1>", lambda event: window_.quit())

        restart_button = tk.Button(congrats_win, text="Try Again")
        restart_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(15, 25), pady=18)
        # bind the restart button to restart the game
        restart_button.bind("<Button-1>", lambda event: (congrats_win.destroy(), restart()))
        restart_button.config(bg="lightblue")


    def hsv_to_hex(hsv):
        h, s, v = hsv
        
        # Convert HSV to RGB
        rgb = colorsys.hsv_to_rgb(h, s, v)
        
        # Convert RGB to hexadecimal
        hex_color = '#{:02x}{:02x}{:02x}'.format(
            int(round(rgb[0] * 255)),
            int(round(rgb[1] * 255)),
            int(round(rgb[2] * 255))
        )
        
        return hex_color

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

    slider_var1 = tk.DoubleVar()
    slider_var2 = tk.DoubleVar()
    slider_var3 = tk.IntVar()
    slider_var4 = tk.DoubleVar()
    slider_var5 = tk.DoubleVar()
    slider_var6 = tk.DoubleVar()
    slider_var7 = tk.DoubleVar()
    slider_var8 = tk.DoubleVar()

    slider_var1.set(0)
    slider_var2.set(45)
    slider_var3.set(2)
    slider_var4.set(0.6)
    slider_var5.set(150)
    slider_var6.set(0.6)
    slider_var7.set(0.7)
    slider_var8.set(0.3)

    import random
    def random_init():
        c1 = random.uniform(0, 1)
        c2 = random.uniform(0, 1)
        return {
            'off_angle': random.uniform(-45, 45),
            'angle_delta': random.uniform(0, 180),
            'n_splits': random.randint(2, 8),
            'length_ratio': random.uniform(0.5, 0.75),
            'init_length': random.uniform(100, 200),
            'width_ratio': random.uniform(0.5, 0.75),
            'color': tuple((hsv_to_hex((c1, 1, 1)), hsv_to_hex(((c2, 1, 1)))))
        }, c1, c2

    rand_pars, c1, c2 = random_init()
    rand_pars_list = list(rand_pars.values())[:-1]
    rand_pars_list.append(c1)
    rand_pars_list.append(c2)

    # Demo of the zoom feature: draw squares on the canvas
    color_tuple = (hsv_to_hex((slider_var7.get(), 1, 1)), hsv_to_hex((slider_var8.get(), 1, 1)))

        # draw a fractal canopy
    fractal_canopy(canvas, 250, 500,
                    n_iters=5,
                    wave_amp=0, width=20, **rand_pars)

    fractal_canopy(canvas, 750, 500,
                    n_iters=5, init_length=slider_var5.get(),
                    n_splits=slider_var3.get(), angle_delta=slider_var2.get(),
                    off_angle=slider_var1.get(), length_ratio=slider_var4.get(),
                    wave_amp=0, width=20,
                    width_ratio=slider_var6.get(), color=(hsv_to_hex((slider_var7.get(), 1, 1)), hsv_to_hex((slider_var8.get(), 1, 1))))



    # Create a frame for the sliders
    slider_frame = tk.Frame(window)
    slider_frame.grid(row=1, column=0, sticky="nsew")
    import math
    import numpy as np
    def minmax(val, mins, maxs):
        return (val-mins)/(maxs-mins)
    ranges = [(-45, 45), (0, 180), (2, 8), (-0.5, 0.75), (100, 200), (0.5, 0.75), (0, 1), (0, 1)]
    def redraw(self):
        
        canvas.delete("all")
        selected_pars = [slider_var1.get(), slider_var2.get(), slider_var3.get(), slider_var4.get(), slider_var5.get(), slider_var6.get(), slider_var7.get(), slider_var8.get()]
        
        diffs=[]
        for i in range(8):
            min_ = ranges[i][0]
            max_ = ranges[i][1]

            diffs.append(abs(minmax(rand_pars_list[i], min_, max_) - minmax(selected_pars[i], min_, max_)))
            diffs_mean = np.mean(diffs)
            diff_perc = int(100 - min(diffs_mean/0.5*100, 100))
            match_label.config(text=f"Match: {diff_perc}%")
            
            
        diffl = match_label.cget("text")
        diffl = int(diffl[7:-1])
        
        if diffl >= 40:
            quit()
        fractal_canopy(canvas, 250, 500,
                    n_iters=5,
                    wave_amp=0, width=20, **rand_pars)

        fractal_canopy(canvas, 750, 500,
                    n_iters=5, init_length=slider_var5.get(),
                    n_splits=slider_var3.get(), angle_delta=slider_var2.get(),
                    off_angle=slider_var1.get(), length_ratio=slider_var4.get(),
                    wave_amp=0, width=20,
                    width_ratio=slider_var6.get(),color=(hsv_to_hex((slider_var7.get(), 1, 1)), hsv_to_hex((slider_var8.get(), 1, 1))))

    sliders = [
        tk.Scale(slider_frame, from_=-45, to=45, resolution=0.1, orient=tk.HORIZONTAL, variable=slider_var1, command=redraw),
        tk.Scale(slider_frame, from_=0, to=180, resolution=0.1, orient=tk.HORIZONTAL, variable=slider_var2, command=redraw),
        tk.Scale(slider_frame, from_=2, to=8, orient=tk.HORIZONTAL, variable=slider_var3, command=redraw),
        tk.Scale(slider_frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, variable=slider_var4, command=redraw),
        tk.Scale(slider_frame, from_=100, to=200, orient=tk.HORIZONTAL, variable=slider_var5, command=redraw),
        tk.Scale(slider_frame, from_=0.5, to=0.75, resolution=0.01, orient=tk.HORIZONTAL, variable=slider_var6, command=redraw),
        tk.Scale(slider_frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, variable=slider_var7, command=redraw),
        tk.Scale(slider_frame, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, variable=slider_var8, command=redraw)
    ]

    labels = [
        tk.Label(slider_frame, text="Angle Offset"),
        tk.Label(slider_frame, text="Angle Size"),
        tk.Label(slider_frame, text="Num. Branches"),
        tk.Label(slider_frame, text="Length Ratio"),
        tk.Label(slider_frame, text="Branch Length"),
        tk.Label(slider_frame, text="Width Ratio"),
        tk.Label(slider_frame, text="Root Color"),
        tk.Label(slider_frame, text="Leaf Color")
    ]

    match_label=tk.Label(slider_frame, text="Match: 0%")
    match_label.grid(row=0, column=9, rowspan=2, columnspan=3)

    # Grid labels and sliders in a 2-column layout
    for i, slider in enumerate(sliders):
        labels[i].grid(row=0, column=i)
        sliders[i].grid(row=1, column=i)




    window.mainloop()
