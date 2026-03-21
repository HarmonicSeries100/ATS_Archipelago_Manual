# American Truck Simulator Archipelago Manual: Road Trip Edition

This is an Archipelago randomizer for American Truck Simulator that emphasizes the road tripping aspect of the game
rather than the hauling aspect. Rather than progressing via finishing jobs and leveling up, this randomizer is a simple,
sync-friendly collect-a-thon that has you driving all over the countryside to collect thingies to unlock more
countryside to collect more thingies.

A few design decisions went into this to make this sync-viable, while still allowing for long, leisurely
playthroughs:
* Configurable number of states, to reduce the amount of land to cover during syncs
* States are further divided into regions, so that playing only a couple of states won't have half your checks in
Sphere 1.
* Quick Travel is enabled to reduce the amount of back-and-forth driving
* No hauling jobs necessary, drive without cargo (or in a car when Road Trip comes out)

## Goal

The goal is to travel to cities, viewpoints, and photo trophy locations to collect stamps for your [National Park
Passport](https://americasnationalparks.org/passport-to-your-national-parks/) (no affiliation with the actual National Park Service). Once you collect the required amount of stamps,
proceed to the Passport Validation Center in the designated state capital to complete your run.

## Locations

* Cities
* Viewpoints
* Photo Trophy Locations

## Items

* National Park Passport Stamps
* Regional Unlock Key
  * To smooth out progression, every state is divided into several regions, with each region having its own unlock key
  * Maps are provided to visually distinguish the regions
  * UT is recommended to know what is in logic
* Quick Travel Unlock Key
  * These keys enable you to teleport to the given city using the Quick Travel feature available in-game
* Vehicle Unlocks
  * Windshield Wipers - Do not use your wipers until you have this item
  * Headlights - Do not use your headlights until you have this item. You may sleep through the night to avoid the
danger and eye-strain of driving at night without your headlights

## Quick Travel Rules
* Quick Travel teleporting is included in logic, so you may encounter a situation where the next region to check can
only be accessible by teleporting to it.
* To Quick Travel to a city, you must have the Quick Travel Unlock for that city _and_ the Regional Unlock for the region
that city is in.
* The game will not let you Quick Travel if your vehicle is damaged enough. If you need to use QT while damaged, use
the "Emergency Towing Service" to tow your truck to the nearest service station. Then teleport to your intended destination
after repairing.


## Other Notes

* This manual is meant to be played on a "complete" save file with all cities discovered and enough money to handle
fuel/repair costs.
* Driving like a maniac and making frequent use of teleporting is **HIGHLY RECOMMENDED FOR SYNCS** to keep the play time
reasonable.
* Some locations are in logic for one state but require the DLC of a different state. This is called out in the maps.
* The Four Corners Monument is in logic for Utah, Colorado, Arizona, and New Mexico and will appear if any of those states
are chosen.

## Still to Do

* Add all the states. Currently only the Four Corners states (UT, AZ, CO, NM) are implemented.
* Vehiclesanity? (different trucks as items)
* Integrate with the Road Trip DLC after it comes out
* Make a PopTracker pack to better visualize the regions/logic
* Better filler items and traps