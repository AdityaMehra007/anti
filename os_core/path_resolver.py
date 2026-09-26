import os

def resolve_data_path(workspace, filename):
    p_data = os.path.join(workspace, 'data', filename)
    if os.path.exists(p_data):
        return p_data
    p_root = os.path.join(workspace, filename)
    if os.path.exists(p_root):
        return p_root
    return p_data
