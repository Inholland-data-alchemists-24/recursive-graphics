import tkinter as tk


def create_sliders(frame: tk.Frame, x_padding: int = 10, y_padding: int = 10) -> None:
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    # sliders for 8 different parameters
    trunk_length = tk.Scale(frame, label="Trunk's Length", from_=10, to=200, orient=tk.HORIZONTAL, resolution=1)
    trunk_length.grid(row=0, column=0, padx=x_padding, pady=y_padding, sticky="ew")

    num_splits = tk.Scale(frame, label="Branch Splits", from_=2, to=7, orient=tk.HORIZONTAL, resolution=1)
    num_splits.grid(row=0, column=1, padx=x_padding, pady=y_padding, sticky="ew")

    length_ratio = tk.Scale(frame, label="Length Ratio", from_=0.2, to=1.2, orient=tk.HORIZONTAL, resolution=0.01)
    length_ratio.grid(row=1, column=0, padx=x_padding, pady=y_padding, sticky="ew")

    angle_delta = tk.Scale(frame, label="Angle Between Branches", from_=0, to=180, orient=tk.HORIZONTAL, resolution=1)
    angle_delta.grid(row=1, column=1, padx=x_padding, pady=y_padding, sticky="ew")

    iteration_number = tk.Scale(frame, from_=1, to=9, orient=tk.HORIZONTAL, label="Iterations", resolution=1)
    iteration_number.grid(row=2, column=0, padx=x_padding, pady=y_padding, sticky="ew")

    off_angle = tk.Scale(frame, label="Angle Offset", from_=-45, to=45, orient=tk.HORIZONTAL, resolution=1)
    off_angle.grid(row=2, column=1, padx=x_padding, pady=y_padding, sticky="ew")

    trunk_color = tk.Scale(frame, label="Trunk's Color", from_=0, to=360, orient=tk.HORIZONTAL, resolution=1)
    trunk_color.grid(row=3, column=0, padx=x_padding, pady=y_padding, sticky="ew")

    leaf_color = tk.Scale(frame, label="Leaf Color", from_=0, to=360, orient=tk.HORIZONTAL, resolution=1)
    leaf_color.grid(row=3, column=1, padx=x_padding, pady=y_padding, sticky="ew")
