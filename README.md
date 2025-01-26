# IMDB Upcoming Releases Scraper 🎬

This project scrapes upcoming movie releases from the IMDB calendar page for Mexico and saves the extracted data in JSON and CSV formats.

## Project Overview

The script performs the following tasks:

1. **Fetch HTML Content:**  
   - Checks if the HTML file exists locally; if not, downloads it from IMDB.
   - Saves the webpage content locally for future use.

2. **Data Extraction:**  
   - Extracts movie names, categories, and cast details.

3. **Data Storage:**  
   - Exports the extracted data to `movies.json` and optionally to `movies.csv`.
