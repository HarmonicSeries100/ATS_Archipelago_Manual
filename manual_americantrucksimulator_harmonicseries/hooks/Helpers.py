from typing import Optional, Any
from BaseClasses import MultiWorld, Item, Location


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item:  dict[str, Any]) -> Optional[bool]:
    chosen_states = set(multiworld.worlds[player].chosen_states)
    categories_to_check = {"Region Unlock", "Fast Travel Unlock"}
    item_categories = set(item["category"])
    # If the item belongs to "state level" categories but are not part of the chosen states, then disable the item
    if item_categories & categories_to_check and not item_categories & chosen_states:
        return False
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location:  dict[str, Any]) -> Optional[bool]:
    chosen_states = set(multiworld.worlds[player].chosen_states)
    categories_to_check = {"City", "Viewpoint", "Photo Trophy Point"}
    location_categories = set(location["category"])
    # If the location belongs to "state level" categories but are not part of the chosen states, then disable the location
    if location_categories & categories_to_check and not location_categories & chosen_states:
        return False
    return None
