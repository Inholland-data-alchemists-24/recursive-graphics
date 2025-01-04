"""
helper_funcs.py

This module contains helper functions for use with drawing fractals on a Tkinter canvas.

Functions:
    draw_sine_wave_segment()
        Draws a sine wave segment on a Tkinter canvas between two points.
    hex_to_rgb()
        Converts a hex color string to an RGB tuple.
    rgb_to_hex()
        Converts an RGB tuple to a hex color string.
    interpolate_color()
        Interpolates between two RGB colors by a given factor.
    generate_gradient()
        Generates a gradient list of colors between two hex color values.
"""

import tkinter as tk
import numpy as np

def draw_sine_wave_segment(canvas: tk.Canvas,
                           x: float,
                           y: float,
                           end_x: float,
                           end_y: float,
                           line_len: float,
                           wave_amp: float,
                           fill: str,
                           width: float = 1):
    """
    Draws a sine wave segment on a Tkinter canvas between two points.

    Args:
        canvas (tk.Canvas): The Tkinter canvas on which to draw the sine wave segment.
        x (float): The x-coordinate of the starting point.
        y (float): The y-coordinate of the starting point.
        end_x (float): The x-coordinate of the ending point.
        end_y (float): The y-coordinate of the ending point.
        line_len (float): The length of the line segment.
        wave_amp (float): The amplitude of the sine wave.
        fill (str): The color of the sine wave in hex format.
        width (float, optional): The width of the sine wave line. Defaults to 1.

    Returns:
        None
    """
    # Calculate the angle of rotation
    angle = np.arctan2(end_y - y, end_x - x)

    period_scale = 2 * np.pi / line_len

    # Generate sine wave points
    t = np.linspace(0, line_len, 100)
    sine_wave_x = t
    sine_wave_y = wave_amp * np.sin(period_scale * t)

    # Rotate and translate points
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)

    transformed_points = []
    for i in range(len(t)):
        new_x = cos_angle * sine_wave_x[i] - sin_angle * sine_wave_y[i] + x
        new_y = sin_angle * sine_wave_x[i] + cos_angle * sine_wave_y[i] + y
        transformed_points.append((new_x, new_y))
    # Draw the sine wave segment
    for i in range(len(transformed_points) - 1):
        unit_vector_x = transformed_points[i+1][0] - transformed_points[i][0]
        unit_vector_y = transformed_points[i+1][1] - transformed_points[i][1]
        unit_vector_length = np.sqrt(unit_vector_x**2 + unit_vector_y**2)
        unit_vector_x /= unit_vector_length
        unit_vector_y /= unit_vector_length

        canvas.create_line(transformed_points[i][0],
                           transformed_points[i][1],
                           transformed_points[i+1][0] + (unit_vector_x * 2.5),
                           transformed_points[i+1][1] + (unit_vector_y * 2.5),
                           width=width,
                           fill=fill)

# Convert hex color to RGB tuple
def hex_to_rgb(hex_color):
    """
    Converts a hex color string to an RGB tuple.

    Args:
        hex_color (str): The hex color string (e.g., "#ff0000").

    Returns:
        tuple: A tuple representing the RGB values (e.g., (255, 0, 0)).
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Convert RGB tuple to hex color
def rgb_to_hex(rgb_color):
    """
    Converts an RGB tuple to a hex color string.

    Args:
        rgb_color (tuple): A tuple representing the RGB values (e.g., (255, 0, 0)).

    Returns:
        str: The hex color string (e.g., "#ff0000").
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

# Interpolate between two colors
def interpolate_color(color1, color2, factor):
    """
    Interpolates between two RGB colors by a given factor.

    Args:
        color1 (tuple): The starting RGB color tuple (e.g., (255, 0, 0)).
        color2 (tuple): The ending RGB color tuple (e.g., (0, 0, 255)).
        factor (float): A factor between 0 and 1 indicating the interpolation position.

    Returns:
        tuple: The interpolated RGB color tuple.
    """
    return tuple(int(color1[i] + (color2[i] - color1[i]) * factor) for i in range(3))

# Generate a gradient between two colors
def generate_gradient(color1, color2, steps):
    """
    Generates a gradient list of colors between two hex color values.

    Args:
        color1 (str): The starting hex color string (e.g., "#ff0000").
        color2 (str): The ending hex color string (e.g., "#0000ff").
        steps (int): The number of colors to generate in the gradient.

    Returns:
        list: A list of hex color strings representing the gradient.
    """
    rgb_color1 = hex_to_rgb(color1)
    rgb_color2 = hex_to_rgb(color2)
    gradient = []
    for step in range(steps):
        factor = step / (steps - 1)
        interpolated_color = interpolate_color(rgb_color1,
                                               rgb_color2,
                                               factor)
        gradient.append(rgb_to_hex(interpolated_color))
    return gradient
