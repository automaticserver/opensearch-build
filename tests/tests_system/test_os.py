# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess
import unittest
from unittest.mock import patch

from system.os import current_architecture, current_platform


class TestOs(unittest.TestCase):
    # current_architecture
    def test_current_architecture(self):
        self.assertTrue(current_architecture() in ["x64", "arm64"])

    @patch("subprocess.check_output", return_value="x86_64".encode())
    def test_x86_64_return_x64_architecture(self, mock_subprocess):
        self.assertTrue(current_architecture() == "x64")

    @patch("subprocess.check_output", return_value="aarch64".encode())
    def test_aarch64_return_arm64_architecture(self, mock_subprocess):
        self.assertTrue(current_architecture() == "arm64")

    @patch("subprocess.check_output", return_value="arm64".encode())
    def test_arm64_return_arm64_architecture(self, mock_subprocess):
        self.assertTrue(current_architecture() == "arm64")

    @patch("subprocess.check_output", return_value="invalid".encode())
    def test_invalid_architecture(self, mock_subprocess):
        with self.assertRaises(ValueError) as context:
            current_architecture()
        self.assertEqual("Unsupported architecture: invalid", str(context.exception))

    @patch("subprocess.check_output", return_value="x86_64".encode())
    def test_subprocess_call(self, mock_subprocess):
        current_architecture()
        subprocess.check_output.assert_called_with(["uname", "-m"])

    # current_platform
    def test_current_platform(self):
        self.assertTrue(current_platform() in ["linux", "darwin"])

    @patch("subprocess.check_output", return_value="Xyz".encode())
    def test_current_platform_lowercase(self, mock_subprocess):
        self.assertTrue(current_platform() == "xyz")
