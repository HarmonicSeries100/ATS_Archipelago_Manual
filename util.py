def to_snake_case(name: str) -> str:
    snake_str: str = name.lower()
    snake_str = snake_str.replace("'", "")
    snake_str = snake_str.replace("\"", "")
    snake_str = snake_str.replace(" ", "_")
    snake_str = snake_str.replace("\\", "_")
    snake_str = snake_str.replace("/", "_")
    snake_str = snake_str.replace(":", "_")
    return snake_str


def get_child_node_by_name(data_list, name, key="name"):
    match_index = None
    match_node = None
    for index, node in enumerate(data_list):
        if node.get(key) == name:
            match_index = index
            match_node = node
    return match_index, match_node