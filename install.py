import shutil
import subprocess

for project in ["cppmakelib", "cppmake"]:
    subprocess.run(f"python -m build", shell=True, cwd=project, check=True)
    subprocess.run(f"pip install .",   shell=True, cwd=project, check=True)
    shutil.rmtree(f"{project}/build",              ignore_errors=True)
    shutil.rmtree(f"{project}/dist",               ignore_errors=True)
    shutil.rmtree(f"{project}/{project}.egg-info", ignore_errors=True)