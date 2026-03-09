# This script generates the following JSON files for the manual
# categories.json
# game.json
# items.json
# locations.json
# regions.json
# options.json

import csv, json

START_REGION_CATEGORY = "Start Region"
FT_UNLOCK_CATEGORY = "Fast Travel Unlock"
REGION_UNLOCK_CATEGORY = "Region Unlock"
DLC_CATEGORY_PREFIX = "DLC - "
DLC_OPTION_PREFIX = "own_"
UNLOCK_REGION_ITEM_PREFIX = "Unlock "
UNLOCK_FT_ITEM_PREFIX = "Unlock Fast Travel - "
FT_REGION_PREFIX = "FT - "
FT_HUB_NAME = "FT Hub"
FILLER_ITEM_NAME = "Nice Photograph"
GOAL_ITEM_NAME = "National Park Passport Stamp"
GOAL_CATEGORY = "National Park Passport Stamp"
GOAL_ITEM_COUNT = 4
GOAL_ITEM_REQUIRED = 4
VICTORY_CATEGORY = "Victory"
LOC_CATEGORY_MAPPING = {
    "City": "City",
    "Photo Trophy": "Photo Trophy Point",
    "Viewpoint": "Viewpoint"
}
VEHICLE_UNLOCK_CATEGORY = "Vehicle Unlock"


def initialize_lists():
    # Note, meta.json, options.json is not generated
    json_data = {
        'categories': {
            START_REGION_CATEGORY: {
                'hidden': 'true'
            }
        },
        'game': {
            "$schema": "https://github.com/ManualForArchipelago/Manual/raw/main/schemas/Manual.game.schema.json",
            "game": "AmericanTruckSimulator",
            "creator": "HarmonicSeries",
            "filler_item_name": FILLER_ITEM_NAME,
            "starting_items": [
                {
                    "item_categories": [START_REGION_CATEGORY],
                    "random": 1
                }
            ]
        },
        'items': [
            {
                "count": GOAL_ITEM_COUNT,
                "name": GOAL_ITEM_NAME,
                "category": [
                    GOAL_ITEM_NAME
                ],
                "progression": True
            },
            {
                "count": 1,
                "name": "Wiper Blades",
                "category": [
                    VEHICLE_UNLOCK_CATEGORY
                ],
                "useful": True
            },
            {
                "count": 1,
                "name": "Headlights",
                "category": [
                    VEHICLE_UNLOCK_CATEGORY
                ],
                "useful": True
            },
        ],
        'locations': [
            {
                "name": "Victory",
                "region": FT_HUB_NAME,
                "victory": True,
                "category": [
                    VICTORY_CATEGORY
                ],
                "requires": f"|{GOAL_ITEM_NAME}:{GOAL_ITEM_REQUIRED}|"
            }
        ],
        'regions': {},
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
                    "hidden": "false"
                },
                "death_link": {
                    "default": "false"
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
                }
            }
        }
    }
    return json_data


def get_location_object(location):
    loc_obj = {
        "name": location["Location_Name"],
        "region": location["Region"],
        "category": [
            LOC_CATEGORY_MAPPING[location["Loc_Type"]]
        ],
        "requires": ""
    }
    loc_obj["category"].append(DLC_CATEGORY_PREFIX + location["State_DLC"])
    loc_obj["category"].extend([item for item in location["State"].split('; ')])
    return loc_obj


def get_fast_travel_item_from_location(location):
    fast_travel_obj = {
        "count": 1,
        "name": f"{UNLOCK_FT_ITEM_PREFIX}{location["Location_Name"]}",
        "category": [
            FT_UNLOCK_CATEGORY
        ],
        "progression": True
    }
    fast_travel_obj["category"].append(DLC_CATEGORY_PREFIX + location["State_DLC"])
    fast_travel_obj["category"].extend([item for item in location["State"].split('; ')])
    return fast_travel_obj


def get_region_object(region):
    region_obj = {
        "connects_to": [item for item in region["Connections"].split('; ')],
        "requires": f"|{UNLOCK_REGION_ITEM_PREFIX}{region['Region_Name']}|"
    }
    return region_obj


def get_region_unlock_item_from_region(region):
    region_unlock_item_obj = {
        "count": 1,
        "name": f"{UNLOCK_REGION_ITEM_PREFIX}{region["Region_Name"]}",
        "category": [
            REGION_UNLOCK_CATEGORY
        ],
        "progression": True
    }
    region_unlock_item_obj["category"].append(DLC_CATEGORY_PREFIX + region["State_DLC"])
    region_unlock_item_obj["category"].extend([item for item in region["State"].split('; ')])
    return region_unlock_item_obj


def get_starting_item(region, city_list):
    starting_item_obj = {
        "if_previous_item": [f"{UNLOCK_REGION_ITEM_PREFIX}{region}"],
        "items": [f"{UNLOCK_FT_ITEM_PREFIX}{city}" for city in city_list],
        "random": 1
    }
    return starting_item_obj


def process_location_csv(json_data):
    garage_cities = {}
    with (open('./resources/ats_manual_location_data.csv', 'r') as f):
        reader = csv.DictReader(f)
        for location in reader:
            # Handle categories and options
            dlc_state = location["State_DLC"]
            dlc_category = DLC_CATEGORY_PREFIX + dlc_state
            dlc_option = DLC_OPTION_PREFIX + dlc_state
            if dlc_category not in json_data['categories']:
                json_data['categories'][dlc_category] ={
                    "hidden": True,
                }
                if dlc_state != 'Base':
                    json_data['categories'][dlc_category]['yaml_option'] = [dlc_option]
            if dlc_option not in json_data['options']['user'] and dlc_state != 'Base':
                json_data['options']['user'][dlc_option] = {
                    "type": "Toggle",
                    "display_name": f"Own {dlc_state} DLC",
                    "description": f"Do you own the {dlc_state} DLC?",
                    "default": True,
                    "group": "DLC"
                }

            # Handle locations and items
            json_data['locations'].append(get_location_object(location))
            if location['Has_Garage'] == 'Y':
                json_data['items'].append(get_fast_travel_item_from_location(location))
                try:
                    garage_cities[location['Region']].append(location['Location_Name'])
                except KeyError:
                    garage_cities[location['Region']] = [location['Location_Name']]
    return json_data, garage_cities


def process_region_csv(json_data):
    with open('./resources/ats_manual_region_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for region in reader:
            json_data['regions'][region["Region_Name"]] = get_region_object(region)
            json_data['items'].append(get_region_unlock_item_from_region(region))
    return json_data


def generate_fast_travel_regions(json_data, garage_city_index):
    unlock_item_list = []
    json_data['regions'][FT_HUB_NAME] = {
        "starting": True,
        "connects_to": []
    }
    for region_name, city_list in garage_city_index.items():
        unlock_item_list.append(f"{UNLOCK_REGION_ITEM_PREFIX}{region_name}")
        ft_region_name = f"{FT_REGION_PREFIX}{region_name}"
        json_data['regions'][FT_HUB_NAME]["connects_to"].append(ft_region_name)
        json_data['regions'][ft_region_name] = {
            "connects_to": [FT_HUB_NAME, region_name],
            "requires": f"|{UNLOCK_REGION_ITEM_PREFIX}{region_name}| AND ({" OR ".join([f"|{UNLOCK_FT_ITEM_PREFIX}{city}|" for city in city_list])})"
        }
    for index, item in enumerate(json_data['items']):
        if item['name'] in unlock_item_list:
            json_data['items'][index]["category"].append(START_REGION_CATEGORY)
    return json_data


def generate_starting_items(json_data, garage_city_index):
    for region, city_list in garage_city_index.items():
        json_data['game']['starting_items'].append(get_starting_item(region, city_list))
    return json_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    json_data = initialize_lists()
    json_data, garage_city_index = process_location_csv(json_data)
    json_data = process_region_csv(json_data)
    json_data = generate_fast_travel_regions(json_data, garage_city_index)
    json_data = generate_starting_items(json_data, garage_city_index)
    for file in json_data:
        json.dump(json_data[file], open("./manual_americantrucksimulator_harmonicseries/data/" + file + ".json", "w"))
