## Introduction
- This is QGuideGuide, a guide to the QGuide, which I made because I (like many of my friends, and as I imagine, you as well) was incredibly frustrated at how bad the my.harvard viewer for courses is, how slow it is, how often my.harvard is down, how hard QGuide is to navigate, etc. etc. I hope this helps you in your future course-selecting endeavors!

## Scraping
1. **API Request**: While fiddling around with the QGuide I realized the QGuide makes requests to an internal API endpoint (`https://qreports.fas.harvard.edu/search/api`), so I simply scraped all of the courses in a single call (Harvard checks SSO credentials before you login to the QGuide, but luckily they don't keep much protection around the internal API, so I could use the session cookies for one "real" session and just used that for the curl). No rate limiting or user agent rotation needed when they're not looking.

2. **Response Handling**: Each QGuide page "links" to this weird "bluera" site I'm sure you guys are familiar with, so I pulled out the URLs from the curl-outputted HTML and searched through each of them extracting the tables (`BeautifulSoup`, `requests`) with a custom function that pulled all the conveniently already-formatted table data and also the instructor name (into Pandas DataFrames). One rut was that unfortunately they changed the table formatting and naming for some reason for 2024 (they added new questions about "how safe are you bringing up your politics(?) or something like that) but I thought those were not really important so I just skipped them.

3. **Parallel Data Processing (Optimizations)**: To speed up the processing of the course entries I used `lru_cache` to not process any possible duplicate URLs, used multithreading (since it's I/O bound--network requests--I don't think it's my CPU slowing things down), with 16 worker threads in `ThreadPoolExecutor` which made the entire 11,961 site scrape take less than a second.

## Data Processing/Exploration(?)
1. **Potential Issues**: Here are some issues I considered I might run into / did run into:
- Instructors having the same name / names that aren't just two words
- Changed the table names to literals vs. just numbered table names, which fucked things up for data extraction
- Tons of missing data, i.e. courses where no one responded, or just n/a values in general
- course names are weird; sometimes two titles/two departments, sometimes instructors have a pseudonym or 3 word names (crazy regex expressions...)

## Website Creation
1. it's slow. slow to show all data and calculate it all... how to make this faster? --> answer: use 