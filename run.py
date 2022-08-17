import gitlab

gl = gitlab.Gitlab('https://gitlab.com', private_token='glpat--Ro8rnCP7iBJ1MhNH13Z')
groups = gl.groups.list(get_all=True)
for group in groups:
    visibility = group.attributes['visibility']
    full_path = group.attributes['full_path']
    description = group.attributes['description']
    if not full_path.startswith("medicaldataworks"):
        continue
    myGroup = gl.groups.get(group.attributes['id'])
    projects = myGroup.projects.list()
    for x in projects:
        # project = gl.projects.get(x.attributes["id"])
        ssh_url = x.attributes["ssh_url_to_repo"]
        archived = x.attributes['archived']
        visibility = x.attributes['visibility']
        default_branch = x.attributes['default_branch']
        empty_repo = x.attributes['empty_repo']