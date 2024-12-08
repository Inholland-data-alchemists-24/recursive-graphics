import numpy as np


class TreeNodeBase:
    """
    Base class for the tree node in the fractal tree.

    Attributes:

        depth (int): Depth in the fractal tree.
        start_x (float): Start x-coordinate.
        start_y (float): Start y-coordinate.
        length (float): Length of the branch.
        angle (float): Display angle (in pi radians).
        end_x (float): End x-coordinate.
        end_y (float): End y-coordinate.
        num_children (int): Number of children.
        length_scale (float): Ratio of the length of the child branch to the parent branch.
        delta_angle (float): Angles in between the branches.
        children (np.ndarray): Declare children variable for children nodes.

    Methods:

        set_children: Create children nodes.
        angle_spectrum: Generate the angles for the children.
    """

    def __init__(
        self,
        depth: int,
        start_x: float,
        start_y: float,
        length: float,
        angle: float,
        num_children: int,
        length_scale: float,
        delta_angle: float,
        max_depth: int = 6,
    ):
        if num_children < 0:
            raise ValueError("Number of children must be greater than or equal to 0.")
        self.depth = depth  # Depth in the fractal tree
        self.start_x = start_x  # Start x-coordinate
        self.start_y = start_y  # Start y-coordinate
        self.length = length  # Length of the branch
        self.angle = angle  # Display angle (in pi radians)
        self.end_x = self.start_x + np.cos(self.angle) * length  # End x-coordinate
        self.end_y = self.start_y + np.sin(self.angle) * length  # End y-coordinate
        self.num_children = num_children  # Number of children
        self.length_scale = (
            length_scale  # Ratio of the length of the child branch to the parent branch
        )
        self.delta_angle = delta_angle  # Angles in between the branches
        self.children = None  # Declare children variable for children nodes
        # Create children nodes
        if self.depth < max_depth and self.num_children > 0:
            self.children = np.ndarray(
                self.num_children, dtype=TreeNodeBase
            )  # Fixed-size array of CanopyTreeNode objects
            self.set_children(
                self.depth + 1,
                self.end_x,
                self.end_y,
                self.length * self.length_scale,
                self.angle,
                self.num_children,
                self.length_scale,
                self.delta_angle,
            )

    def set_children(
        self,
        depth: int,
        start_x: float,
        start_y: float,
        length: float,
        parent_angle: float,
        num_children: int,
        length_scale: float,
        delta_angle: float,
    ):
        angle_spectrum: np.ndarray[float] = self.angle_spectrum(parent_angle, delta_angle, num_children)
        if len(angle_spectrum) != num_children:
            raise ValueError(
                "The number of children must match the number of angles in the spectrum."
            )
        for i, angle in enumerate(angle_spectrum):  # type: int, float
            self.children[i] = TreeNodeBase(
                depth,
                start_x,
                start_y,
                length,
                angle,
                num_children,
                length_scale,
                delta_angle,
            )

    @staticmethod
    def angle_spectrum(
        parent_angle: float, delta_angle: float, num_children: int
    ) -> np.ndarray:
        """
        Generate the angles for the children nodes in the tree data structure.

        Args:
            parent_angle (float): The angle of the parent branch.
            delta_angle (float): The angle difference between each child branch.
            num_children (int): The number of children branches.

        Returns:
            np.ndarray: An array of angles for the children branches.
        """
        if num_children < 0:
            raise ValueError("Number of children must be greater than or equal to 0.")
        if num_children == 0:
            result = np.array([])
            return result
        angle_range = (num_children - 1) * delta_angle
        result = np.linspace(
            parent_angle - (angle_range / 2),
            parent_angle + (angle_range / 2),
            num=num_children
        )
        return result
