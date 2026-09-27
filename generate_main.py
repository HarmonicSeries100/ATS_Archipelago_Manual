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

def generate_hook_util(state_metadata):
    file_content = "STATE_DICT = {\n"
    for key,value in state_metadata.items():
        file_content += f"  \"{key}\":\n"
        file_content += f"  {{\n"
        file_content += f"    \"items\": {value["items"]},\n"
        file_content += f"    \"locations\": {value["locations"]}\n"
        file_content += f"  }},\n"
    file_content += "}"
    with open("./manual_americantrucksimulator_harmonicseries/hooks/util.py","w") as file:
        file.write(file_content)

def process_state_csv(json_data,poptracker_data):
    lua_state_options = {}
    dlc_list = []
    state_list = []
    state_metadata = {}
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

                layout_row = poptracker_data["layout"]["options_layout"]["settings_popup"]["content"][1]["content"]["rows"]
                layout_row = gen_pop_layout.add_item_to_row(layout_row, const.DLC_OPTION_PREFIX+dlc_id, const.NUMBER_OF_OPTION_COLUMNS)
                poptracker_data["layout"]["options_layout"]["settings_popup"]["content"][1]["content"]["rows"]=layout_row
                poptracker_data["item"]["options"].append(gen_pop.get_poptracker_dlc_owned_item(dlc_id, dlc_name))
                dlc_list.append(dlc_id)

            if dlc_option not in json_data['options']['user'] and dlc_name != 'Base':
                json_data['options']['user'][dlc_option] = gen_man.get_own_dlc_option(dlc_name)

            state_code = state["state_id"]
            state_name = state["state_display_name"]
            state_pref_option = state_code + const.STATE_PREFERENCE_SUFFIX

            state_list.append((state_code,state_name))

            state_metadata[state_name] = {}
            state_metadata[state_name]["items"] = 0
            state_metadata[state_name]["locations"] = 0
            state_metadata[state_name]["DLC"] = dlc_name

            json_data['options']['user'][state_pref_option] = gen_man.get_state_preference_option(state_name)
            
            poptracker_data["item"]["options"].append(gen_pop.get_poptracker_state_option_item(state_code, state_name))

            poptracker_data["map"].append(gen_pop.get_poptracker_map(state_code))

            poptracker_data["location"][dlc_id] = [] if dlc_id != "base" else poptracker_data["location"][dlc_id]

            poptracker_data["layout"]["tracker"]["tracker_default"]["content"]["tabs"].append(gen_pop_layout.get_tracker_tab_layout_node(state_name, state_code))
            poptracker_data["layout"][state_code] = gen_pop_layout.get_state_layout(state_name, state_code)
            layout_row = poptracker_data["layout"]["options_layout"]["settings_popup"]["content"][2]["content"]["rows"]
            layout_row = gen_pop_layout.add_item_to_row(layout_row, state_code+const.POPTRACKER_STATE_CHOSEN_SUFFIX, const.NUMBER_OF_OPTION_COLUMNS)
            poptracker_data["layout"]["options_layout"]["settings_popup"]["content"][2]["content"]["rows"]=layout_row

            lua_state_options[state_code+const.POPTRACKER_STATE_CHOSEN_SUFFIX] = state_name

    gen_lua.generate_init_lua_script(dlc_list, state_list)
    return json_data, poptracker_data, lua_state_options, state_metadata


def process_region_csv(json_data, poptracker_data, state_metadata):
    region_dlc_index = {}
    with open('./resources/ats_manual_region_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for region in reader:
            json_data['regions'][region["Region_Name"]] = gen_man.get_region_object(region)
            json_data['items']['data'].append(gen_man.get_region_unlock_item_from_region(region))

            state_metadata[region["State"].split("; ")[0]]["items"] += 1 # Attribute multistate region key to first state in list to prevent duplicate counting in metadata

            poptracker_data["item"]['items'].append(gen_pop.get_poptracker_region_unlock_item(region))

            poptracker_data["location"], region_dlc_index = gen_pop.get_poptracker_region_location(region, poptracker_data["location"], region_dlc_index)

            for state in region["State"].split("; "):
                state_code = to_snake_case(state)
                poptracker_data["layout"][state_code][f"{state_code}_layout"]["content"][1]["content"][1]["content"]["content"].append(gen_pop_layout.get_region_layout_node(region))

    return json_data, poptracker_data, region_dlc_index, state_metadata


def process_location_csv(json_data, poptracker_data, region_dlc_index, state_metadata):
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

            # Attribute location to first state in list, to prevent duplicate counting in metadata
            # Only attribute if the location DLC matches the state's "home" DLC, to prevent issues with unbought DLC blocking locations
            first_location_state = location["State"].split("; ")[0]
            if location["State_DLC"] == state_metadata[first_location_state]["DLC"]:
                state_metadata[first_location_state]["locations"] += 1
                if location['Has_Garage'] == 'Y':
                    state_metadata[first_location_state]["items"] += 1

            poptracker_data["location"] = gen_pop.get_poptracker_location(location, poptracker_data["location"], region_dlc_index)

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

                poptracker_data["item"]["items"].append(gen_pop.get_poptracker_fast_travel_unlock_item(location))
                poptracker_data["item"]["items"].append(gen_pop.get_poptracker_starting_city_item(location))
                poptracker_data["layout"] = gen_pop_layout.add_ft_item_to_layout(location, poptracker_data["layout"])
                
            if location["Location_Group"]:
                location_map[location_name] = f"{to_snake_case(location["Region"])}/{location["Location_Group"]}/{location_name}"
            else:
                location_map[location_name] = f"{to_snake_case(location["Region"])}/{location_name}/"

            if location['State_Capital'] == 'Y':
                json_data['locations']['data'].append(gen_man.get_state_capital_location(location))

                location_map[const.STATE_CAPITAL_LOC_PREFIX+location_name] = f"{to_snake_case(location["Region"])}/{location["Location_Group"]}/{const.STATE_CAPITAL_LOC_PREFIX+location_name}"
    
    return json_data, poptracker_data, garage_cities, location_map, state_metadata


if __name__ == '__main__':
    json_data = gen_man.initialize_lists()
    poptracker_data = {}
    poptracker_data["item"] = gen_pop.initialize_poptracker_items()
    poptracker_data["location"] = gen_pop.initialize_poptracker_locations()
    poptracker_data["map"] = gen_pop.initialize_poptracker_maps()
    poptracker_data["layout"] = gen_pop_layout.initialize_poptracker_layout_data()

    json_data, poptracker_data, lua_state_options, state_metadata = process_state_csv(json_data, poptracker_data)
    json_data, poptracker_data, region_dlc_index, state_metadata = process_region_csv(json_data, poptracker_data, state_metadata)
    json_data, poptracker_data, garage_city_index, location_map, state_metadata = process_location_csv(json_data, poptracker_data, region_dlc_index, state_metadata)
    json_data = gen_man.generate_fast_travel_regions(json_data, garage_city_index)
    json_data = gen_man.generate_starting_items(json_data, garage_city_index)
    
    for file in json_data:
        json.dump(json_data[file], open("./manual_americantrucksimulator_harmonicseries/data/" + file + ".json", "w"),
                  indent=2)
    
    for file in poptracker_data["item"]:
        json.dump(poptracker_data["item"][file], open(f"./ats_harmonic_series-main/items/{file}.json","w"), indent=2)

    for file in poptracker_data["location"]:
        json.dump(poptracker_data["location"][file], open(f"./ats_harmonic_series-main/locations/{file}.json","w"), indent=2)

    json.dump(poptracker_data["map"], open(f"./ats_harmonic_series-main/maps/ats_maps.json","w"), indent=2)

    for file in poptracker_data["layout"]:
        json.dump(poptracker_data["layout"][file], open(f"./ats_harmonic_series-main/layouts/{file}.json","w"), indent=2)

    gen_lua.generate_item_mapping_script(json_data["items"]["data"], lua_state_options)
    gen_lua.generate_location_mapping_script(json_data["locations"]["data"], location_map)

    generate_hook_util(state_metadata)