import gitlab

gl = gitlab.Gitlab('https://gitlab.com', private_token='')
groups = gl.groups.list(get_all=True)
for group in groups:
    visibility = group.attributes['visibility']
    full_path = group.attributes['full_path']
    description = group.attributes['description']
    