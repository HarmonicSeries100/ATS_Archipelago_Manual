import constants as const
from util import to_snake_case, get_child_node_by_name

def initialize_poptracker_layout_data():
    poptracker_layout_data = {}
    poptracker_layout_data["items"] = {
        "shared_item_grid": {
            "type": "group",
            "header": "Passport Items",
            "content": {
                "type": "itemgrid",
                "h_alignment": "left",
                "item_width": 48,
                "item_height": 48,
                "rows": [
                    [
                        "national_park_passport_stamp",
                        "number_of_stamps_required",
                        "validated_passport"
                    ]
                ]
            }
        }
    }
    poptracker_layout_data["tracker"] = {
        "tracker_default": {
            "type": "container",
            "background": "#111111",
            "content": {
                "type": "tabbed",
                "tabs": [
                    {
                        "title": "Victory",
                        "content": {
                            "type": "layout",
                            "key": "victory_island_layout"
                        }  
                    }
                ]
            }
        }
    }
    poptracker_layout_data["options_layout"] = {
        "settings_popup": {
            "type": "array",
            "orientation": "horizontal",
            "v_alignment": "top",
            "content": [
                {
                    "type": "group",
                    "header": "Game Options",
                    "content": {
                        "type": "itemgrid",
                        "item_width": 48,
                        "item_height": 48,
                        "item_v_alignment": "center",
                        "rows": [
                            [
                                "number_of_stamps_available",
                                "percent_stamps_required",
                                "number_of_stamps_required"
                            ]
                        ]
                    }
                },
                {
                    "type": "group",
                    "header": "DLC Owned",
                    "content": {
                        "type": "itemgrid",
                        "item_width": 64,
                        "item_height": 64,
                        "item_v_alignment": "center",
                        "rows": [
                            []
                        ]
                    }
                },
                {
                    "type": "group",
                    "header": "State Options",
                    "content": {
                        "type": "itemgrid",
                        "item_width": 64,
                        "item_height": 64,
                        "item_v_alignment": "center",                 
                        "rows": [
                            []
                        ]
                    }
                }
            ]
        }
    }
    poptracker_layout_data["victory_island"] = {
       f"victory_island_layout": {
            "type": "dock",
            "background": "#222228",
            "content": [
                {
                    "type": "map",
                    "maps": [
                        "victory_island_map"
                    ]
                },
                {
                    "type": "array",
                    "dock": "left",
                    "orientation": "vertical",
                    "content": [
                        {
                            "type": "layout",
                            "key": "shared_item_grid"
                        }
                    ]
                }
            ]
        }
    }
    return poptracker_layout_data

def get_tracker_tab_layout_node(state_name, state_code):
    tab_layout_node = {
        "title": state_name,
        "content": {
            "type": "layout",
            "key": f"{state_code}_layout"
        }
    }
    return tab_layout_node

def get_state_layout(state_name, state_code):
    state_layout_node = {
        f"{state_code}_layout": {
            "type": "dock",
            "background": "#222228",
            "content": [
                {
                    "type": "map",
                    "maps": [
                        f"{state_code}_map"
                    ]
                },
                {
                    "type": "array",
                    "dock": "left",
                    "orientation": "vertical",
                    "content": [
                        {
                            "type": "layout",
                            "key": "shared_item_grid"
                        },
                        {
                            "type": "group",
                            "header": f"{state_name} Items",
                            "content": {
                                "type": "array",
                                "orientation": "vertical",
                                "margin": "10,5,5,5",
                                "content": []
                            }
                        }
                    ]
                }
            ]
        }
    }
    return state_layout_node

def get_region_layout_node(region):
    region_name = region["Region_Name"]
    region_code = to_snake_case(region_name)
    region_layout_node = {
        "type": "group",
        "header": region_name,
        "content": {
            "type": "itemgrid",
            "item_size": 32,
            "h_alignment": "left",
            "rows": [
                [const.POPTRACKER_UNLOCK_ITEM_PREFIX + region_code]
            ]
        }
    }
    return region_layout_node

def add_ft_item_to_layout(location, pop_layout_data):
    state_name = location["State"]
    state_code = to_snake_case(state_name)
    region_name = location["Region"]
    region_code = to_snake_case(region_name)
    location_code = to_snake_case(location["Location_Name"])
    regions_node = pop_layout_data[state_code][f"{state_code}_layout"]["content"][1]["content"][1]["content"]["content"]
    region_index, region_node = get_child_node_by_name(regions_node, region_name, key="header")
    rows_node = region_node["content"]["rows"]
    rows_node = add_item_to_row(rows_node, const.POPTRACKER_UNLOCK_FT_ITEM_PREFIX+location_code, const.NUMBER_OF_ITEM_COLUMNS)
    pop_layout_data[state_code][f"{state_code}_layout"]["content"][1]["content"][1]["content"]["content"][region_index]["content"]["rows"]=rows_node
    return pop_layout_data

def add_item_to_row(rows_node, item_text, row_width):
    last_row_length = len(rows_node[-1])
    if last_row_length == row_width:
        rows_node.append([item_text])
    else:
        rows_node[-1].append(item_text)
    return rows_node