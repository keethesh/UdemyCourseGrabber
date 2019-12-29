from os import system, path
from pathlib import Path

home = str(Path.home())
envs_dir = str(home + "/.virtualenvs/")
if not path.isdir(envs_dir):
    system("cd")
    system("mkdir /.virtualenvs/UdemyCourseGrabber")
    system("source /.virtualenvs/UdemyCourseGrabber/bin/activate")
system("virtualenv" + home + "/.virtualenvs/")
system("pip3 install --upgrade selenium")
