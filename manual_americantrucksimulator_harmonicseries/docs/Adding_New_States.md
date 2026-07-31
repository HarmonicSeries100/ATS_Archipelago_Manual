Manual AP World

1) Add a new line to resources/ats_manual_state_data.csv
2) Add one or more lines to resources/ats_manual_region_data.csv for each region
3) Add lines to resources/ats_manual_location_data.csv for each location
4) Add the <state_name> to hooks/World.py in the available_states list in before_generate_early

Poptracker

1) Add a flag to ats_harmonic_series-main/images/flags. It should be named <state_code>.png
2) Add a map to ats_harmonic_series-main/images/maps. It should be named <state_code>_map.png

Run generate_main.py to generate the rest of the files