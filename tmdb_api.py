"""
TMDB API utility module for fetching movie and TV series data.
"""
import requests
from flask import current_app

def get_api_url(endpoint, **kwargs):
    """
    Construct a TMDB API URL with the given endpoint and parameters.
    
    Args:
        endpoint (str): The API endpoint (e.g., '/movie/popular')
        **kwargs: Additional query parameters
    
    Returns:
        str: The complete API URL
    
    Raises:
        ValueError: If the API key is not set or is still the default placeholder
    """
    base_url = current_app.config['TMDB_API_URL']
    api_key = current_app.config['TMDB_API_KEY']
    
    # Check if API key is valid
    if not api_key or api_key == 'your-tmdb-api-key-here':
        raise ValueError(
            "Invalid TMDB API key. Please set a valid API key in appconfig.py. "
            "You can get an API key from https://www.themoviedb.org/settings/api"
        )
    
    # Start with the base parameters
    params = {'api_key': api_key, 'language': 'en-US'}
    
    # Add any additional parameters
    params.update(kwargs)
    
    # Convert parameters to query string
    query_string = '&'.join(["{}={}".format(key, value) for key, value in params.items()])
    
    return "{0}{1}?{2}".format(base_url, endpoint, query_string)

def get_image_url(path, size='w500'):
    """
    Construct a TMDB image URL with the given path and size.
    
    Args:
        path (str): The image path from TMDB API
        size (str): The image size (e.g., 'w500', 'original')
    
    Returns:
        str: The complete image URL or None if path is None
    """
    if not path:
        return None
        
    base_url = current_app.config['TMDB_IMAGE_BASE_URL']
    return "{0}{1}{2}".format(base_url, size, path)

def get_popular_movies(page=1):
    """
    Get popular movies from TMDB API.
    
    Args:
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing popular movies
    """
    try:
        # Try different parameter names for controlling items per page
        url = get_api_url('/movie/popular', page=page, limit=24)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for movie in data.get('results', []):
                if movie.get('poster_path'):
                    movie['poster_url'] = get_image_url(movie['poster_path'])
                if movie.get('backdrop_path'):
                    movie['backdrop_url'] = get_image_url(movie['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch popular movies. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_top_rated_movies(page=1):
    """
    Get top-rated movies from TMDB API.
    
    Args:
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing top-rated movies
    """
    try:
        # Try different parameter names for controlling items per page
        url = get_api_url('/movie/top_rated', page=page, limit=24)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for movie in data.get('results', []):
                if movie.get('poster_path'):
                    movie['poster_url'] = get_image_url(movie['poster_path'])
                if movie.get('backdrop_path'):
                    movie['backdrop_url'] = get_image_url(movie['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch top-rated movies. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_recently_released_movies(page=1):
    """
    Get recently released movies (now playing in theaters) from TMDB API.
    
    Args:
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing recently released movies
    """
    try:
        # Try different parameter names for controlling items per page
        url = get_api_url('/movie/now_playing', page=page, limit=24)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for movie in data.get('results', []):
                if movie.get('poster_path'):
                    movie['poster_url'] = get_image_url(movie['poster_path'])
                if movie.get('backdrop_path'):
                    movie['backdrop_url'] = get_image_url(movie['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch recently released movies. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_trending_movies(time_window='week', page=1):
    """
    Get trending movies from TMDB API.
    
    Args:
        time_window (str): Time window for trending calculation ('day' or 'week')
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing trending movies
    """
    try:
        # Try different parameter names for controlling items per page
        url = get_api_url('/trending/movie/{}'.format(time_window), page=page, limit=24)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for movie in data.get('results', []):
                if movie.get('poster_path'):
                    movie['poster_url'] = get_image_url(movie['poster_path'])
                if movie.get('backdrop_path'):
                    movie['backdrop_url'] = get_image_url(movie['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch trending movies. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_movie_external_ids(movie_id):
    """
    Get external IDs for a specific movie (IMDB, Facebook, Instagram, Twitter).
    
    Args:
        movie_id (int): The TMDB movie ID
    
    Returns:
        dict: The external IDs or None if not found
    """
    try:
        url = get_api_url('/movie/{}/external_ids'.format(movie_id))
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        elif response.status_code == 404:
            print("Error: Movie with ID {} not found. Status code: {}".format(movie_id, response.status_code))
        else:
            print("Error: Failed to fetch movie external IDs. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    return None

def get_embess_url(imdb_id):
    """
    Get the embess.ws embed URL for a movie using its IMDB ID.
    
    Args:
        imdb_id (str): The IMDB ID of the movie
    
    Returns:
        str: The embess.ws embed URL or None if IMDB ID is not available
    """
    if not imdb_id:
        return None
        
    base_url = current_app.config['EMBESS_BASE_URL']
    return "{0}{1}".format(base_url, imdb_id)

def get_movie_details(movie_id):
    """
    Get detailed information for a specific movie.
    
    Args:
        movie_id (int): The TMDB movie ID
    
    Returns:
        dict: The movie details or None if not found
    """
    try:
        url = get_api_url('/movie/{}'.format(movie_id), append_to_response='videos,credits,external_ids')
        response = requests.get(url)
        
        if response.status_code == 200:
            movie = response.json()
            
            # Add complete image URLs
            if movie.get('poster_path'):
                movie['poster_url'] = get_image_url(movie['poster_path'])
            if movie.get('backdrop_path'):
                movie['backdrop_url'] = get_image_url(movie['backdrop_path'], 'original')
                
            # Process cast members
            cast = movie.get('credits', {}).get('cast', [])
            for person in cast:
                if person.get('profile_path'):
                    person['profile_url'] = get_image_url(person['profile_path'], 'w185')
            
            return movie
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        elif response.status_code == 404:
            print("Error: Movie with ID {} not found. Status code: {}".format(movie_id, response.status_code))
        else:
            print("Error: Failed to fetch movie details. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    return None

def search_movies(query, page=1):
    """
    Search for movies by title.
    
    Args:
        query (str): The search query
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing search results
    """
    try:
        url = get_api_url('/search/movie', query=query, page=page)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for movie in data.get('results', []):
                if movie.get('poster_path'):
                    movie['poster_url'] = get_image_url(movie['poster_path'])
                if movie.get('backdrop_path'):
                    movie['backdrop_url'] = get_image_url(movie['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to search movies. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_movie_genres():
    """
    Get the list of movie genres from TMDB API.
    
    Returns:
        list: The list of genres or empty list if not found
    """
    try:
        url = get_api_url('/genre/movie/list')
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json().get('genres', [])
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch movie genres. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    return []

def get_movies_by_genre(genre_id, page=1):
    """
    Get movies by genre.
    
    Args:
        genre_id (int): The genre ID
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing movies in the specified genre
    """
    try:
        # Try different parameter names for controlling items per page
        url = get_api_url('/discover/movie', with_genres=genre_id, page=page, limit=24)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for movie in data.get('results', []):
                if movie.get('poster_path'):
                    movie['poster_url'] = get_image_url(movie['poster_path'])
                if movie.get('backdrop_path'):
                    movie['backdrop_url'] = get_image_url(movie['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch movies by genre. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_popular_tv_shows(page=1):
    """
    Get popular TV shows from TMDB API.
    
    Args:
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing popular TV shows
    """
    try:
        # Try different parameter names for controlling items per page
        url = get_api_url('/tv/popular', page=page, limit=24)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for show in data.get('results', []):
                if show.get('poster_path'):
                    show['poster_url'] = get_image_url(show['poster_path'])
                if show.get('backdrop_path'):
                    show['backdrop_url'] = get_image_url(show['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch popular TV shows. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_trending_tv_shows(time_window='week', page=1):
    """
    Get trending TV shows from TMDB API.
    
    Args:
        time_window (str): Time window for trending calculation ('day' or 'week')
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing trending TV shows
    """
    try:
        # Try different parameter names for controlling items per page
        url = get_api_url('/trending/tv/{}'.format(time_window), page=page, limit=24)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for show in data.get('results', []):
                if show.get('poster_path'):
                    show['poster_url'] = get_image_url(show['poster_path'])
                if show.get('backdrop_path'):
                    show['backdrop_url'] = get_image_url(show['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch trending TV shows. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_tv_external_ids(tv_id):
    """
    Get external IDs for a specific TV show (IMDB, Facebook, Instagram, Twitter).
    
    Args:
        tv_id (int): The TMDB TV show ID
    
    Returns:
        dict: The external IDs or None if not found
    """
    try:
        url = get_api_url('/tv/{}/external_ids'.format(tv_id))
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        elif response.status_code == 404:
            print("Error: TV show with ID {} not found. Status code: {}".format(tv_id, response.status_code))
        else:
            print("Error: Failed to fetch TV show external IDs. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    return None

def get_tv_show_details(tv_id):
    """
    Get detailed information for a specific TV show.
    
    Args:
        tv_id (int): The TMDB TV show ID
    
    Returns:
        dict: The TV show details or None if not found
    """
    try:
        url = get_api_url('/tv/{}'.format(tv_id), append_to_response='videos,credits,external_ids')
        response = requests.get(url)
        
        if response.status_code == 200:
            show = response.json()
            
            # Add complete image URLs
            if show.get('poster_path'):
                show['poster_url'] = get_image_url(show['poster_path'])
            if show.get('backdrop_path'):
                show['backdrop_url'] = get_image_url(show['backdrop_path'], 'original')
                
            # Process cast members
            cast = show.get('credits', {}).get('cast', [])
            for person in cast:
                if person.get('profile_path'):
                    person['profile_url'] = get_image_url(person['profile_path'], 'w185')
            
            return show
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        elif response.status_code == 404:
            print("Error: TV show with ID {} not found. Status code: {}".format(tv_id, response.status_code))
        else:
            print("Error: Failed to fetch TV show details. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    return None

def search_tv_shows(query, page=1):
    """
    Search for TV shows by title.
    
    Args:
        query (str): The search query
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing search results
    """
    try:
        url = get_api_url('/search/tv', query=query, page=page)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for show in data.get('results', []):
                if show.get('poster_path'):
                    show['poster_url'] = get_image_url(show['poster_path'])
                if show.get('backdrop_path'):
                    show['backdrop_url'] = get_image_url(show['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to search TV shows. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_tv_show_genres():
    """
    Get the list of TV show genres from TMDB API.
    
    Returns:
        list: The list of genres or empty list if not found
    """
    try:
        url = get_api_url('/genre/tv/list')
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json().get('genres', [])
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch TV show genres. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    return []

def get_tv_shows_by_genre(genre_id, page=1):
    """
    Get TV shows by genre.
    
    Args:
        genre_id (int): The genre ID
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing TV shows in the specified genre
    """
    try:
        # Try different parameter names for controlling items per page
        url = get_api_url('/discover/tv', with_genres=genre_id, page=page, limit=24)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for show in data.get('results', []):
                if show.get('poster_path'):
                    show['poster_url'] = get_image_url(show['poster_path'])
                if show.get('backdrop_path'):
                    show['backdrop_url'] = get_image_url(show['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch TV shows by genre. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_recently_released_tv_shows(page=1):
    """
    Get recently released TV shows (currently on the air) from TMDB API.
    
    Args:
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing recently released TV shows
    """
    try:
        # Try different parameter names for controlling items per page
        url = get_api_url('/tv/on_the_air', page=page, limit=24)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for show in data.get('results', []):
                if show.get('poster_path'):
                    show['poster_url'] = get_image_url(show['poster_path'])
                if show.get('backdrop_path'):
                    show['backdrop_url'] = get_image_url(show['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch recently released TV shows. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_top_rated_tv_shows(page=1):
    """
    Get top-rated TV shows from TMDB API.
    
    Args:
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing top-rated TV shows
    """
    try:
        # Try different parameter names for controlling items per page
        url = get_api_url('/tv/top_rated', page=page, limit=24)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for show in data.get('results', []):
                if show.get('poster_path'):
                    show['poster_url'] = get_image_url(show['poster_path'])
                if show.get('backdrop_path'):
                    show['backdrop_url'] = get_image_url(show['backdrop_path'], 'original')
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to fetch top-rated TV shows. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_vidsrc_url(movie_id, media_type='movie'):
    """
    Get the vidsrc.to embed URL for a movie or TV show.
    
    Args:
        movie_id (int): The TMDB movie or TV show ID
        media_type (str): The media type ('movie' or 'tv')
    
    Returns:
        str: The vidsrc.to embed URL
    """
    if media_type == 'tv':
        # For TV shows, use the correct base URL format
        # The base URL in config includes 'movie/' so we need to remove it for TV shows
        base_url = current_app.config['VIDSRC_BASE_URL'].replace('movie/', '')
        return "{0}tv/{1}".format(base_url, movie_id)
    else:
        # For movies, use the original format
        base_url = current_app.config['VIDSRC_BASE_URL']
        return "{0}{1}".format(base_url, movie_id)

def get_vidsrc_tv_url(tv_id):
    """
    Get the vidsrc.to embed URL for a TV show.
    
    Args:
        tv_id (int): The TMDB TV show ID
    
    Returns:
        str: The vidsrc.to embed URL
    """
    return get_vidsrc_url(tv_id, media_type='tv')

def get_related_movies(movie_id):
    """
    Get related movies for a specific movie.
    
    Args:
        movie_id (int): The TMDB movie ID
    
    Returns:
        list: A list of related movies or empty list if not found
    """
    try:
        url = get_api_url('/movie/{}/recommendations'.format(movie_id))
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for movie in data.get('results', [])[:10]:  # Limit to 10 items
                if movie.get('poster_path'):
                    movie['poster_url'] = get_image_url(movie['poster_path'])
                if movie.get('backdrop_path'):
                    movie['backdrop_url'] = get_image_url(movie['backdrop_path'], 'original')
            
            return data.get('results', [])[:10]  # Return only the first 10 items
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        elif response.status_code == 404:
            print("Error: Movie with ID {} not found. Status code: {}".format(movie_id, response.status_code))
        else:
            print("Error: Failed to fetch related movies. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    return []

def get_related_tv_shows(tv_id):
    """
    Get related TV shows for a specific TV show.
    
    Args:
        tv_id (int): The TMDB TV show ID
    
    Returns:
        list: A list of related TV shows or empty list if not found
    """
    try:
        url = get_api_url('/tv/{}/recommendations'.format(tv_id))
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for show in data.get('results', [])[:10]:  # Limit to 10 items
                if show.get('poster_path'):
                    show['poster_url'] = get_image_url(show['poster_path'])
                if show.get('backdrop_path'):
                    show['backdrop_url'] = get_image_url(show['backdrop_path'], 'original')
            
            return data.get('results', [])[:10]  # Return only the first 10 items
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        elif response.status_code == 404:
            print("Error: TV show with ID {} not found. Status code: {}".format(tv_id, response.status_code))
        else:
            print("Error: Failed to fetch related TV shows. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    return []

def search_actors(query, page=1):
    """
    Search for actors by name.
    
    Args:
        query (str): The search query
        page (int): The page number for pagination
    
    Returns:
        dict: The API response containing search results
    """
    try:
        url = get_api_url('/search/person', query=query, page=page)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process the results to add complete image URLs
            for person in data.get('results', []):
                if person.get('profile_path'):
                    person['profile_url'] = get_image_url(person['profile_path'], 'w185')
                # Add a default profile image if none exists
                else:
                    person['profile_url'] = None
                
                # Add known_for_titles for display purposes
                known_for_titles = []
                for item in person.get('known_for', []):
                    if item.get('media_type') == 'movie' and item.get('title'):
                        known_for_titles.append(item['title'])
                    elif item.get('media_type') == 'tv' and item.get('name'):
                        known_for_titles.append(item['name'])
                
                person['known_for_titles'] = known_for_titles
            
            return data
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        else:
            print("Error: Failed to search actors. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    # Return empty results on error
    return {'results': [], 'total_pages': 0, 'total_results': 0, 'page': page}

def get_actor_details(actor_id):
    """
    Get detailed information for a specific actor/person.
    
    Args:
        actor_id (int): The TMDB person ID
    
    Returns:
        dict: The actor details or None if not found
    """
    try:
        url = get_api_url('/person/{}'.format(actor_id), append_to_response='movie_credits,tv_credits,images')
        response = requests.get(url)
        
        if response.status_code == 200:
            actor = response.json()
            
            # Add complete image URLs
            if actor.get('profile_path'):
                actor['profile_url'] = get_image_url(actor['profile_path'], 'w500')
            
            # Process movie credits
            movie_credits = actor.get('movie_credits', {}).get('cast', [])
            for movie in movie_credits:
                if movie.get('poster_path'):
                    movie['poster_url'] = get_image_url(movie['poster_path'], 'w185')
            
            # Sort movie credits by popularity (descending)
            actor['movie_credits']['cast'] = sorted(
                movie_credits, 
                key=lambda x: x.get('popularity', 0), 
                reverse=True
            )
            
            # Process TV credits
            tv_credits = actor.get('tv_credits', {}).get('cast', [])
            for show in tv_credits:
                if show.get('poster_path'):
                    show['poster_url'] = get_image_url(show['poster_path'], 'w185')
            
            # Sort TV credits by popularity (descending)
            actor['tv_credits']['cast'] = sorted(
                tv_credits, 
                key=lambda x: x.get('popularity', 0), 
                reverse=True
            )
            
            return actor
        elif response.status_code == 401:
            # Unauthorized - likely an invalid API key
            print("Error: Unauthorized API request. Check your TMDB API key. Status code: {}".format(response.status_code))
        elif response.status_code == 404:
            print("Error: Actor with ID {} not found. Status code: {}".format(actor_id, response.status_code))
        else:
            print("Error: Failed to fetch actor details. Status code: {}".format(response.status_code))
    except ValueError as e:
        print("Error: {}".format(str(e)))
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to TMDB API. {}".format(str(e)))
    
    return None