from unittest import TestCase

import numpy as np

from datastructures.fractal_tree_base import TreeNodeBase


class TestTreeNodeBase(TestCase):

    def test_set_2_children(self):
        node = TreeNodeBase(0, 0, 0, 100, 0, 2, 0.7, np.radians(30), 3)
        self.assertEqual(len(node.children), 2)
        self.assertIsInstance(node.children[0], TreeNodeBase)
        self.assertIsInstance(node.children[1], TreeNodeBase)
        self.assertEqual(node.children[0].depth, 1)
        self.assertEqual(node.children[1].depth, 1)
        self.assertAlmostEqual(node.children[0].start_x, 100)
        self.assertAlmostEqual(node.children[0].start_y, 0)
        self.assertAlmostEqual(node.children[1].start_x, 100)
        self.assertAlmostEqual(node.children[1].start_y, 0)
        self.assertAlmostEqual(node.children[0].length, 70)
        self.assertAlmostEqual(node.children[1].length, 70)
        self.assertAlmostEqual(node.children[0].angle, np.radians(-15))
        self.assertAlmostEqual(node.children[1].angle, np.radians(15))
        self.assertAlmostEqual(node.children[0].end_x, 100 + 70 * np.cos(np.radians(-15)))
        self.assertAlmostEqual(node.children[0].end_y, 0 + 70 * np.sin(np.radians(-15)))
        self.assertAlmostEqual(node.children[1].end_x, 100 + 70 * np.cos(np.radians(15)))
        self.assertAlmostEqual(node.children[1].end_y, 0 + 70 * np.sin(np.radians(15)))

    def test_set_3_children(self):
        parent = TreeNodeBase(0, 0, 0, 1, 0, 3, 0.5, np.pi / 8)
        self.assertEqual(len(parent.children), 3)
        self.assertIsInstance(parent.children[0], TreeNodeBase)
        self.assertIsInstance(parent.children[1], TreeNodeBase)
        self.assertIsInstance(parent.children[2], TreeNodeBase)
        self.assertRaises(IndexError, lambda: parent.children[3])
        self.assertEqual(parent.children[0].depth, 1)
        self.assertEqual(parent.children[1].depth, 1)
        self.assertEqual(parent.children[2].depth, 1)
        self.assertAlmostEqual(parent.children[0].start_x, 1)
        self.assertAlmostEqual(parent.children[0].start_y, 0)
        self.assertAlmostEqual(parent.children[1].start_x, 1)
        self.assertAlmostEqual(parent.children[1].start_y, 0)
        self.assertAlmostEqual(parent.children[2].start_x, 1)
        self.assertAlmostEqual(parent.children[2].start_y, 0)
        self.assertAlmostEqual(parent.children[0].length, 0.5)
        self.assertAlmostEqual(parent.children[1].length, 0.5)
        self.assertAlmostEqual(parent.children[2].length, 0.5)
        self.assertAlmostEqual(parent.children[0].angle, -np.pi / 8)
        self.assertAlmostEqual(parent.children[1].angle, 0)
        self.assertAlmostEqual(parent.children[2].angle, np.pi / 8)
        self.assertAlmostEqual(parent.children[0].end_x, 1 + 0.5 * np.cos(-np.pi / 8))
        self.assertAlmostEqual(parent.children[0].end_y, 0 + 0.5 * np.sin(-np.pi / 8))
        self.assertAlmostEqual(parent.children[1].end_x, 1 + 0.5 * np.cos(0))
        self.assertAlmostEqual(parent.children[1].end_y, 0 + 0.5 * np.sin(0))
        self.assertAlmostEqual(parent.children[2].end_x, 1 + 0.5 * np.cos(np.pi / 8))

    def test_set_children_no_children(self):
        parent = TreeNodeBase(0, 0, 0, 1, 0, 0, 0.5, np.pi / 8)
        self.assertIsNone(parent.children)

    def test_set_children_max_depth(self):
        parent = TreeNodeBase(6, 0, 0, 1, 0, 3, 0.5, np.pi / 8, 6)
        self.assertIsNone(parent.children)

    def test_angle_spectrum(self):
        parent_angle = np.pi / 4
        delta_angle = np.pi / 8
        num_children = 3
        expected_angles = np.array([np.pi / 8, np.pi / 4, 3 * np.pi / 8])
        result = TreeNodeBase.angle_spectrum(parent_angle, delta_angle, num_children)
        np.testing.assert_array_almost_equal(result, expected_angles)

    def test_angle_spectrum_no_children(self):
        parent_angle = np.pi / 4
        delta_angle = np.pi / 8
        num_children = 0
        expected_angles = np.array([])
        result = TreeNodeBase.angle_spectrum(parent_angle, delta_angle, num_children)
        np.testing.assert_array_almost_equal(result, expected_angles)

    def test_angle_spectrum_single_child(self):
        parent_angle = np.pi / 4
        delta_angle = np.pi / 8
        num_children = 1
        expected_angles = np.array([np.pi / 4])
        result = TreeNodeBase.angle_spectrum(parent_angle, delta_angle, num_children)
        np.testing.assert_array_almost_equal(result, expected_angles)

    def test_angle_spectrum_negative_parent_angle(self):
        parent_angle = -np.pi / 4
        delta_angle = np.pi / 8
        num_children = 3
        expected_angles = np.array([-3 * np.pi / 8, -np.pi / 4, -np.pi / 8])
        result = TreeNodeBase.angle_spectrum(parent_angle, delta_angle, num_children)
        np.testing.assert_array_almost_equal(result, expected_angles)

    def test_angle_spectrum_negative_delta_angle(self):
        parent_angle = np.pi / 4
        delta_angle = -np.pi / 8
        num_children = 3
        expected_angles = np.array([3 * np.pi / 8, np.pi / 4, np.pi / 8])
        result = TreeNodeBase.angle_spectrum(parent_angle, delta_angle, num_children)
        np.testing.assert_array_almost_equal(result, expected_angles)

    def test_angle_spectrum_negative_num_children(self):
        parent_angle = np.pi / 4
        delta_angle = np.pi / 8
        num_children = -3
        # In case where the number of children > 0 only then the array of children is instantiated

        with self.assertRaises(ValueError):
            TreeNodeBase.angle_spectrum(parent_angle, delta_angle, num_children)

    def test_angle_spectrum_zero_num_children(self):
        parent_angle = np.pi / 4
        delta_angle = np.pi / 8
        num_children = 0
        expected_angles = np.array([])
        result = TreeNodeBase.angle_spectrum(parent_angle, delta_angle, num_children)
        np.testing.assert_array_almost_equal(result, expected_angles)

    def test_angle_spectrum_return_type(self):
        parent_angle = np.pi / 4
        delta_angle = np.pi / 8
        num_children = 3
        result = TreeNodeBase.angle_spectrum(parent_angle, delta_angle, num_children)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.dtype, float)
        self.assertTrue(issubclass(result.dtype.type, float))

    def test_angle_spectrum_return_type_for_0_children(self):
        parent_angle = np.pi / 4
        delta_angle = np.pi / 8
        num_children = 0
        result = TreeNodeBase.angle_spectrum(parent_angle, delta_angle, num_children)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.size, 0)
        self.assertEqual(result.dtype, float)
        self.assertTrue(issubclass(result.dtype.type, float))