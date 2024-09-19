# Flicks Scraper

This script scrapes [www.flicks.com.au](https://drytickets.com.au/) and save to this [google sheets](https://docs.google.com/spreadsheets/d/1fMD-Ld9LOn8LctXuaFYywv3mY_LugjS1syd-bCizer0/edit?pli=1&gid=1789520897#gid=1789520897)

# Run time of script.
   - 23:58 UTC

## Technologies Used
- Python
- GOOGLE SHEETs

## Workflow of script
1. Go to https://drytickets.com.au
2. Scroll to section "Events by date"
3. Scrape all event urls and store in google sheet - Google sheet tab name "Today"
4. Compare all event urls in Google sheet tab name "Yesterday" and find new events
5. Loop through new event urls, open "URL" and scrape below data

## Fields
event_name = [Title]
event_description = [Title]
event_start_date = [Date]
event_start_time = [Time]
venue_latlong = blank
city = see formula below
weblink = page [URL]
org = [Organised by]
language = blank
venue = [Address]
