-- put logic functions here using the Lua API: https://github.com/black-sliver/PopTracker/blob/master/doc/PACKS.md#lua-interface
-- don't be afraid to use custom logic functions. it will make many things a lot easier to maintain, for example by adding logging.
-- to see how this function gets called, check: locations/locations.json
-- example:
function has_more_then_n_consumable(n)
    local count = Tracker:ProviderCountForCode('consumable')
    local val = (count > tonumber(n))
    if ENABLE_DEBUG_LOG then
        print(string.format("called has_more_then_n_consumable: count: %s, n: %s, val: %s", count, n, val))
    end
    if val then
        return 1 -- 1 => access is in logic
    end
    return 0 -- 0 => no access
end

function is_in_chosen_state(...)
    local states = {...}
    if ENABLE_DEBUG_LOG then
        print(string.format("called is_in_chosen_state"))
        print(dump_table(states))
    end
    for _, state in ipairs(states) do
        if ENABLE_DEBUG_LOG then
            print(state)
            print(Tracker:ProviderCountForCode(state .. "_chosen"))
        end
        if Tracker:ProviderCountForCode(state .. "_chosen")>0 then
            if ENABLE_DEBUG_LOG then
                print("Found chosen state: " .. state)
                return 1
            end
        end
    end
    return 0
end

function is_region_connected(unlock_prefix, ...)
    local regions = {...}
    if ENABLE_DEBUG_LOG then
        print(string.format("called is_region_connected"))
        print(unlock_prefix)
        print(dump_table(regions))
    end
    for _, region in ipairs(regions) do
        if Tracker:ProviderCountForCode("@" .. region)>0 then
            return 1
        end
    end
    if Tracker:ProviderCountForCode(unlock_prefix .. region) then
        return 1
    else
        return 0
    end
end