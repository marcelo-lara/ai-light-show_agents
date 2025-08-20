def write_file(file_path: str, content: str):
    with open(file_path, 'w') as f:
        f.write(content)

def read_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()