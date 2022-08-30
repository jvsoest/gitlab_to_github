import gitlab
import subprocess

def loop_repositories(gitlab_url, private_token, group_name):
    gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
    groups = gl.groups.list(get_all=True)
    for group in groups:
        visibility = group.attributes['visibility']
        full_path = group.attributes['full_path']
        description = group.attributes['description']
        if not full_path.startswith(group_name):
            continue
        myGroup = gl.groups.get(group.attributes['id'])
        projects = myGroup.projects.list()
        for x in projects:
            # project = gl.projects.get(x.attributes["id"])
            ssh_url = x.attributes["ssh_url_to_repo"]
            repo_id = x.attributes["id"]
            path_with_namespace = x.attributes["path_with_namespace"]
            archived = x.attributes['archived']
            visibility = x.attributes['visibility']
            default_branch = x.attributes['default_branch']
            empty_repo = x.attributes['empty_repo']

            process_repository(gl, {
                'id': repo_id,
                'ssh_url': ssh_url,
                'path': path_with_namespace,
                'archived': archived,
                'visibility': visibility,
                'default_branch': default_branch,
                'empty_repo': empty_repo
            })

def call_cmd(myCommand):
    myCall = subprocess.Popen(myCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = myCall.communicate()
    myCall.wait()
    if len(errors) > 0:
        return False, errors.decode("utf-8")
    else:
        return True, output.decode("utf-8").replace("\n","")

def create_github_repository(repository_info):
    repo_name = "mdw-nl/" + repository_info['path'].replace("/", "_")
    myCommand = 'gh repo create ' + repo_name + " --" + repository_info['visibility']
    ssh_url = "git@github.com:" + repo_name

    success, output = call_cmd(myCommand)
    if success:
        return {
            'repo_name': repo_name,
            'ssh_url': ssh_url,
            'repo_url': output
        }
    else:
        None

def perform_migration(gitlab_info, github_info):
    migrate_cmd = f"bash git_shell_move.sh {gitlab_info['ssh_url']} {github_info['ssh_url']} {github_info['repo_url']}"
    print(migrate_cmd)
    success, output = call_cmd(migrate_cmd)
    print(success)
    print(output)

def process_repository(gl, gitlab_info):
    print(gitlab_info)
    github_info = create_github_repository(gitlab_info)
    perform_migration(gitlab_info, github_info)

    # Set default branch
    call_cmd("gh repo edit " + github_info['repo_name'] + " --default-branch " + gitlab_info['default_branch'])

if __name__ == "__main__":
    loop_repositories(
        "https://gitlab.com",
        "glpat--Ro8rnCP7iBJ1MhNH13Z",
        "medicaldataworks"
    )