import gitlab
import subprocess

def loop_repositories(gitlab_url, private_token, group_name, org_name):
    """
    Loop over all repositories for a given group_name
    """
    gl = gitlab.Gitlab(gitlab_url, private_token=private_token)
    groups = gl.groups.list(get_all=True)
    process_repo = False
    for group in groups:
        visibility = group.attributes['visibility']
        full_path = group.attributes['full_path']
        description = group.attributes['description']
        if not full_path.startswith(group_name):
            continue
        myGroup = gl.groups.get(group.attributes['id'])
        projects = myGroup.projects.list(get_all=True)
        for x in projects:
            # project = gl.projects.get(x.attributes["id"])
            ssh_url = x.attributes["ssh_url_to_repo"]
            repo_id = x.attributes["id"]
            path_with_namespace = x.attributes["path_with_namespace"]
            archived = x.attributes['archived']
            visibility = x.attributes['visibility']
            default_branch = x.attributes['default_branch']
            empty_repo = x.attributes['empty_repo']

            repo_name = org_name + "/" + path_with_namespace.replace(group_name+"/", "").replace("/", "_")
            print(str(archived) + "," + path_with_namespace + "," + repo_name)
            
            if visibility=="internal":
                visibility = "private"
            
            if process_repo:
            process_repository(gl, {
                'id': repo_id,
                'ssh_url': ssh_url,
                'path': path_with_namespace,
                'archived': archived,
                'visibility': visibility,
                'default_branch': default_branch,
                'empty_repo': empty_repo
            }, group_name, org_name)

            if path_with_namespace == 'UM-CDS/fair/tools/r2rml':
                process_repo = True

def call_cmd(myCommand):
    """
    Generic function to call a command-line script
    """
    myCall = subprocess.Popen(myCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, errors = myCall.communicate()
    myCall.wait()
    if len(errors) > 0:
        return False, errors.decode("utf-8")
    else:
        return True, output.decode("utf-8").replace("\n","")

def create_github_repository(repository_info, group_name, org_name):
    """
    Create GitHub repository using logged in gh cli command
    """
    repo_name = org_name + "/" + repository_info['path'].replace(group_name+"/", "").replace("/", "_")
    myCommand = 'gh repo create ' + repo_name + " --" + repository_info['visibility']
    print("==================================================")
    print("================ Create Repo =====================")
    print(myCommand)
    print("==================================================")
    ssh_url = "git@github.com:" + repo_name

    success, output = call_cmd(myCommand)
    if success:
        return {
            'repo_name': repo_name,
            'ssh_url': ssh_url,
            'repo_url': output
        }
    else:
        print(output)
        return None

def perform_migration(gitlab_info, github_info):
    """
    Perform the actual git migration
    """
    migrate_cmd = f"bash git_shell_move.sh {gitlab_info['ssh_url']} {github_info['ssh_url']} {github_info['repo_url']}"
    print(migrate_cmd)
    success, output = call_cmd(migrate_cmd)
    print(success)
    print(output)

def process_repository(gl:gitlab.Gitlab, gitlab_info, group_name, org_name):
    """
    Process an individual GitLab project
    """
    print(gitlab_info)
    github_info = create_github_repository(gitlab_info, group_name, org_name)
    perform_migration(gitlab_info, github_info)
    
    # Archive gitlab project
    project = gl.projects.get(gitlab_info['id'])
    project.archive()

    # Set default branch
    call_cmd("gh repo edit " + github_info['repo_name'] + " --default-branch " + gitlab_info['default_branch'])

if __name__ == "__main__":
    loop_repositories(
        "https://gitlab.com",
        "glpat--Ro8rnCP7iBJ1MhNH13Z",
        "UM-CDS",
        "maastrichtu-cds"
    )