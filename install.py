import shutil
import subprocess

for project in ["cppmakelib", "cppmake"]:
    shutil.rmtree(f"{project}/build", ignore_errors=True)
    subprocess.run(f"pip install .",  shell=True, cwd=project, check=True)