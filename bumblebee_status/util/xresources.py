import subprocess
import shutil

def query(key):
    if shutil.which("xgetres"):
        return subprocess.run(["xgetres", key],
                capture_output=True).stdout.decode("utf-8").strip()
    else:
        raise Exception("xgetres must be installed for this theme")

