#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Red Hat, Inc.
# SPDX-License-Identifier: MIT

"""Unit tests for nbde_server_tang module symlink protection."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import errno
import os
import sys
import tempfile
import unittest

try:
    from unittest.mock import MagicMock, Mock, patch, call
except ImportError:
    from mock import MagicMock, Mock, patch, call

# Mock Ansible imports before importing the module
sys.modules["ansible"] = MagicMock()
sys.modules["ansible.module_utils"] = MagicMock()
sys.modules["ansible.module_utils.basic"] = MagicMock()
sys.modules["ansible.module_utils._text"] = MagicMock()

# Add library directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../library"))

# pylint: disable=wrong-import-position
import nbde_server_tang  # noqa: E402


class TestSymlinkProtection(unittest.TestCase):
    """Test symlink protection in set_file_ownership_and_perms."""

    def setUp(self):
        """Set up test fixtures."""
        self.module = Mock()
        self.module.check_mode = False
        self.test_dir = "/test/keydir"
        self.uid = 1000
        self.gid = 1000

    @patch("nbde_server_tang.os.path.isdir")
    @patch("nbde_server_tang.get_dir_ownership")
    @patch("nbde_server_tang.os.listdir")
    @patch("nbde_server_tang.os.path.islink")
    @patch("nbde_server_tang.os.open")
    @patch("nbde_server_tang.os.fchown")
    @patch("nbde_server_tang.os.fchmod")
    @patch("nbde_server_tang.os.close")
    def test_normal_file_ownership_change(
        self,
        mock_close,
        mock_fchmod,
        mock_fchown,
        mock_open,
        mock_islink,
        mock_listdir,
        mock_get_ownership,
        mock_isdir,
    ):
        """Test that normal files have ownership and permissions changed."""
        mock_isdir.return_value = True
        mock_get_ownership.return_value = (self.uid, self.gid)
        mock_listdir.return_value = ["key1.jwk", "key2.jwk"]
        mock_islink.return_value = False
        mock_open.return_value = 42  # File descriptor

        nbde_server_tang.set_file_ownership_and_perms(self.module, self.test_dir)

        # Verify files were opened with O_NOFOLLOW
        self.assertEqual(mock_open.call_count, 2)
        mock_open.assert_any_call(
            "/test/keydir/key1.jwk", os.O_RDONLY | os.O_NOFOLLOW
        )
        mock_open.assert_any_call(
            "/test/keydir/key2.jwk", os.O_RDONLY | os.O_NOFOLLOW
        )

        # Verify ownership was changed
        self.assertEqual(mock_fchown.call_count, 2)
        mock_fchown.assert_any_call(42, self.uid, self.gid)

        # Verify permissions were set
        self.assertEqual(mock_fchmod.call_count, 2)
        mock_fchmod.assert_any_call(42, 0o400)

        # Verify file descriptors were closed
        self.assertEqual(mock_close.call_count, 2)
        mock_close.assert_any_call(42)

    @patch("nbde_server_tang.os.path.isdir")
    @patch("nbde_server_tang.get_dir_ownership")
    @patch("nbde_server_tang.os.listdir")
    @patch("nbde_server_tang.os.path.islink")
    @patch("nbde_server_tang.os.open")
    @patch("nbde_server_tang.os.fchown")
    @patch("nbde_server_tang.os.fchmod")
    @patch("nbde_server_tang.os.close")
    def test_symlink_skipped_by_islink_check(
        self,
        mock_close,
        mock_fchmod,
        mock_fchown,
        mock_open,
        mock_islink,
        mock_listdir,
        mock_get_ownership,
        mock_isdir,
    ):
        """Test that symlinks detected by islink() are skipped."""
        mock_isdir.return_value = True
        mock_get_ownership.return_value = (self.uid, self.gid)
        mock_listdir.return_value = ["symlink.jwk", "normal.jwk"]
        # First file is a symlink, second is normal
        mock_islink.side_effect = [True, False]
        mock_open.return_value = 42

        nbde_server_tang.set_file_ownership_and_perms(self.module, self.test_dir)

        # Verify only one file was opened (symlink was skipped)
        self.assertEqual(mock_open.call_count, 1)
        mock_open.assert_called_once_with(
            "/test/keydir/normal.jwk", os.O_RDONLY | os.O_NOFOLLOW
        )

        # Verify ownership/permissions only set once
        self.assertEqual(mock_fchown.call_count, 1)
        self.assertEqual(mock_fchmod.call_count, 1)
        self.assertEqual(mock_close.call_count, 1)

    @patch("nbde_server_tang.os.path.isdir")
    @patch("nbde_server_tang.get_dir_ownership")
    @patch("nbde_server_tang.os.listdir")
    @patch("nbde_server_tang.os.path.islink")
    @patch("nbde_server_tang.os.open")
    @patch("nbde_server_tang.os.fchown")
    @patch("nbde_server_tang.os.fchmod")
    @patch("nbde_server_tang.os.close")
    def test_symlink_caught_by_o_nofollow(
        self,
        mock_close,
        mock_fchmod,
        mock_fchown,
        mock_open,
        mock_islink,
        mock_listdir,
        mock_get_ownership,
        mock_isdir,
    ):
        """Test that symlinks caught by O_NOFOLLOW are handled safely."""
        mock_isdir.return_value = True
        mock_get_ownership.return_value = (self.uid, self.gid)
        mock_listdir.return_value = ["racecondition.jwk"]
        # islink returns False (TOCTOU race), but O_NOFOLLOW catches it
        mock_islink.return_value = False
        # Simulate ELOOP error from O_NOFOLLOW
        mock_open.side_effect = OSError(errno.ELOOP, "Too many symbolic links")

        nbde_server_tang.set_file_ownership_and_perms(self.module, self.test_dir)

        # Verify open was attempted
        self.assertEqual(mock_open.call_count, 1)

        # Verify ownership/permissions were NOT set (exception caught)
        mock_fchown.assert_not_called()
        mock_fchmod.assert_not_called()
        mock_close.assert_not_called()

    @patch("nbde_server_tang.os.path.isdir")
    @patch("nbde_server_tang.get_dir_ownership")
    @patch("nbde_server_tang.os.listdir")
    @patch("nbde_server_tang.os.path.islink")
    @patch("nbde_server_tang.os.open")
    @patch("nbde_server_tang.os.fchown")
    @patch("nbde_server_tang.os.fchmod")
    @patch("nbde_server_tang.os.close")
    def test_ioerror_handled_gracefully(
        self,
        mock_close,
        mock_fchmod,
        mock_fchown,
        mock_open,
        mock_islink,
        mock_listdir,
        mock_get_ownership,
        mock_isdir,
    ):
        """Test that IOError exceptions are handled gracefully."""
        mock_isdir.return_value = True
        mock_get_ownership.return_value = (self.uid, self.gid)
        mock_listdir.return_value = ["error.jwk"]
        mock_islink.return_value = False
        # Simulate IOError (Python 2 compatibility)
        mock_open.side_effect = IOError(errno.EACCES, "Permission denied")

        nbde_server_tang.set_file_ownership_and_perms(self.module, self.test_dir)

        # Verify open was attempted
        self.assertEqual(mock_open.call_count, 1)

        # Verify ownership/permissions were NOT set
        mock_fchown.assert_not_called()
        mock_fchmod.assert_not_called()
        mock_close.assert_not_called()

    @patch("nbde_server_tang.os.path.isdir")
    @patch("nbde_server_tang.get_dir_ownership")
    @patch("nbde_server_tang.os.listdir")
    @patch("nbde_server_tang.os.path.islink")
    @patch("nbde_server_tang.os.open")
    @patch("nbde_server_tang.os.fchown")
    @patch("nbde_server_tang.os.fchmod")
    @patch("nbde_server_tang.os.close")
    def test_fd_closed_even_on_fchown_error(
        self,
        mock_close,
        mock_fchmod,
        mock_fchown,
        mock_open,
        mock_islink,
        mock_listdir,
        mock_get_ownership,
        mock_isdir,
    ):
        """Test that file descriptor is closed even if fchown fails."""
        mock_isdir.return_value = True
        mock_get_ownership.return_value = (self.uid, self.gid)
        mock_listdir.return_value = ["key.jwk"]
        mock_islink.return_value = False
        mock_open.return_value = 42
        # Simulate fchown failure
        mock_fchown.side_effect = OSError(errno.EPERM, "Operation not permitted")

        # Should raise exception but still close fd
        with self.assertRaises(OSError):
            nbde_server_tang.set_file_ownership_and_perms(self.module, self.test_dir)

        # Verify fd was closed despite error
        mock_close.assert_called_once_with(42)

    @patch("nbde_server_tang.os.path.isdir")
    @patch("nbde_server_tang.get_dir_ownership")
    @patch("nbde_server_tang.os.listdir")
    def test_non_jwk_files_ignored(
        self, mock_listdir, mock_get_ownership, mock_isdir
    ):
        """Test that non-.jwk files are ignored."""
        mock_isdir.return_value = True
        mock_get_ownership.return_value = (self.uid, self.gid)
        mock_listdir.return_value = [
            "key.jwk",
            "readme.txt",
            ".hidden",
            "config.json",
        ]

        with patch("nbde_server_tang.os.path.islink") as mock_islink:
            mock_islink.return_value = False
            with patch("nbde_server_tang.os.open") as mock_open:
                mock_open.return_value = 42
                with patch("nbde_server_tang.os.fchown"):
                    with patch("nbde_server_tang.os.fchmod"):
                        with patch("nbde_server_tang.os.close"):
                            nbde_server_tang.set_file_ownership_and_perms(
                                self.module, self.test_dir
                            )

                            # Only .jwk file should be processed
                            self.assertEqual(mock_open.call_count, 1)
                            mock_open.assert_called_once_with(
                                "/test/keydir/key.jwk", os.O_RDONLY | os.O_NOFOLLOW
                            )

    @patch("nbde_server_tang.os.path.isdir")
    def test_check_mode_skips_operation(self, mock_isdir):
        """Test that check mode skips all operations."""
        self.module.check_mode = True
        mock_isdir.return_value = True

        with patch("nbde_server_tang.get_dir_ownership") as mock_get_ownership:
            nbde_server_tang.set_file_ownership_and_perms(self.module, self.test_dir)
            # Should return early, not call get_dir_ownership
            mock_get_ownership.assert_not_called()

    @patch("nbde_server_tang.os.path.isdir")
    def test_non_directory_skips_operation(self, mock_isdir):
        """Test that non-directory target skips all operations."""
        mock_isdir.return_value = False

        with patch("nbde_server_tang.get_dir_ownership") as mock_get_ownership:
            nbde_server_tang.set_file_ownership_and_perms(self.module, self.test_dir)
            # Should return early
            mock_get_ownership.assert_not_called()


class TestIntegrationSymlinkProtection(unittest.TestCase):
    """Integration tests with real filesystem operations."""

    def setUp(self):
        """Create temporary directory for testing."""
        self.test_dir = tempfile.mkdtemp(prefix="nbde_test_")
        self.module = Mock()
        self.module.check_mode = False

    def tearDown(self):
        """Clean up test directory."""
        import shutil

        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_real_symlink_is_skipped(self):
        """Integration test: Real symlinks are skipped."""
        # Create a real key file
        key_file = os.path.join(self.test_dir, "real.jwk")
        with open(key_file, "w") as f:
            f.write('{"test": "key"}')

        # Create a symlink pointing outside the directory
        target_file = tempfile.mktemp(prefix="target_")
        with open(target_file, "w") as f:
            f.write("sensitive data")
        symlink_file = os.path.join(self.test_dir, "symlink.jwk")
        os.symlink(target_file, symlink_file)

        try:
            # Get original ownership of target
            target_stat_before = os.stat(target_file)

            # Run the function
            nbde_server_tang.set_file_ownership_and_perms(self.module, self.test_dir)

            # Verify target ownership was NOT changed
            target_stat_after = os.stat(target_file)
            self.assertEqual(target_stat_before.st_uid, target_stat_after.st_uid)
            self.assertEqual(target_stat_before.st_gid, target_stat_after.st_gid)

            # Verify real key file was processed
            key_stat = os.stat(key_file)
            self.assertEqual(key_stat.st_mode & 0o777, 0o400)

        finally:
            os.unlink(target_file)


if __name__ == "__main__":
    unittest.main()
