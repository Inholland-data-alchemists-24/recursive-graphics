import tkinter as tk
from random import randint
import numpy as np

def progress():
    total_progress = 0
    for key in sliders:
        slider_value = sliders[key].get()
        target_value = random_params[key]

        # Normalize the difference to a fixed range
        max_range = sliders[key]['to'] - sliders[key]['from']
        ratio = 1 - abs(slider_value - target_value) / max_range

        # Ensure the ratio is between 0 and 1
        ratio = max(0, min(1, ratio))

        # Convert ratio to percentage (each parameter contributes equally)
        percentage = ratio * (100 / len(sliders))
        total_progress += percentage

    return f"{round(total_progress, 2)}%"




# Function to create sliders
def choose_season(canvas, season):
    canvas.delete('season')
    seasons = {
        "winter": tk.PhotoImage(file="winter1png.png"),
        "spring": tk.PhotoImage(file="spring1.png"),#.subsample(3),
        "summer": tk.PhotoImage(file="summer_4k.png").subsample(2),
        "autumn": tk.PhotoImage(file="autumn2.png").subsample(2)
    }
    canvas.season_images = seasons  # Keep a reference to avoid garbage collection
    canvas.create_image(599, 250, image=seasons[season], tag='season')
    update_tree(canvas, sliders)
    

def create_slider(window, from_value, to_value, label, resolution, command, length, set_value, row, column):
    slider = tk.Scale(
        window, label=label, from_=from_value, to=to_value, orient=tk.HORIZONTAL,
        resolution=resolution, command=command, length=length
    )
    slider.set(set_value)
    slider.grid(row=row, column=column, padx=10, pady=10)
    return slider

# Function to draw the tree
def draw_tree(x, y, canvas, length, angle, iteration, branch_angle, length_ratio, tag, first_iter=True):
    if iteration == 0:
        return
    
    current_angle = 90 if first_iter else angle
    color = "brown" if first_iter else "green"
    
    x_end = x + length * np.cos(np.radians(current_angle))
    y_end = y - length * np.sin(np.radians(current_angle))
    
    canvas.create_line(x, y, x_end, y_end, width=3, fill=color, tags=tag)
    
    draw_tree(x_end, y_end, canvas, length * length_ratio, angle + branch_angle, iteration - 1, branch_angle, length_ratio, tag, False)
    draw_tree(x_end, y_end, canvas, length * length_ratio, angle - branch_angle, iteration - 1, branch_angle, length_ratio, tag, False)

# Function to check if user parameters match the random tree
def check_match(sliders):
    global random_params  # Ensure the use of the global variable
    global tolerance
    tolerance = {
        'length': 2,
        'angle': 2,
        'iteration': 0.1,
        'branch_angle': 2,
        'length_ratio': 0.02
    }
    global diff
    diff = {
        'length': abs(random_params['length'] - sliders['length'].get()),
        'angle': abs(random_params['angle'] - sliders['angle'].get()),
        'iteration': abs(random_params['iteration'] - sliders['iteration'].get()),
        'branch_angle': abs(random_params['branch_angle'] - sliders['branch_angle'].get()),
        'length_ratio': abs(random_params['length_ratio'] - sliders['length_ratio'].get())
    }

    if all(diff[key] <= tolerance[key] for key in tolerance):
        for slider in sliders.values():
            slider.config(state=tk.DISABLED)
        show_congratulations(win)
    else:
        not_match = tk.Toplevel(win)
        centrum_window(not_match, "Not Matched", 300, 300)

        not_match_label = tk.Label(not_match, text=f"Sorry! \n You haven't matched the tree! \n Try again! \n The progress is {progress()} ", font=("Arial", 14))
        not_match_label.pack(padx=10, pady=10)

        continue_button = tk.Button(not_match, text="Continue", command=not_match.destroy)
        continue_button.pack(padx=10, pady=10)


# Function to update the tree
def update_tree(canvas, sliders):
    canvas.delete('updated')
    length = sliders['length'].get()
    angle = sliders['angle'].get()
    iterations = sliders['iteration'].get()
    branch_angle = sliders['branch_angle'].get()
    length_ratio = sliders['length_ratio'].get()

    draw_tree(800, 500, canvas, length, angle, iterations, branch_angle, length_ratio, tag="updated", first_iter=True)
    # check_match(sliders)

# Function to generate a random tree
def generate_random_tree(canvas):
    global random_params
    random_params = {
        'length': randint(80, 180),
        'angle': randint(0, 180),
        'iteration': randint(3, 8),
        'branch_angle': randint(10, 90),
        'length_ratio': (randint(20, 100) / 100)
    }
    print("Random Tree Parameters:", random_params)
    canvas.delete("random")
    draw_tree(300, 500, canvas, **random_params, tag="random")

# Function to show congratulations window
def show_congratulations(window):
    congrat_win = tk.Toplevel(window)
    centrum_window(congrat_win, "Congratulations", 300, 300)
    
    congrat_label = tk.Label(congrat_win, text="Congratulations!\nYou've matched the tree!", font=("Arial", 14))
    congrat_label.pack(padx=10, pady=10)
    
    restart_button = tk.Button(congrat_win, text="Restart", command=lambda: restart(win))
    restart_button.pack(padx=10, pady=10)
    
    exit_button = tk.Button(congrat_win, text="Exit", command=lambda: exit_app(win))
    exit_button.pack(padx=10, pady=10)

# Function to center window
def centrum_window(window, title, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.title(title)
    window.resizable(False, False)

# Function to restart the application
def restart(window):
    window.destroy()
    start()

# Function to exit the application
def exit_app(window):
    window.destroy()

# Main application function
def start():
    global win
    win = tk.Tk()
    centrum_window(win, "Tree Matching Game", 1200, 900)
    
    canvas = tk.Canvas(win, width=1198, height=500)
    canvas.pack(padx=1, pady=1)
    controls = tk.LabelFrame(win, text="Controls", font=("Arial", 14), padx=10, pady=10)
    global sliders
    sliders = {}
    controls = tk.LabelFrame(win, text="Adjust Tree Parameters", font=("Arial", 14), padx=10, pady=10)
    sliders['length'] = create_slider(controls, 50, 200, "Branch Length", 1, lambda e: update_tree(canvas, sliders), 200, 100, 0, 0)
    sliders['angle'] = create_slider(controls, 0, 180, "Branch Angle", 1, lambda e: update_tree(canvas, sliders), 200, 45, 0, 1)
    sliders['iteration'] = create_slider(controls, 1, 10, "Iterations", 1, lambda e: update_tree(canvas, sliders), 200, 6, 0, 2)
    sliders['branch_angle'] = create_slider(controls, 0, 90, "Branch Angle", 1, lambda e: update_tree(canvas, sliders), 200, 30, 0, 3)
    sliders['length_ratio'] = create_slider(controls, 0.1, 1, "Length Ratio", 0.01, lambda e: update_tree(canvas, sliders), 200, 0.7, 0, 4)
    controls.pack(padx=10, pady=10)
    
    Buttons_Label = tk.LabelFrame(win, text="Control Buttons", font=("Arial", 14), padx=10, pady=10)
    # Button to generate random tree
    random_tree_button = tk.Button(Buttons_Label, text="Generate Random Tree", command=lambda: generate_random_tree(canvas))
    random_tree_button.grid(row=0, column=0, padx=10, pady=10)
    
    # Button to check match
    match_button = tk.Button(Buttons_Label, text="Check Match", command= lambda: check_match(sliders))
    match_button.grid(row=0, column=1, padx=10, pady=10)

    winter_button = tk.Button(Buttons_Label, text="Winter", command=lambda: choose_season(canvas, "winter"))
    winter_button.grid(row=0, column=2, padx=10, pady=10)

    autumn_button = tk.Button(Buttons_Label, text="Autumn", command= lambda: choose_season(canvas, "autumn"))
    autumn_button.grid(row=0, column=3, padx=10, pady=10)

    spring_button = tk.Button(Buttons_Label, text="Spring", command= lambda: choose_season(canvas, "spring"))
    spring_button.grid(row=0, column=4, padx=10, pady=10)

    summer_button = tk.Button(Buttons_Label, text="Summer", command= lambda: choose_season(canvas, "summer"))
    summer_button.grid(row=0, column=5, padx=10, pady=10)

    Buttons_Label.pack(padx=10, pady=10)
    
    win.mainloop()

start()

