import json


def create_program_from_file(ctx, path):
    with open(path, 'r') as file:
        data = json.load(file)
    vertex_shaders = []
    for vs_path in data["vertex_shaders"]:
        with open(vs_path, 'r') as file:
            vertex_shaders.append(ctx.vertex_shader(file.read()))

    fragment_shaders = []
    for fs_path in data["fragment_shaders"]:
        with open(fs_path, 'r') as file:
            fragment_shaders.append(ctx.fragment_shader(file.read()))

    return ctx.program(vertex_shaders + fragment_shaders)
