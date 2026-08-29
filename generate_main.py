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
import generate_lua_scripts as gen_lua
from util import to_snake_case

def generate_hook_util(state_list):
    file_content = "STATE_LIST = [\n"
    for state in state_list:
        file_content += f"\"{state[1]}\",\n"
    file_content += "]"
    with open("./manual_americantrucksimulator_harmonicseries/hooks/util.py","w") as file:
        file.write(file_content)

def process_state_csv(json_data,pop_item_data,pop_map_data,pop_location_data,pop_layout_data):
    lua_state_options = {}
    dlc_list = []
    state_list = []
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
                pop_item_data["options"].append(gen_pop.get_poptracker_dlc_owned_item(dlc_id, dlc_name))
                dlc_list.append(dlc_id)

            if dlc_option not in json_data['options']['user'] and dlc_name != 'Base':
                json_data['options']['user'][dlc_option] = gen_man.get_own_dlc_option(dlc_name)

            state_code = state["state_id"]
            state_name = state["state_display_name"]
            state_pref_option = state_code + const.STATE_PREFERENCE_SUFFIX

            state_list.append((state_code,state_name))

            json_data['options']['user'][state_pref_option] = gen_man.get_state_preference_option(state_name)
            
            pop_item_data["options"].append(gen_pop.get_poptracker_state_option_item(state_code, state_name))

            pop_map_data.append(gen_pop.get_poptracker_map(state_code))

            pop_location_data[dlc_id] = [] if dlc_id != "base" else pop_location_data[dlc_id]

            pop_layout_data["tracker"]["tracker_default"]["content"]["tabs"].append(gen_pop_layout.get_tracker_tab_layout_node(state_name, state_code))
            pop_layout_data[state_code] = gen_pop_layout.get_state_layout(state_name, state_code)
            layout_row = pop_layout_data["options_layout"]["settings_popup"]["content"][2]["content"]["rows"]
            layout_row = gen_pop_layout.add_item_to_row(layout_row, state_code+const.POPTRACKER_STATE_CHOSEN_SUFFIX, const.NUMBER_OF_OPTION_COLUMNS)
            pop_layout_data["options_layout"]["settings_popup"]["content"][2]["content"]["rows"]=layout_row

            lua_state_options[state_code+const.POPTRACKER_STATE_CHOSEN_SUFFIX] = state_name

    gen_lua.generate_init_lua_script(dlc_list, state_list)
    generate_hook_util(state_list)
    return json_data, pop_item_data, pop_map_data, pop_location_data, pop_layout_data, lua_state_options


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
    location_map = {
        "Victory": "Victory Island/"
    }
    with (open('./resources/ats_manual_location_data.csv', 'r') as f):
        reader = csv.DictReader(f)
        for location in reader:
            location_name = location["Location_Name"]
            # Handle locations and items
            json_data['locations']['data'].append(gen_man.get_location_object(location))

            pop_loc_data = gen_pop.get_poptracker_location(location, pop_loc_data, region_dlc_index)

            if location['Has_Garage'] == 'Y':
                json_data['items']['data'].append(gen_man.get_fast_travel_item_from_location(location))
                starting_item = gen_man.get_start_item_from_location(location)
                json_data['items']['data'].append(starting_item)
                json_data['regions'][location['Region']]["starting"] = True
                try:
                    json_data['regions'][location['Region']]["entrance_requires"]["Manual"] += f" OR |{starting_item["name"]}|"
                except KeyError:
                    json_data['regions'][location['Region']]["entrance_requires"]={}
                    json_data['regions'][location['Region']]["entrance_requires"]["Manual"] = f"|{starting_item["name"]}|"
                try:
                    garage_cities[location['Region']].append(location_name)
                except KeyError:
                    garage_cities[location['Region']] = [location_name]

                pop_item_data["items"].append(gen_pop.get_poptracker_fast_travel_unlock_item(location))
                pop_layout_data = gen_pop_layout.add_ft_item_to_layout(location, pop_layout_data)
                
            if location["Location_Group"]:
                location_map[location_name] = f"{to_snake_case(location["Region"])}/{location["Location_Group"]}/{location_name}"
            else:
                location_map[location_name] = f"{to_snake_case(location["Region"])}/{location_name}/"

            if location['State_Capital'] == 'Y':
                json_data['locations']['data'].append(gen_man.get_state_capital_location(location))

                location_map[const.STATE_CAPITAL_LOC_PREFIX+location_name] = f"{to_snake_case(location["Region"])}/{location["Location_Group"]}/{const.STATE_CAPITAL_LOC_PREFIX+location_name}"
    
    return json_data, garage_cities, pop_item_data, pop_loc_data, pop_layout_data, location_map


if __name__ == '__main__':
    json_data = gen_man.initialize_lists()
    pop_item_data = gen_pop.initialize_poptracker_items()
    pop_loc_data = gen_pop.initialize_poptracker_locations()
    pop_map_data = gen_pop.initialize_poptracker_maps()
    pop_layout_data = gen_pop_layout.initialize_poptracker_layout_data()

    json_data, pop_item_data, pop_map_data, pop_loc_data, pop_layout_data, lua_state_options = process_state_csv(json_data, pop_item_data, pop_map_data, pop_loc_data, pop_layout_data)
    json_data, pop_item_data, pop_loc_data, region_dlc_index, pop_layout_data = process_region_csv(json_data, pop_item_data, pop_loc_data, pop_layout_data)
    json_data, garage_city_index, pop_item_data, pop_loc_data, pop_layout_data, location_map = process_location_csv(json_data, pop_item_data, pop_loc_data, region_dlc_index, pop_layout_data)
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

    gen_lua.generate_item_mapping_script(json_data["items"]["data"], lua_state_options)
    gen_lua.generate_location_mapping_script(json_data["locations"]["data"], location_map)