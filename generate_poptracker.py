import json
import constants as const
from util import to_snake_case


def get_child_node_by_name(data_list, name):
    match_index = None
    match_node = None
    for index, node in enumerate(data_list):
        if node.get("name") == name:
            match_index = index
            match_node = node
    return match_index, match_node


def initialize_poptracker_items():
    poptracker_items = {}
    poptracker_items["items"] = [
        {
            "name": const.GOAL_COLLECT_NAME,
            "type": "consumable",
            "loop": "true",
            "img": "images/items/national_park_passport_stamp.png",
            "codes": to_snake_case(const.GOAL_COLLECT_NAME),
            "min_quantity": 0,
            "max_quantity": 12
        },
        {
            "name": const.GOAL_ITEM_NAME,
            "type": "toggle",
            "loop": "true",
            "img": "images/items/validated_passport.png",
            "codes": to_snake_case(const.GOAL_ITEM_NAME)
        }
    ]
    poptracker_items["options"] = [
        {
            "name": "Number of Stamps Available",
            "type": "consumable",
            "loop": "true",
            "img": "images/items/national_park_passport_stamp.png",
            "codes": "number_of_stamps_available",
            "min_quantity": 2,
            "max_quantity": 12
        },
        {
            "name": "Percent Stamps Required",
            "type": "consumable",
            "loop": "true",
            "img": "images/items/national_park_passport_stamp_percent.png",
            "codes": "percent_stamps_required",
            "min_quantity": 1,
            "max_quantity": 100
        },
        {
            "name": "Number of Stamps Required",
            "type": "consumable",
            "loop": "true",
            "img": "images/items/national_park_passport_stamp.png",
            "codes": "number_of_stamps_required",
            "min_quantity": 2,
            "max_quantity": 12
        }
    ]
    return poptracker_items


def initialize_poptracker_locations():
    poptracker_locations = {}
    return poptracker_locations


def initialize_poptracker_maps():
    poptracker_maps = []
    return poptracker_maps


def get_poptracker_state_option_item(state_id, state_name):
    poptracker_state_option = {
        "name": f"{state_name} Option",
        "type": "progressive",
        "loop": "true",
        "stages": [
            {
                "img": f"images/flags/{state_id}.png",
                "codes": state_id + const.POPTRACKER_STATE_CHOSEN_SUFFIX              
            },
            {
                "img": f"images/flags/{state_id}.png",
                "img_mods": "overlay|images/overlay/trophy_overlay.png",
                "codes": state_id + const.POPTRACKER_VICTORY_STATE_SUFFIX                        
            }
        ]
    }
    return poptracker_state_option


def get_poptracker_dlc_owned_item(dlc_id, dlc_name):
    poptracker_dlc_owned = {
        "name": f"Owns {dlc_name}",
        "type": "toggle",
        "loop": "true",
        "codes": const.DLC_OPTION_PREFIX + dlc_id,
        "img": f"images/flags/{dlc_id}.png"
    }
    if dlc_id == "base": # Base DLC is all owned, so change type to "static"
        poptracker_dlc_owned["type"] = "static"
    
    return poptracker_dlc_owned


def get_poptracker_region_unlock_item(region):
    region_unlock_item_obj = {
        "name": const.UNLOCK_REGION_ITEM_PREFIX + region["Region_Name"],
        "type": "toggle",
        "loop": "true",
        "codes": const.POPTRACKER_UNLOCK_ITEM_PREFIX + to_snake_case(region["Region_Name"]),
        "img": "images/items/region_unlock.png",
        "disabled_img": "images/items/region_lock.png"
    }
    return region_unlock_item_obj


def get_poptracker_fast_travel_unlock_item(location):
    fast_travel_unlock_item_obj = {
        "name": const.UNLOCK_FT_ITEM_PREFIX + location["Location_Name"],
        "type": "toggle",
        "loop": "true",
        "codes": const.POPTRACKER_UNLOCK_FT_ITEM_PREFIX + to_snake_case(location["Location_Name"])+", "\
            +const.POPTRACKER_UNLOCK_FT_ITEM_PREFIX + to_snake_case(location["Region"]),
        "img": "images/items/fast_travel_unlock.png",
        "disabled_img": "images/items/fast_travel_lock.png"
    }
    return fast_travel_unlock_item_obj


def get_poptracker_region_location(region, poptracker_location_data, region_dlc_index):
    region_node = None
    region_name = region["Region_Name"]
    region_code = to_snake_case(region_name)
    connections = [to_snake_case(r) for r in region["Connections"].split('; ')]
    region_state = to_snake_case(region["State"])
    region_dlc = to_snake_case(region["State_DLC"])
    region_dlc_index[region_code] = region_dlc
    is_multistate = region["Multistate"] == "Y"

    if is_multistate:
        poptracker_location_data = get_poptracker_multistate_region(poptracker_location_data, region_name, region_code, region_state, region_dlc, connections)
        return poptracker_location_data, region_dlc_index

    region_rules = f"{const.DLC_OPTION_PREFIX+region_dlc}, "+\
        f"{region_state+const.POPTRACKER_STATE_CHOSEN_SUFFIX}, "+\
        f"$is_region_connected|{const.POPTRACKER_UNLOCK_FT_ITEM_PREFIX}|{"|".join([conn for conn in connections])}"
    
    region_node = {
        "name": region_code,
        "access_rules": region_rules,
        "visibility_rules": [
            f"{const.DLC_OPTION_PREFIX+region_dlc}, {region_state+const.POPTRACKER_STATE_CHOSEN_SUFFIX}"
        ],
        "children": []
    }
    poptracker_location_data[region_dlc].append(region_node)
    return poptracker_location_data, region_dlc_index


def get_poptracker_multistate_region(poptracker_location_data, region_name, region_code, region_state, region_dlc, connections):
    state_list = "|".join([to_snake_case(state) for state in region_state.split(";_")])
    region_rules = f"{const.DLC_OPTION_PREFIX+region_dlc}, $is_in_chosen_state|{state_list}, "+\
        f"$is_region_connected|{const.POPTRACKER_UNLOCK_FT_ITEM_PREFIX}|{"|".join([conn for conn in connections])}"
    
    region_node = {
        "name": region_code,
        "access_rules": region_rules,
        "visibility_rules": [
            f"{const.DLC_OPTION_PREFIX+region_dlc}"
        ],
        "children": []
    }

    poptracker_location_data[region_dlc].append(region_node)
    return poptracker_location_data

def get_poptracker_location(location, poptracker_location_data, region_dlc_index):
    loc_name = location["Location_Name"]
    loc_region_code = to_snake_case(location["Region"])
    loc_region_dlc = region_dlc_index[loc_region_code]
    loc_type = to_snake_case(location["Loc_Type"])
    loc_state = to_snake_case(location["State"])
    loc_dlc = to_snake_case(location["State_DLC"])
    loc_capital = location["State_Capital"]
    loc_group = location["Location_Group"]
    loc_x = location["Pop_X"]
    loc_y = location["Pop_Y"]
    is_multistate = location["Multistate"] == "Y"

    if not loc_group:
        loc_node = {
            "name": loc_name,
            "chest_unopened_img": f"images/items/{loc_type}_lock.png",
            "chest_opened_img": f"images/items/{loc_type}_unlock.png",
            "map_locations": [get_map_node(s, int(x), int(y), is_multistate) for s, x, y in zip(loc_state.split(";_"),loc_x.split("; "),loc_y.split("; "))],
            "sections":[
                {
                    "name": "",
                    "item_count": 1
                }
            ]
        }
        if loc_dlc != loc_region_dlc:
            loc_node["access_rules"] = [
                const.DLC_OPTION_PREFIX + loc_dlc
            ]
            loc_node["visibility_rules"] = [
                const.DLC_OPTION_PREFIX + loc_dlc
            ]
        index, _ = get_child_node_by_name(poptracker_location_data[loc_region_dlc], loc_region_code)
        poptracker_location_data[loc_region_dlc][index]["children"].append(loc_node)

    else:
        loc_region_index, _ = get_child_node_by_name(poptracker_location_data[loc_region_dlc], loc_region_code)
        loc_index, loc_node = get_child_node_by_name(poptracker_location_data[loc_region_dlc][loc_region_index]["children"], loc_group)
        if loc_node is None:
            loc_node = {
                "name": loc_group,
                "map_locations": [get_map_node(s, int(x), int(y), is_multistate) for s, x, y in zip(loc_state.split(";_"),loc_x.split("; "),loc_y.split("; "))],
                "sections": [
                    {
                        "name": loc_name,
                        "item_count": 1,
                        "chest_unopened_img": f"images/items/{loc_type}_lock.png",
                        "chest_opened_img": f"images/items/{loc_type}_unlock.png"
                    }
                ]
            }
        else:
            loc_node["sections"].append(
                {
                    "name": loc_name,
                    "item_count": 1,
                    "chest_unopened_img": f"images/items/{loc_type}_lock.png",
                    "chest_opened_img": f"images/items/{loc_type}_unlock.png"
                }
            )
        
        if loc_dlc != loc_region_dlc: #Use -1 index since relevant node will always be last one added
            loc_node["sections"][-1]["access_rules"] = [
                const.DLC_OPTION_PREFIX + loc_dlc
            ]
            loc_node["sections"][-1]["visibility_rules"] = [
                const.DLC_OPTION_PREFIX + loc_dlc
            ]
        
        if loc_capital:
            loc_node["sections"].append(
                {
                    "name": const.STATE_CAPITAL_LOC_PREFIX + loc_name,
                    "item_count": 1,
                    "chest_unopened_img": f"images/items/{loc_type}_lock.png",
                    "chest_opened_img": f"images/items/{loc_type}_unlock.png",
                    "access_rules": ["$has_enough_stamps"]
                }
            )
        if loc_index is None:
            poptracker_location_data[loc_region_dlc][loc_region_index]["children"].append(loc_node)
        else:
            poptracker_location_data[loc_region_dlc][loc_region_index]["children"][loc_index] = loc_node

    return poptracker_location_data


def get_map_node(state, x, y, is_multistate):
    map_node = {
        "map": f"{state}_map",
        "x": x,
        "y": y
    }
    if is_multistate:
        map_node["restrict_visibility_rules"] = [
            state + const.POPTRACKER_STATE_CHOSEN_SUFFIX
        ]
    return map_node


def get_poptracker_map(state):
    poptracker_map_obj = {
        "name": f"{state}_map",
        "location_size": 24,
        "location_border_thickness": 2,
        "location_shape": "rect",
        "img": f"images/maps/{state}_map.png"
    }
    return poptracker_map_obj


