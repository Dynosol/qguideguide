Now available at [qguideguide.com](url) although I'm using free tiers for everything so you will most likely encounter an egregious cold start. Django for backend api, Vite + React for frontend, Redis for caching, and Neon for the postgresql.

Unique visitor count: ~447

## Introduction
- This is QGuideGuide, a guide to the QGuide, which I made because I (like many of my friends, and as I imagine, you as well) was incredibly frustrated at how bad the my.harvard viewer for courses is, how slow it is, how often my.harvard is down, how hard QGuide is to navigate, etc. etc. I hope this helps you in your future course-selecting endeavors!

## Scraping
1. **API Request**: While fiddling around with the QGuide I realized the QGuide makes requests to an internal API endpoint (`https://qreports.fas.harvard.edu/search/api`), so I simply scraped all of the courses in a single call (Harvard checks SSO credentials before you login to the QGuide, but luckily they don't keep much protection around the internal API, so I could use the session cookies for one "real" session and just used that for the curl). No rate limiting or user agent rotation needed when they're not looking.

2. **Response Handling**: Each QGuide page "links" to this weird "bluera" site I'm sure you guys are familiar with, so I pulled out the URLs from the curl-outputted HTML and searched through each of them extracting the tables (`BeautifulSoup`, `requests`) with a custom function that pulled all the conveniently already-formatted table data and also the instructor name (into Pandas DataFrames). One rut was that unfortunately they changed the table formatting and naming for some reason for 2024 (they added new questions about "how safe are you bringing up your politics(?) or something like that) but I thought those were not really important so I just skipped them.
