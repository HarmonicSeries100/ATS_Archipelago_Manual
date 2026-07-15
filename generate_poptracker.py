import json
import constants as const
from util import to_snake_case

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
            "max_quantity": 1
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
        }
    ]
    return poptracker_items


def get_poptracker_state_option_item(state_id, state_name):
    poptracker_state_option = {
        "name": f"{state_name} Option",
        "type": "progressive",
        "loop": "true",
        "stages": [
            {
                "img": f"images/flags/{state_id}_flag.png",
                "codes": const.DLC_OPTION_PREFIX + state_id
            },
            {
                "img": f"images/flags/{state_id}_flag.png",
                "img_mods": "overlay|images/overlay/check_overlay.png",
                "codes": state_id + const.POPTRACKER_STATE_CHOSEN_SUFFIX              
            },
            {
                "img": f"images/flags/{state_id}_flag.png",
                "img_mods": "overlay|images/overlay/trophy_overlay.png",
                "codes": state_id + const.POPTRACKER_VICTORY_STATE_SUFFIX                        
            }
        ]
    }
    return poptracker_state_option


def get_poptracker_region_unlock_item(region):
    region_unlock_item_obj = {
        "name": const.UNLOCK_REGION_ITEM_PREFIX + region["Region_Name"],
        "type": "toggle",
        "loop": "true",
        "codes": to_snake_case(const.UNLOCK_REGION_ITEM_PREFIX + region["Region_Name"]),
        "img": "images/items/region_unlock.png",
        "disabled_img": "images/items/region_lock.png"
    }
    return region_unlock_item_obj


def get_poptracker_fast_travel_unlock_item(location):
    fast_travel_unlock_item_obj = {
        "name": const.UNLOCK_FT_ITEM_PREFIX + location["Location_Name"],
        "type": "toggle",
        "loop": "true",
        "codes": to_snake_case(const.UNLOCK_FT_ITEM_PREFIX + location["Location_Name"]),
        "img": "images/items/fast_travel_unlock.png",
        "disabled_img": "images/items/fast_travel_lock.png"
    }
    return fast_travel_unlock_item_obj


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
