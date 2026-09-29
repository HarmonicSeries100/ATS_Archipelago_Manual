from typing import Optional, Any
from BaseClasses import MultiWorld, Item, Location
from .util import STATE_DICT

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    chosen_states = frozenset(multiworld.worlds[player].chosen_states)
    if category_name in STATE_DICT.keys(): # Check only state categories
        return category_name in chosen_states

    if category_name.startswith("DLC - "):
        from ..Helpers import get_option_value
        owned_DLC = set([f"DLC - {item}" for item in get_option_value(multiworld, player, "state_dlc")])
        return category_name in owned_DLC or category_name == "DLC - Base"
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item:  dict[str, Any]) -> Optional[bool]:
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location:  dict[str, Any]) -> Optional[bool]:
    victory_state = multiworld.worlds[player].victory_state
    location_categories = frozenset(location["category"])
    # If location is a state capital and not the victory state, then disable the location
    if "State Capital" in location_categories and victory_state not in location_categories:
        return False
    return None
    
# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the event, False to disable it, or None to use the default behavior
def before_is_event_enabled(multiworld: MultiWorld, player: int, event:  dict[str, Any]) -> Optional[bool]:
    return None
