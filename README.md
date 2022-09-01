# GitLab to GitHub

Repository containing scripts to move repositories from GitLab to GitHub.

## Brief instructions
If you want to move a single repository, you can directly use the file [./git_shell.move.sh](./git_shell_move.sh).

If you need to move a full group from gitlab to github, you can use the python script [./run.py](./run.py). **Mind to change the properties at the end of the [./run.py](./run.py) file**.
The libraries used during this python execution are available in [./requirements.txt](./requirements.txt).

## Update local computer
Afterwards, any local clones on laptops need to update their remotes. This can be done using the following steps:
1. Open your local git folder in the terminal
2. Set the new origin location: `git remote set-url <new git location>`

This new git location is the same url as when you would normally clone a git repository. So probably it is something like `http://github.com/<organization_or_user>/<repository>.git`
