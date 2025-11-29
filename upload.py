import re
import shutil
import subprocess

for project in ["cppmakelib", "cppmake"]:
    with open(f"{project}/pyproject.toml", 'r') as reader:
        pyproject = reader.read()
    pyproject = re.sub(r'^version = "(\d+)"$', lambda match: f'version = "{int(match.group(1)) + 1}"', pyproject, flags=re.MULTILINE)
    with open(f"{project}/pyproject.toml", 'w') as writer:
        writer.write(pyproject)
    subprocess.run(f"python -m build",                                                                     shell=True, cwd=project, check=True)
    subprocess.run(f"twine upload dist/* --username __token__ --password {open("pypi_token.txt").read()}", shell=True, cwd=project, check=True)
    shutil.rmtree(f"{project}/dist",               ignore_errors=True)
    shutil.rmtree(f"{project}/{project}.egg-info", ignore_errors=True)
