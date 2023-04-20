"""Tests VersionChecker class"""
from click_skeleton.version_checker import VersionCheckerThread


def test_version_checker() -> None:
    """Test that version checker is working, as this an example CLI, it will print nothing"""
    version_checker = VersionCheckerThread(
        prog_name="click-skeleton", current_version="0.0.0"
    )
    version_checker.print()
