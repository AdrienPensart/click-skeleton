from click_skeleton.version_checker import VersionCheckerThread

def test_version_checker():
    version_check = VersionCheckerThread(
       prog_name='click-skeleton',
       current_version='0.0.0',
    )
    version_check.join()
