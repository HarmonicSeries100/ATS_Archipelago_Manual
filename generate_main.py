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
import generate_pop_layouts as gen_pop_layout
from util import to_snake_case

def process_state_csv(json_data,pop_item_data,pop_map_data,pop_location_data,pop_layout_data):
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

                layout_row = pop_layout_data["options_layout"]["settings_popup"]["content"][1]["content"]["rows"]
                layout_row = gen_pop_layout.add_item_to_row(layout_row, const.DLC_OPTION_PREFIX+dlc_id, const.NUMBER_OF_OPTION_COLUMNS)
                pop_layout_data["options_layout"]["settings_popup"]["content"][1]["content"]["rows"]=layout_row

            if dlc_option not in json_data['options']['user'] and dlc_name != 'Base':
                json_data['options']['user'][dlc_option] = gen_man.get_own_dlc_option(dlc_name)

            state_code = state["state_id"]
            state_name = state["state_display_name"]
            state_pref_option = state_code + const.STATE_PREFERENCE_SUFFIX
            json_data['options']['user'][state_pref_option] = gen_man.get_state_preference_option(state_name)
            
            pop_item_data["options"].append(gen_pop.get_poptracker_dlc_owned_item(dlc_id, dlc_name))
            pop_item_data["options"].append(gen_pop.get_poptracker_state_option_item(state_code, state_name))

            pop_map_data.append(gen_pop.get_poptracker_map(state_code))

            pop_location_data[dlc_id] = []

            pop_layout_data["tracker"]["tracker_default"]["content"]["tabs"].append(gen_pop_layout.get_tracker_tab_layout_node(state_name, state_code))
            pop_layout_data[state_code] = gen_pop_layout.get_state_layout(state_name, state_code)
            layout_row = pop_layout_data["options_layout"]["settings_popup"]["content"][2]["content"]["rows"]
            layout_row = gen_pop_layout.add_item_to_row(layout_row, state_code+const.POPTRACKER_STATE_CHOSEN_SUFFIX, const.NUMBER_OF_OPTION_COLUMNS)
            pop_layout_data["options_layout"]["settings_popup"]["content"][2]["content"]["rows"]=layout_row

    return json_data, pop_item_data, pop_map_data, pop_location_data, pop_layout_data


def process_region_csv(json_data, pop_item_data, pop_loc_data, pop_layout_data):
    region_dlc_index = {}
    with open('./resources/ats_manual_region_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for region in reader:
            json_data['regions'][region["Region_Name"]] = gen_man.get_region_object(region)
            json_data['items']['data'].append(gen_man.get_region_unlock_item_from_region(region))

            pop_item_data['items'].append(gen_pop.get_poptracker_region_unlock_item(region))

            pop_loc_data, region_dlc_index = gen_pop.get_poptracker_region_location(region, pop_loc_data, region_dlc_index)

            for state in region["State"].split("; "):
                state_code = to_snake_case(state)
                pop_layout_data[state_code][f"{state_code}_layout"]["content"][1]["content"][1]["content"]["content"].append(gen_pop_layout.get_region_layout_node(region))

    return json_data, pop_item_data, pop_loc_data, region_dlc_index, pop_layout_data


def process_location_csv(json_data, pop_item_data, pop_loc_data, region_dlc_index, pop_layout_data):
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

                pop_item_data["items"].append(gen_pop.get_poptracker_fast_travel_unlock_item(location))
                pop_layout_data = gen_pop_layout.add_ft_item_to_layout(location, pop_layout_data)
                
            if location['State_Capital'] == 'Y':
                json_data['locations']['data'].append(gen_man.get_state_capital_location(location))

            pop_loc_data = gen_pop.get_poptracker_location(location, pop_loc_data, region_dlc_index)
    return json_data, garage_cities, pop_item_data, pop_loc_data, pop_layout_data


if __name__ == '__main__':
    json_data = gen_man.initialize_lists()
    pop_item_data = gen_pop.initialize_poptracker_items()
    pop_loc_data = gen_pop.initialize_poptracker_locations()
    pop_map_data = gen_pop.initialize_poptracker_maps()
    pop_layout_data = gen_pop_layout.initialize_poptracker_layout_data()

    json_data, pop_item_data, pop_map_data, pop_loc_data, pop_layout_data = process_state_csv(json_data, pop_item_data, pop_map_data, pop_loc_data, pop_layout_data)
    json_data, pop_item_data, pop_loc_data, region_dlc_index, pop_layout_data = process_region_csv(json_data, pop_item_data, pop_loc_data, pop_layout_data)
    json_data, garage_city_index, pop_item_data, pop_loc_data, pop_layout_data = process_location_csv(json_data, pop_item_data, pop_loc_data, region_dlc_index, pop_layout_data)
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

    for file in pop_layout_data:
        json.dump(pop_layout_data[file], open(f"./ats_harmonic_series-main/layouts/{file}.json","w"), indent=2)
    #TODO: Fix issues in archipelago.lua
    #TODO: Generate item_mapping.lua
    #TODO: Generate location_mapping.lua
    #TODO: Generate init.lua

    #TODO: Create better pngs for cities, viewpoints, photo trophies locked/unlocked

    #TODO: Generate layouts?
    # Settings page will have a grid for all the states
    # Also have item for number of stamps available, number required
