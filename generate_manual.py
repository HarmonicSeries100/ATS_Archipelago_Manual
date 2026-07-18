import constants as const
import generate_manual as gen_man


def get_location_object(location):
    loc_obj = {
        "name": location["Location_Name"],
        "region": location["Region"],
        "category": [
            const.LOC_CATEGORY_MAPPING[location["Loc_Type"]]
        ],
        "requires": ""
    }
    loc_obj["category"].append(const.DLC_CATEGORY_PREFIX + location["State_DLC"])
    loc_obj["category"].extend([item for item in location["State"].split('; ')])
    return loc_obj


def get_fast_travel_item_from_location(location):
    fast_travel_obj = {
        "count": 1,
        "name": f"{const.UNLOCK_FT_ITEM_PREFIX}{location["Location_Name"]}",
        "category": [
            const.FT_UNLOCK_CATEGORY
        ],
        "progression": True
    }
    fast_travel_obj["category"].append(const.DLC_CATEGORY_PREFIX + location["State_DLC"])
    fast_travel_obj["category"].extend([item for item in location["State"].split('; ')])
    return fast_travel_obj


def get_region_object(region):
    region_obj = {
        "connects_to": [item for item in region["Connections"].split('; ')],
        "requires": f"|{const.UNLOCK_REGION_ITEM_PREFIX}{region['Region_Name']}|"
    }
    return region_obj


def get_region_unlock_item_from_region(region):
    region_unlock_item_obj = {
        "count": 1,
        "name": f"{const.UNLOCK_REGION_ITEM_PREFIX}{region["Region_Name"]}",
        "category": [
            const.REGION_UNLOCK_CATEGORY
        ],
        "progression": True
    }
    region_unlock_item_obj["category"].append(const.DLC_CATEGORY_PREFIX + region["State_DLC"])
    region_unlock_item_obj["category"].extend([item for item in region["State"].split('; ')])
    return region_unlock_item_obj


def get_starting_item(region, city_list):
    starting_item_obj = {
        "if_previous_item": [f"{const.UNLOCK_REGION_ITEM_PREFIX}{region}"],
        "items": [f"{const.UNLOCK_FT_ITEM_PREFIX}{city}" for city in city_list],
        "random": 1
    }
    return starting_item_obj


def initialize_lists():
    # Note, meta.json, options.json is not generated
    json_data = {
        'categories': {
            "$schema": "https://github.com/ManualForArchipelago/Manual/raw/main/schemas/Manual.categories.schema.json",
            const.START_REGION_CATEGORY: {
                'hidden': True
            },
            const.STATE_CAPITAL_CATEGORY: {
                'hidden': True
            }
        },
        'game': {
            "$schema": "https://github.com/ManualForArchipelago/Manual/raw/main/schemas/Manual.game.schema.json",
            "game": "AmericanTruckSimulator",
            "creator": "HarmonicSeries",
            "filler_item_name": const.FILLER_ITEM_NAME,
            "starting_items": [
                {
                    "item_categories": [const.START_REGION_CATEGORY],
                    "random": 1
                }
            ]
        },
        'events': {
            "$schema": "https://github.com/ManualForArchipelago/Manual/raw/main/schemas/Manual.events.schema.json",
            "data": [
                {
                    "name": const.GOAL_EVENT_NAME,
                    "category": [const.GOAL_CATEGORY],
                    "requires": f"{{OptionCountPercent({const.GOAL_COLLECT_NAME},percent_stamps_required)}}",
                    "visible": True
                }
            ]
        },
        'items': {
            "$schema": "https://github.com/ManualForArchipelago/Manual/raw/main/schemas/Manual.items.schema.json",
            "data":
                [
                    {
                        "count": 1,
                        "name": const.GOAL_COLLECT_NAME,
                        "category": [
                            const.GOAL_CATEGORY
                        ],
                        "progression": True
                    },
                    {
                        "count": 1,
                        "name": const.GOAL_ITEM_NAME,
                        "category": [
                            const.GOAL_CATEGORY
                        ],
                        "progression": True,
                        "local": True
                    },
                    {
                        "count": 1,
                        "name": "Wiper Blades",
                        "category": [
                            const.VEHICLE_UNLOCK_CATEGORY
                        ],
                        "useful": True
                    },
                    {
                        "count": 1,
                        "name": "Headlights",
                        "category": [
                            const.VEHICLE_UNLOCK_CATEGORY
                        ],
                        "useful": True
                    },
                ],
        },
        'locations': {
            "$schema": "https://github.com/ManualForArchipelago/Manual/raw/main/schemas/Manual.locations.schema.json",
            "data":
                [
                    {
                        "name": "Victory",
                        "region": const.FT_HUB_NAME,
                        "victory": True,
                        "category": [
                            const.VICTORY_CATEGORY
                        ],
                        "requires": f"|{const.GOAL_ITEM_NAME}|"
                    }
                ],
        },
        'regions': {
            "$schema": "https://github.com/ManualForArchipelago/Manual/raw/main/schemas/Manual.regions.schema.json"
        },
        'options': {
            "$schema": "https://raw.githubusercontent.com/ManualForArchipelago/Manual/main/schemas/Manual.options.schema.json",
            "_comment": "Add a _ before an option name to comment it out and it wont be added to the apworld",
            "core": {
                "goal": {
                    "_comment": [
                        "Using 'goal' as the name of an option let you override some of the generated goal parameters"
                    ],
                    "display_name": "The End Objective",
                    "description": "How to End your Randomized playthrough.",
                    "aliases": {
                        "easiest": 0
                    },
                    "hidden": False
                },
                "death_link": {
                    "default": False
                },
                "filler_traps": {
                    "_comment": "Using values here let you set a 'recommended' filler_trap percentage or even a default percentage",
                    "values": {
                        "recommended": 20
                    }
                }
            },
            "user": {
                "number_of_states": {
                    "type": "Range",
                    "display_name": "Number of States",
                    "description": [
                        "Choose the number of states to include in the randomizer. 2-3 recommended for syncs"
                    ],
                    "range_start": 1,
                    "default": 2,
                    "range_end": 4
                },
                "number_of_stamps_available": {
                    "type": "Range",
                    "display_name": "Number of Stamps Available",
                    "description": "Number of National Park Stamps available in the randomizer",
                    "range_start": 2,
                    "default": 5,
                    "range_end": 12
                },
                "percent_stamps_required": {
                    "type": "Range",
                    "display_name": "Percent of Stamps Required",
                    "description": "Percent of National Park Stamps required to complete the passport",
                    "range_start": 1,
                    "default": 80,
                    "range_end": 100
                }
            }
        }
    }
    return json_data


def get_state_capital_location(location):
    state_capital_obj = {
        "name": const.STATE_CAPITAL_LOC_PREFIX + location['Location_Name'],
        "region": location["Region"],
        "category": [
            const.STATE_CAPITAL_CATEGORY,
            const.VICTORY_CATEGORY
        ],
        "requires": f"|{const.GOAL_EVENT_NAME}|",
        "place_item": [const.GOAL_ITEM_NAME]
    }
    state_capital_obj["category"].append(const.DLC_CATEGORY_PREFIX + location["State_DLC"])
    state_capital_obj["category"].extend([item for item in location["State"].split('; ')])
    return state_capital_obj


def get_own_dlc_option(dlc_name):
    own_dlc_obj = {
        "type": "Toggle",
        "display_name": f"Own {dlc_name} DLC",
        "description": f"Do you own the {dlc_name} DLC?",
        "default": True,
        "group": "DLC"
    }
    return own_dlc_obj


def get_state_preference_option(state_name):
    state_pref_obj = {
        "type": "Range",
        "display_name": f"{state_name} Preference",
        "description": [
            f"Preference setting for {state_name}. Choose a weighting between 0 and 100",
            "0 will always exclude the state from being picked",
            "100 will always include the state",
            "If there are more '100' states than the number_of_states option, randomly choose between them with equal weighting"
        ],
        "default": 50,
        "range_start": 0,
        "range_end": 100,
        "group": "State_Preferences"
    }
    return state_pref_obj


def generate_fast_travel_regions(json_data, garage_city_index):
    unlock_item_list = []
    json_data['regions'][const.FT_HUB_NAME] = {
        "starting": True,
        "connects_to": []
    }
    for region_name, city_list in garage_city_index.items():
        unlock_item_list.append(f"{const.UNLOCK_REGION_ITEM_PREFIX}{region_name}")
        ft_region_name = f"{const.FT_REGION_PREFIX}{region_name}"
        json_data['regions'][const.FT_HUB_NAME]["connects_to"].append(ft_region_name)
        json_data['regions'][ft_region_name] = {
            "connects_to": [const.FT_HUB_NAME, region_name],
            "requires": f"|{const.UNLOCK_REGION_ITEM_PREFIX}{region_name}| AND ({" OR ".join([f"|{const.UNLOCK_FT_ITEM_PREFIX}{city}|" for city in city_list])})"
        }
    for index, item in enumerate(json_data['items']['data']):
        if item['name'] in unlock_item_list:
            json_data['items']['data'][index]["category"].append(const.START_REGION_CATEGORY)
    return json_data


def generate_starting_items(json_data, garage_city_index):
    for region, city_list in garage_city_index.items():
        json_data['game']['starting_items'].append(gen_man.get_starting_item(region, city_list))
    return json_data