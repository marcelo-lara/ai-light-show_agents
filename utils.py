def write_file(file_path: str, content: str):
    with open(file_path, 'w') as f:
        f.write(content)
