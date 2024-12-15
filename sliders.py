"""
Module for creating sliders in the GUI.

Contains functions for creating sliders given their parameters.

A create_sliders function is provided to add sliders for controlling various parameters of the game.
It adds each slider to the sliders frame provided as the argument to this function.
It uses data for the sliders which needs to be provided as a parameter in a form of a collection of tuples,
each containing data establishing the identity of each slider, such as what parameter in the app it controls,
its label, range and resolution and an initial value.

The create_sliders function also binds each slider to an event and assigns the event handlers to each,
e.g. handlers that update the canvas with a fractal tree generated with a new parameter taken from the slider-its value.

This module also defines the generator of the row and column pairs, which makes it automated
to populate rows and columns in the grid layout of the sliders. Enough to specify the number of columns for the sliders.
This may help populating the sliders automatically on each change to the window's size or the number of sliders.
"""
from collections.abc import Collection
from tkinter import Frame, Scale, HORIZONTAL


def create_sliders(
        parent_frame: Frame, sliders_init_data: Collection[tuple], num_columns: int, x_padding: int, y_padding: int
) -> list[Scale]:
    """
    Create sliders for modifying various parameters of the fractal tree by the user.
    Add them to the sliders frame in automatic way: each slider's position will

    Parameters:
        parent_frame (Frame): The frame to which the sliders will be added.
        sliders_init_data (Collection): A collection of tuples, each containing the following slider data:
            - label (str): The label for the slider.
            - from_ (int or float): The starting value of the slider.
            - to (int or float): The ending value of the slider.
            - resolution (int or float): The resolution of the slider.
        num_columns (int): The number of columns in the grid layout of the sliders frame.
        x_padding (int): The horizontal padding for each of the slider.
        y_padding (int): The vertical padding for each of the slider.
    """
    # The columns in the slider frame will expand equally
    for i in range(num_columns):
        parent_frame.columnconfigure(i, weight=1)

    column_sequence = column_sequence_generator(num_columns)

    sliders = []
    for slider_args in sliders_init_data:
        placement = next(column_sequence)
        sliders.append(create_slider(parent_frame, x_padding, y_padding, *slider_args, *placement))
    return sliders


def repopulate_sliders(sliders: list[Scale], num_columns: int) -> None:
    column_sequence = column_sequence_generator(num_columns)
    for slider in sliders:
        placement = next(column_sequence)
        slider.grid(row=placement[0], column=placement[1])
    return


def create_slider(
        parent: Frame, x_padding: int, y_padding: int, label: str,
        from_: int | float, to: int | float, resolution: int | float, row: int, column: int
) -> Scale:
    """
    Create a slider and add it to the parent widget.

    Parameters:

        parent (Frame): The parent widget to which the slider will be added.
        x_padding (int): The horizontal padding of the slider.
        y_padding (int): The vertical padding of the slider.
        label (str): The label for the slider.
        from_ (int or float): The starting value of the slider.
        to (int or float): The ending value of the slider.
        resolution (int or float): The resolution of the slider
        row (int): The row position in the grid layout.
        column (int): The column position in the grid layout.


    Returns:
        Scale: The created slider widget.
    """
    slider = Scale(parent, label=label, from_=from_, to=to, orient=HORIZONTAL, resolution=resolution)
    slider.grid(row=row, column=column, padx=x_padding, pady=y_padding, sticky="ew")
    return slider


def column_sequence_generator(num_columns: int):
    """
    A generator that yields the next field in the grid layout in the form of tuple: (row, column).
    The generator cycles through the columns from left to right, incrementing rows - top to bottom.
    """
    row = 0
    while True:
        for column in range(0, num_columns):
            yield row, column
        row += 1


def calc_max_num_columns(
        frame_width: int, slider_frame_x_padding: int, minimal_slider_width: int, each_slider_x_padding: int
) -> int:
    """
    Calculate the maximum number of sliders that can fit in a row of specified frame size.
    Takes into account a minimum width and padding (on both left & right side) of each slider.
    The padding is considered to be same on each side of each slider.
    Args:
        frame_width (int): The width of the frame to hold the sliders.
        slider_frame_x_padding (int): The padding of the slider frame.
        minimal_slider_width (int): The minimal width of a slider.
        each_slider_x_padding (int): The padding of each slider.

    Returns:
        int: The maximum number of sliders that can fit in a row
    """
    working_frame_width = frame_width - 2 * slider_frame_x_padding
    each_slider_min_width = minimal_slider_width + (2 * each_slider_x_padding)
    max_slots_in_row = working_frame_width // each_slider_min_width

    return max_slots_in_row


def calc_optimal_num_columns(num_of_sliders: int, max_slots_in_row: int) -> int:
    """
    Based on the number of sliders and the maximum number of sliders in a row, calculate the optimal
    number of columns this number of sliders should fit on to avoid almost empty rows, instead
    distributing as much from the full rows into the empty rows to make the frame look balanced over the rows.
    Args:
        num_of_sliders (int): The number of sliders to be placed in the frame.
        max_slots_in_row (int): The maximum number of sliders that can fit in a row.

    Returns:
        int: Number of columns for the sliders that makes the layout look balanced.
    """
    if max_slots_in_row == 0:
        return 1
    elif num_of_sliders <= max_slots_in_row:
        return num_of_sliders
    # sliders fit perfectly in a single or multiple rows
    elif num_of_sliders % max_slots_in_row == 0:
        return max_slots_in_row
    # sliders spread across multiple rows unevenly (last row has fewer sliders)
    elif num_of_sliders % max_slots_in_row != 0:
        number_of_full_rows = num_of_sliders // max_slots_in_row
        num_of_sliders_in_last_row = num_of_sliders % max_slots_in_row
        empty_place_in_last_row = max_slots_in_row - num_of_sliders_in_last_row

        sliders_in_a_row = max_slots_in_row
        # repopulate some sliders to the last row if there is enough space
        while empty_place_in_last_row - 1 >= number_of_full_rows:
            sliders_in_a_row -= 1
            num_of_sliders_in_last_row += number_of_full_rows
            empty_place_in_last_row = sliders_in_a_row - num_of_sliders_in_last_row
        return sliders_in_a_row
