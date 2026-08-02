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

def generate_init_lua_script(dlc_list, state_list):
    file_content = """
ENABLE_DEBUG_LOG = true
-- get current variant
local variant = Tracker.ActiveVariantUID
-- check variant info
print("-- American Truck Simulator Poptracker --")
print("Loaded variant: ", variant)
if ENABLE_DEBUG_LOG then
    print("Debug logging is enabled!")
end

-- Utility Script for helper functions etc.
ScriptHost:LoadScript("scripts/utils.lua")

-- Logic
ScriptHost:LoadScript("scripts/logic/logic.lua")

-- Items
Tracker:AddItems("items/items.json")
Tracker:AddItems("items/options.json")

-- Maps
Tracker:AddMaps("maps/ats_maps.json")

--AutoTracking for Poptracker
if PopVersion and PopVersion >= "0.18.0" then
ScriptHost:LoadScript("scripts/autotracking.lua")
end

-- Layout
Tracker:AddLayouts("layouts/items.json")
Tracker:AddLayouts("layouts/tracker.json")
Tracker:AddLayouts("layouts/broadcast.jsonc")
Tracker:AddLayouts("layouts/options_layout.json")
Tracker:AddLayouts("layouts/victory_island.json")
"""
    for state in state_list:
        file_content += f"Tracker:AddLayouts(\"layouts/{state[0]}.json\")\n"

    file_content += "\n-- Locations\n"

    for dlc in dlc_list:
        file_content += f"Tracker:AddLocations(\"locations/{dlc}.json\")\n"

    with open('./ats_harmonic_series-main/scripts/init.lua', 'w', encoding="utf_8") as file:
        file.write(file_content)