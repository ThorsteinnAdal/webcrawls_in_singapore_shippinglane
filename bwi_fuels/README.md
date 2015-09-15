# The Bunker World Index

Bunker World Index is a wonderful website that reports daily high/low/average prices for bunker fuels on every work-day of the week. 
This scraper/bs4 package is written to collect this information for later processing/exploring.

## The method

- The bwi_page scraper collects the information and returns a dictionary object
- A second function bwi_unify takes two dictionary objects and returns a unified dictionary objects (removes duplicates)
- A function bwi_dict_to_csv picks a table from the db and creates a csv file

