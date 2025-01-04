"""
fractal_funcs.py

This module contains functions for generating various
fractal patterns designed for use with a Tkinter canvas.
The fractal generating functions utilize recursion to
create complex and visually appealing structures.

Functions:
    fractal_canopy()
        Recursively draws a fractal canopy (a tree-like structure) on the provided Tkinter canvas.
"""

import tkinter as tk
import numpy as np
from numpy import radians as rad
from helper_funcs import draw_sine_wave_segment, generate_gradient

def fractal_canopy(
    canvas: tk.Canvas,
    x: float,
    y: float,
    off_angle: float = 0,
    angle_delta: float = 10,
    start_angle: float = -90,
    n_splits: int = 2,
    n_iters: int = 3,
    length_ratio: float = 0.75,
    init_length: float = 200,
    wave_amp: float = 0,
    width: float = 1,
    width_ratio: float = 0.75,
    color="#000000",
    first_iter: bool = True,
) -> None:
    """
    Recursively draws a fractal canopy (a tree-like structure) on the provided Tkinter canvas.

    This function uses recursion to draw a fractal canopy
    by splitting each branch into multiple smaller branches
    at specified angles and lengths.
    Optionally, sine wave segments can be added to the branches.

    Args:
        canvas (tk.Canvas):
            The Tkinter canvas on which to draw the fractal canopy.
        x (float):
            The x-coordinate of the starting point of the fractal canopy.
        y (float):
            The y-coordinate of the starting point of the fractal canopy.
        off_angle (float, optional): 
            The offset angle for the branches in degrees. Defaults to 0.
        angle_delta (float, optional): 
            The angle between the branches in degrees. Defaults to 10.
        start_angle (float, optional): 
            The starting angle of the first branch in degrees. Defaults to -90 (upwards).
        n_splits (int, optional): 
            The number of branches to split into at each iteration. Defaults to 2.
        n_iters (int, optional): 
            The number of recursive iterations to perform. Defaults to 3.
        length_ratio (float, optional): 
            The ratio by which the length of each branch decreases at each iteration.
            Defaults to 0.75.
        init_length (float, optional): 
            The initial length of the first branch. Defaults to 200.
        wave_amp (float, optional): 
            The amplitude of the sine wave segments. Defaults to 0.
            If non-zero, sine wave segments will be added to the branches.
        width (float, optional): 
            The width of the branches. Defaults to 1.
        width_ratio (float, optional): 
            The ratio by which the width of each branch decreases at each iteration.
            Defaults to 0.75.
        color (str or tuple of size 2, optional): 
            The color of the branches in hex format. Defaults to "#000000" (black).
            If a tuple of size 2 is provided, a color gradient is generated between the two colors.
            If a single color is provided, all branches will be drawn in that color.
        first_iter (bool, optional): 
            A flag indicating whether this is the first iteration.
            Defaults to True. Do not modify this parameter.

    Returns:
        None
    """
    def draw_branch(
        x: float,
        y: float,
        end_x: float,
        end_y: float,
        width: float,
        color: str
    ) -> None:
        """
        Draws a branch segment on the canvas.
        If wave_amp is non-zero, a sine wave segment is drawn instead.

        Args:
            x (float): The x-coordinate of the starting point of the branch.
            y (float): The y-coordinate of the starting point of the branch.
            end_x (float): The x-coordinate of the ending point of the branch.
            end_y (float): The y-coordinate of the ending point of the branch.
            width (float): The width of the branch.
            color (str): The color of the branch in hex format.
        
        Returns:
            None
        """
        if wave_amp != 0:
            draw_sine_wave_segment(canvas, x, y, end_x, end_y,
                                   init_length, wave_amp,
                                   width=width, fill=color)
        else:
            canvas.create_line(x, y, end_x, end_y, width=width, fill=color)


    def get_color(
        n_iters: int,
        color: str|list
    ) -> str:
        """
        Returns the color for the current iteration based on the provided color.
        If a list of colors is provided, the color changes with each iteration.

        Args:
            n_iters (int): The current iteration number.
            color (str or list): The color of the branches in hex format or a list of hex values.

        Returns:
            str: The color for the current iteration.
        """
        if isinstance(color, str):
            return color
        return color[-(n_iters-1)]


    # Base case - stop recursion if n_iters is 1
    if n_iters == 1:
        return
    start_angle_rad = rad(start_angle)

    # Draw the first branch segment
    if first_iter:
        if isinstance(color, str):
            color = generate_gradient(color, color, n_iters)
        else:
            color = generate_gradient(color[0], color[1], n_iters)

        end_x = (x
                 + np.cos(start_angle_rad)
                 * init_length)
        end_y = (y
                 + np.sin(start_angle_rad)
                 * init_length)
        draw_branch(x, y, end_x, end_y, width, get_color(n_iters, color))
        fractal_canopy(canvas, end_x, end_y,
                       n_iters=n_iters-1,
                       first_iter=False,
                       n_splits=n_splits,
                       angle_delta=angle_delta,
                       start_angle=np.degrees(start_angle_rad) + off_angle,
                       init_length=(init_length * length_ratio),
                       off_angle=off_angle,
                       wave_amp=wave_amp,
                       width=width * width_ratio,
                       width_ratio=width_ratio,
                       color=color)
    else:
        # Calculate the angles for the branches
        left_angle = start_angle - (angle_delta / 2)
        right_angle = start_angle + (angle_delta / 2)
        angles = np.linspace(left_angle, right_angle, n_splits)
        # For each angle, draw a branch and recursively call the function
        for angle in angles:
            angle_rad = rad(angle)
            end_x = (x
                     + np.cos(angle_rad)
                     * init_length)
            end_y = (y
                     + np.sin(angle_rad)
                     * init_length)
            draw_branch(x, y, end_x, end_y, width, get_color(n_iters, color))
            fractal_canopy(canvas,
                           end_x,
                           end_y,
                           n_iters=n_iters-1,
                           first_iter=False,
                           init_length=init_length * length_ratio,
                           start_angle=np.degrees(angle_rad) + off_angle,
                           n_splits=n_splits,
                           angle_delta=angle_delta,
                           off_angle=off_angle,
                           wave_amp=wave_amp,
                           width=width * width_ratio,
                           width_ratio=width_ratio,
                           color=color)
