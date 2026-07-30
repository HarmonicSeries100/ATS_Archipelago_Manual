import constants as const
from util import to_snake_case

def generate_item_mapping_script(item_data, state_options):
    starting_index = 1
    file_content = "ITEM_MAPPING = {\n"
    item_id = starting_index
    for item in item_data:
        if "progression" in item and item["progression"]:
            if ("count" in item and int(item["count"]) > 1) or \
            (item["name"] == "National Park Passport Stamp"):
                item_type = "consumable"
            else:
                item_type = "toggle"
            if item["name"].startswith(const.UNLOCK_FT_ITEM_PREFIX):
                item_name = to_snake_case(const.POPTRACKER_UNLOCK_FT_ITEM_PREFIX+item["name"][len(const.UNLOCK_FT_ITEM_PREFIX):])
            else:
                item_name = to_snake_case(item["name"])
            file_content += f"    [{item_id}] = {{{{\"{item_name}\", \"{item_type}\"}}}},\n"
        item_id += 1
    file_content += "}\n"

    file_content += "STATE_OPTIONS = {\n"
    for state,state_name in state_options.items():
        file_content += f"[\"{state}\"] = \"{state_name}\",\n"
    file_content += "}"
    
    with open('./ats_harmonic_series-main/scripts/autotracking/item_mapping.lua', 'w', encoding="utf_8") as file:
        file.write(file_content)

def generate_location_mapping_script(location_data, location_map):
    starting_index = 1
    file_content = "LOCATION_MAPPING = {\n"
    file_content_reverse_map = "LOCATION_TO_ID_MAP = {\n"
    item_id = starting_index
    for location in location_data:
        loc_address = location_map[location["name"]]
        file_content += f"    [{item_id}] = {{{{\"@{loc_address}\"}}}},\n"
        file_content_reverse_map += f"    [\"{loc_address}\"] = {item_id},\n"
        item_id += 1
    file_content += "}\n\n"
    file_content_reverse_map += "}"
    all_content = file_content + file_content_reverse_map
    with open('./ats_harmonic_series-main/scripts/autotracking/location_mapping.lua', 'w', encoding="utf_8") as file:
        file.write(all_content)