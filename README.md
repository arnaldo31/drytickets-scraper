# Drytickets Scraper

This script scrapes [https://drytickets.com.au/](https://drytickets.com.au/) and save to this [google sheets](https://docs.google.com/spreadsheets/d/1HjsWyf8EJARJi192xB8gJIlc5aCPM3xQrPGPHOFUqv8/edit?gid=1814938593#gid=1814938593)

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
6. Enter scraped data in google sheet tab "New_events"

## Fields

- event_name = [Title]
- event_description = [Title]
- event_start_date = [Date]
- event_start_time = [Time]
- venue_latlong = blank
- city = see formula below
- weblink = page [URL]
- org = [Organised by]
- language = blank
- venue = [Address]


