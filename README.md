## drytickets events scraper

Step 1: Go to https://drytickets.com.au
Step 2: Scroll to section "Events by date"
Step 3: Scrape all event urls and store in google sheet - Google sheet tab name "Today"
Step 4: Compare all event urls in Google sheet tab name "Yesterday" and find new events
Step 5: Loop through new event urls, open "URL" and scrape below data
Title
Venue name
Address
Date
Time
Banner url
Organised by
Step 6: Enter scraped data in google sheet tab "New_events"
Columns --> | event_name | event_description | event_start_date | event_start_time | venue_latlong | city | weblink | org | language | venue |
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

Formula for city
-----------------------------------------------------------------
address = location.get('address', {})
address_region = address.get('addressRegion', 'N/A')
if address_region == 'VIC':
city_name = 'Melbourne'
elif address_region == 'NSW':
city_name = 'Sydney'
elif address_region == 'QLD':
city_name = 'Brisbane'
elif address_region == 'SA':
city_name = 'Adelaide'
elif address_region == 'WA':
city_name = 'Perth'
else:
city_name = address.get('addressLocality', 'N/A')
event_data['city'] = city_name
