# This script generates the following JSON files for the manual
# categories.json
# game.json
# items.json
# locations.json
# regions.json
# options.json

import csv, json
import constants as const
import generate_poptracker as gen_pop

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


def get_state_capital_location(location):
    state_capital_obj = {
        "name": f"Passport Validation Center - {location['Location_Name']}",
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


def process_location_csv(json_data, poptracker_item_data):
    garage_cities = {}
    with (open('./resources/ats_manual_location_data.csv', 'r') as f):
        reader = csv.DictReader(f)
        for location in reader:
            # Handle locations and items
            json_data['locations']['data'].append(get_location_object(location))
            if location['Has_Garage'] == 'Y':
                json_data['items']['data'].append(get_fast_travel_item_from_location(location))
                try:
                    garage_cities[location['Region']].append(location['Location_Name'])
                except KeyError:
                    garage_cities[location['Region']] = [location['Location_Name']]

            poptracker_item_data["items"].append(get_fast_travel_item_from_location(location))
                
            if location['State_Capital'] == 'Y':
                json_data['locations']['data'].append(get_state_capital_location(location))
    return json_data, garage_cities, poptracker_item_data


def process_region_csv(json_data, poptracker_item_data):
    with open('./resources/ats_manual_region_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for region in reader:
            json_data['regions'][region["Region_Name"]] = get_region_object(region)
            json_data['items']['data'].append(get_region_unlock_item_from_region(region))

            poptracker_item_data['items'].append(gen_pop.get_poptracker_region_unlock_item(region))


    return json_data, poptracker_item_data

def process_state_csv(json_data,poptracker_item_data):
    with open('./resources/ats_manual_state_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for state in reader:
            dlc_name = state["DLC"]
            dlc_category = const.DLC_CATEGORY_PREFIX + dlc_name
            dlc_option = const.DLC_OPTION_PREFIX + state["DLC_id"]

            if dlc_category not in json_data['categories']:
                json_data['categories'][dlc_category] = {
                    "hidden": True,
                }
                if dlc_name != 'Base':
                    json_data['categories'][dlc_category]['yaml_option'] = [dlc_option]

            if dlc_option not in json_data['options']['user'] and dlc_name != 'Base':
                json_data['options']['user'][dlc_option] = get_own_dlc_option(dlc_name)

            state_id = state["state_id"]
            state_name = state["state_display_name"]
            state_pref_option = state_id + const.STATE_PREFERENCE_SUFFIX
            json_data['options']['user'][state_pref_option] = get_state_preference_option(state_name)
            
            poptracker_item_data["options"].append(gen_pop.get_poptracker_state_option_item(state_id, state_name))

    return json_data, poptracker_item_data


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
        json_data['game']['starting_items'].append(get_starting_item(region, city_list))
    return json_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    json_data = initialize_lists()
    poptracker_item_data = gen_pop.initialize_poptracker_items()
    json_data, poptracker_item_data = process_state_csv(json_data, poptracker_item_data)
    json_data, poptracker_item_data = process_region_csv(json_data, poptracker_item_data)
    json_data, garage_city_index, poptracker_item_data = process_location_csv(json_data, poptracker_item_data)
    json_data = generate_fast_travel_regions(json_data, garage_city_index)
    json_data = generate_starting_items(json_data, garage_city_index)
    for file in json_data:
        json.dump(json_data[file], open("./manual_americantrucksimulator_harmonicseries/data/" + file + ".json", "w"),
                  indent=2)
    
    for file in poptracker_item_data:
        json.dump(poptracker_item_data[file], open(f"./ats_harmonic_series-main/items/{file}.json","w"), indent=2)
    #TODO: Generate locations.json for poptracker. Every region is a "parent" and every location check has a map location
    #TODO: Add a section in location_data.csv to group close-together locations, to make use of "sections"
    #TODO: Generate item_mapping.lua
    #TODO: Generate location_mapping.lua
    #TODO: Create custom logic in logic.lua
    # Logic for location checks. Locations will have in the access rules calling the function with all of their neighbors as parameters
    # Recursive search function to check for neighbors
    # Fast travel points have ft_<location name>_##
    # Write custom function for the "all stamps collected" event. Put function in access rules for state capital locations
    # Add visibility rules depending on chosen state and DLC owned
    # Get chosen states from slot data - Possible!
    #TODO: Create map PNGs
    #TODO: Add map coordinates to resources
    #TODO: Generate layouts?
    # Have a "progressive" item for each state. Level 0: DLC Unowned, Level 1: DLC Owned, Level 2: Chosen in Randomizer, Level 3: Victory State
    # Settings page will have a grid for all the states
    # Also have item for number of stamps available, number required, change min count of stamp item to the number required
