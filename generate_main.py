# This script generates the following JSON files for the manual
# categories.json
# game.json
# items.json
# locations.json
# regions.json
# options.json

import csv, json
import constants as const
import generate_manual as gen_man
import generate_poptracker as gen_pop
from util import to_snake_case

def process_state_csv(json_data,poptracker_item_data,poptracker_map_data,poptracker_location_data):
    with open('./resources/ats_manual_state_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for state in reader:
            dlc_id = state["DLC_id"]
            dlc_name = state["DLC"]
            dlc_category = const.DLC_CATEGORY_PREFIX + dlc_name
            dlc_option = const.DLC_OPTION_PREFIX + dlc_id

            if dlc_category not in json_data['categories']:
                json_data['categories'][dlc_category] = {
                    "hidden": True,
                }
                if dlc_name != 'Base':
                    json_data['categories'][dlc_category]['yaml_option'] = [dlc_option]

            if dlc_option not in json_data['options']['user'] and dlc_name != 'Base':
                json_data['options']['user'][dlc_option] = gen_man.get_own_dlc_option(dlc_name)

            state_id = state["state_id"]
            state_name = state["state_display_name"]
            state_pref_option = state_id + const.STATE_PREFERENCE_SUFFIX
            json_data['options']['user'][state_pref_option] = gen_man.get_state_preference_option(state_name)
            
            poptracker_item_data["options"].append(gen_pop.get_poptracker_dlc_owned_item(dlc_id, dlc_name))
            poptracker_item_data["options"].append(gen_pop.get_poptracker_state_option_item(state_id, state_name))

            poptracker_map_data.append(gen_pop.get_poptracker_map(state_id))

            poptracker_location_data[dlc_id] = []

    return json_data, poptracker_item_data, poptracker_map_data, poptracker_location_data


def process_region_csv(json_data, poptracker_item_data, poptracker_location_data):
    region_dlc_index = {}
    with open('./resources/ats_manual_region_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for region in reader:
            json_data['regions'][region["Region_Name"]] = gen_man.get_region_object(region)
            json_data['items']['data'].append(gen_man.get_region_unlock_item_from_region(region))

            poptracker_item_data['items'].append(gen_pop.get_poptracker_region_unlock_item(region))

            poptracker_location_data, region_dlc_index = gen_pop.get_poptracker_region_location(region, poptracker_location_data, region_dlc_index)

    return json_data, poptracker_item_data, poptracker_location_data, region_dlc_index


def process_location_csv(json_data, poptracker_item_data, poptracker_location_data, region_dlc_index):
    garage_cities = {}
    with (open('./resources/ats_manual_location_data.csv', 'r') as f):
        reader = csv.DictReader(f)
        for location in reader:
            # Handle locations and items
            json_data['locations']['data'].append(gen_man.get_location_object(location))
            if location['Has_Garage'] == 'Y':
                json_data['items']['data'].append(gen_man.get_fast_travel_item_from_location(location))
                try:
                    garage_cities[location['Region']].append(location['Location_Name'])
                except KeyError:
                    garage_cities[location['Region']] = [location['Location_Name']]

                poptracker_item_data["items"].append(gen_pop.get_poptracker_fast_travel_unlock_item(location))
                
            if location['State_Capital'] == 'Y':
                json_data['locations']['data'].append(gen_man.get_state_capital_location(location))

            poptracker_location_data = gen_pop.get_poptracker_location(location, poptracker_location_data, region_dlc_index)
    return json_data, garage_cities, poptracker_item_data, poptracker_location_data


if __name__ == '__main__':
    json_data = gen_man.initialize_lists()
    pop_item_data = gen_pop.initialize_poptracker_items()
    pop_loc_data = gen_pop.initialize_poptracker_locations()
    pop_map_data = gen_pop.initialize_poptracker_maps()
    json_data, pop_item_data, pop_map_data, pop_loc_data = process_state_csv(json_data, pop_item_data, pop_map_data, pop_loc_data)
    json_data, pop_item_data, pop_loc_data, region_dlc_index = process_region_csv(json_data, pop_item_data, pop_loc_data)
    json_data, garage_city_index, pop_item_data, pop_loc_data = process_location_csv(json_data, pop_item_data, pop_loc_data, region_dlc_index)
    json_data = gen_man.generate_fast_travel_regions(json_data, garage_city_index)
    json_data = gen_man.generate_starting_items(json_data, garage_city_index)
    
    for file in json_data:
        json.dump(json_data[file], open("./manual_americantrucksimulator_harmonicseries/data/" + file + ".json", "w"),
                  indent=2)
    
    for file in pop_item_data:
        json.dump(pop_item_data[file], open(f"./ats_harmonic_series-main/items/{file}.json","w"), indent=2)

    for file in pop_loc_data:
        json.dump(pop_loc_data[file], open(f"./ats_harmonic_series-main/locations/{file}.json","w"), indent=2)

    json.dump(pop_map_data, open(f"./ats_harmonic_series-main/maps/ats_maps.json","w"), indent=2)
    #TODO: Fix issues in archipelago.lua
    #TODO: Generate item_mapping.lua
    #TODO: Generate location_mapping.lua
    #TODO: Generate init.lua

    #TODO: Create better pngs for cities, viewpoints, photo trophies locked/unlocked

    #TODO: Generate layouts?
    # Settings page will have a grid for all the states
    # Also have item for number of stamps available, number required

    #TODO: Add script for better deployment
