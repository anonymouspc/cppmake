import re
import shutil
import subprocess

for dir in ["cppmakelib", "cppmake"]:
    # Update version
    with open(f"{dir}/pyproject.toml", 'r') as reader:
        pyproject = reader.read()
    pyproject = re.sub(r'^version = "(\d+)"$', lambda match: f'version = "{int(match.group(1)) + 1}"', pyproject, flags=re.MULTILINE)
    with open(f"{dir}/pyproject.toml", 'w') as writer:
        writer.write(pyproject)
    
    # Build
    shutil.rmtree(f"{dir}/dist", ignore_errors=True)
    subprocess.run(f"python -m build", shell=True, cwd=dir)

    # Install
    subprocess.run(f"pip install -e .", shell=True, cwd=dir)

    # Upload
    subprocess.run(f"twine upload dist/* --username __token__ --password {open("pypi-token.txt").read()}", shell=True, cwd=dir)
    



