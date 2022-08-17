import gitlab

gl = gitlab.Gitlab('https://gitlab.com', private_token='')
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
        project = gl.projects.get(x.attributes["id"])
        print(x.attributes["ssh_url_to_repo"])
        print(x)