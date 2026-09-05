-- put logic functions here using the Lua API: https://github.com/black-sliver/PopTracker/blob/master/doc/PACKS.md#lua-interface
-- don't be afraid to use custom logic functions. it will make many things a lot easier to maintain, for example by adding logging.
-- to see how this function gets called, check: locations/locations.json
-- example:
function is_in_chosen_state(...)
    local states = {...}
    if ENABLE_DEBUG_LOG then
        print(string.format("called is_in_chosen_state"))
    end
    for _, state in ipairs(states) do
        if Tracker:ProviderCountForCode(state .. "_chosen")>0 then
            if ENABLE_DEBUG_LOG then
                print("Found chosen state: " .. state)
                return true
            end
        end
    end
    return false
end

function has_enough_stamps()
    if ENABLE_DEBUG_LOG then
        print("Called has_enough_stamps")
    end
    local current_stamp_count = Tracker:ProviderCountForCode("national_park_passport_stamp")
    local stamps_needed = Tracker:ProviderCountForCode("number_of_stamps_required")
    if ENABLE_DEBUG_LOG then
        print(string.format("Current stamps: %s Needed stamps: %s",current_stamp_count,stamps_needed))
    end
    if current_stamp_count >= stamps_needed then
        return true
    else
        return false
    end
end

function set_required_stamps()
    local total_stamps = Tracker:ProviderCountForCode("number_of_stamps_available")
    local percent_needed = Tracker:ProviderCountForCode("percent_stamps_required")
    local stamps_needed = math.floor(total_stamps*percent_needed/100)
    if ENABLE_DEBUG_LOG then
        print("Calculated number of stamps needed: " .. stamps_needed)
    end
    local stamps_item = Tracker:FindObjectForCode("number_of_stamps_required")
    stamps_item.AcquiredCount = stamps_needed
    local stamp_collect_item = Tracker:FindObjectForCode("national_park_passport_stamp")
    stamp_collect_item.MaxCount = total_stamps
end

function set_chosen_states(chosen_states, victory_state)
    for state_item_key, state_name in pairs(STATE_OPTIONS) do
        state_item_object = Tracker:FindObjectForCode(state_item_key)
        state_item_object.CurrentStage = 0
        for _, value in ipairs(chosen_states) do
            if value == state_name then
                state_item_object.CurrentStage = 1
                break
            end
        end
        if victory_state == state_name then
            state_item_object.CurrentStage = 2
        end
    end
end