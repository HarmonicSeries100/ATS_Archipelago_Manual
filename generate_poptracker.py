import json

def to_snake_case(name: str) -> str:
    snake_str: str = name.lower()
    snake_str = snake_str.replace("'", "")
    snake_str = snake_str.replace("\"", "")
    snake_str = snake_str.replace(" ", "_")
    snake_str = snake_str.replace("\\", "_")
    snake_str = snake_str.replace("/", "_")
    snake_str = snake_str.replace(":", "_")
    return snake_str

def generate_poptracker_items(manual_items):
    poptracker_items: list[dict[str, any]] = []
    for item in manual_items:
        if (("progression" not in item or not item["progression"]) and
           ("progression_skip_balancing" not in item or not item["progression_skip_balancing"])):
            continue
        poptracker_item: dict[str, any] = {}
        count: int = int(item["count"]) if "count" in item else 1
        has_multiple: bool = count > 1
        poptracker_item["name"] = item["name"]
        poptracker_item["type"] = "consumable" if has_multiple else "toggle"
        poptracker_item["loop"] = "true"
        poptracker_item["img"] = f"images/items/{to_snake_case(item['name'])}.png"
        poptracker_item["codes"] = to_snake_case(item["name"])
        if has_multiple:
            poptracker_item["min_quantity"] = 0
            poptracker_item["max_quantity"] = count
        poptracker_items.append(poptracker_item)
    return poptracker_items

def poptracker_item_fix(poptracker_items, GOAL_COLLECT_NAME):
    for item in poptracker_items:
        if item["name"] == GOAL_COLLECT_NAME:
            item["type"] = "consumable"
            item["min_quantity"] = 0
            item["max_quantity"] = 1
    return poptracker_items
