import csv
import json

import requests
from bs4 import BeautifulSoup

TITLE = 'Upcoming Releases'
URL = 'https://www.imdb.com/calendar/?region=MX'

"""
1.- Get the HTML content
    - If the HTML file does not exist locally, create it.
    - If the HTML file exists locally, retrieve its content.
2.- Extract information
    - Name
    - Categories
    - Cast
3.- Generate a CSV file
"""

def get_imdb_content():
    """Get the content of the IMDB calendar page
    Returns:
        string -- The content of the IMDB calendar page
        None -- If the request was not successful
    """
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        return response.text
    
    return None
    

def create_imdb_file_local(content):
    """Create a local file from the web page markup."""
    try:
        with open('imdb.html', 'w') as file:
            file.write(content)
    except:
        pass

def get_imdb_file_local():
    """Read the content of a local file"""
    content = None
    
    try:
        with open('imdb.html', 'r') as file:
            content = file.read()
    except:
        pass
    
    return content

def get_local_imdb_content():
    """Get the IMDB page content, either locally or from the server."""
    content = get_imdb_file_local()
    
    if content:
        return content

    content = get_imdb_content()
    create_imdb_file_local(content)

    return content
    

def create_movie(tag):
    main_div = tag.find('div', {'class': 'ipc-metadata-list-summary-item__c' })
    
    name = main_div.div.a.text
    ul_categories = main_div.find('ul', {
        'class': 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__tl base'
    })

    ul_cast = main_div.find('ul', {
        'class': 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--no-wrap ipc-inline-list--inline ipc-metadata-list-summary-item__stl base'
    })

    categories = [category.span.text for category in ul_categories.find_all('li')]
    cast = [cast.span.text for cast in ul_cast.find_all('li')] if ul_cast else []
    
    return (name, categories, cast)

def create_csv_movies_file(movies):
    with open('movies.csv', 'w') as file:
        writer = csv.writer(file, delimiter="-")
        writer.writerow(['name', 'categories', 'cast'])

        for movie in movies:
            writer.writerow([
                movie[0],  # name
                ",".join(movie[1]),  # categories
                ",".join(movie[2]),  # cast
            ])

def create_json_movies_file(movies):
    movies_list = [
        {
            'name': movie[0],
            'categories': movie[1],
            'cast': movie[2]
        }
        for movie in movies
    ]

    with open('movies.json', 'w', encoding='UTF-8') as file:
        json.dump(movies_list, file, indent=4)

def main():
    content = get_local_imdb_content()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    li_tags = soup.find_all('li', {
        'data-testid': 'coming-soon-entry',
        'class': 'ipc-metadata-list-summary-item ipc-metadata-list-summary-item--click sc-8c2b7f1f-0 bpqYIE'
    })

    movies = []
    for tag in li_tags:
        movie = create_movie(tag)
        movies.append(movie)

    # create_csv_movies_file(movies)
    create_json_movies_file(movies)

if __name__ == '__main__':
    main()
