-- entry point for all lua code of the pack
-- more info on the lua API: https://github.com/black-sliver/PopTracker/blob/master/doc/PACKS.md#lua-interface
ENABLE_DEBUG_LOG = true
-- get current variant
local variant = Tracker.ActiveVariantUID
-- check variant info

print("-- Example Tracker --")
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

-- Locations
Tracker:AddLocations("locations/base.json")
Tracker:AddLocations("locations/colorado.json")
Tracker:AddLocations("locations/new_mexico.json")
Tracker:AddLocations("locations/utah.json")


-- Layout
Tracker:AddLayouts("layouts/items.json")
Tracker:AddLayouts("layouts/tracker.json")
Tracker:AddLayouts("layouts/broadcast.jsonc")
Tracker:AddLayouts("layouts/options_layout.json")
Tracker:AddLayouts("layouts/victory_island.json")
Tracker:AddLayouts("layouts/arizona.json")
Tracker:AddLayouts("layouts/colorado.json")
Tracker:AddLayouts("layouts/new_mexico.json")
Tracker:AddLayouts("layouts/utah.json")
Tracker:AddLayouts("layouts/nevada.json")

--AutoTracking for Poptracker
if PopVersion and PopVersion >= "0.18.0" then
   ScriptHost:LoadScript("scripts/autotracking.lua")
end
