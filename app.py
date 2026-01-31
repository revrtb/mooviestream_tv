import os
import re
import glob
from flask import Flask, render_template, request, redirect, url_for, jsonify, render_template_string, send_file
import appconfig
import tmdb_api
from lib.database import db

# Load environment variables from web.env file
from dotenv import load_dotenv
load_dotenv('env.web')

app = Flask(__name__)
app.config.from_object(appconfig.Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
# db.init_app(app)

# ZAP_DOMAIN = 'https://zap.buzz'
# ### ### ### ### ### ### ###

ZAPS = {}
# ZAPS_COUNT = 100000

@app.route('/<zap_code>')
def redirect_short_url(zap_code):
    try:
        return redirect(ZAPS[zap_code])
    except KeyError as e:
        from lib.link import Link
        item = Link.query.filter_by(short_code=zap_code).first()
        if item:
            if len(ZAPS) < ZAPS_COUNT:
                ZAPS[zap_code] = item.url
            return redirect(item.url)
        else:
            return redirect(url_for('.index'))
    return redirect(url_for('.index')) 

@app.route('/sub/<code>', methods=['GET', 'POST'])
def system(code):
    url= ''
    if code == 'da4da2w':
        url = 'https://xml.revrtb.net/redirect?feed=800738&auth=PEEB&pubid=217546'
    elif code == 'r67qr6r':
        url = 'https://xml.popmonetizer.net/redirect?feed=800775&auth=2l1V&pubid=217594'
    elif code == 'rwe5qe':
        url = 'https://xml.adxnexus.com/redirect?feed=800794&auth=OV4I&pubid=217593'
    elif code == 'dqwd7':
        url = 'https://xml.zeusadx.com/redirect?feed=800880&auth=ZQXK&pubid=217595'
    elif code == 'adad8ad':
        url = 'https://xml.acertb.com/redirect?feed=800865&auth=QY6P&pubid=217596'
    elif code == 'w8qe8':
        url = 'https://xml.poprtb.com/redirect?feed=800895&auth=U1lO&pubid=217598'
    elif code == 'da7adsu3':
        url = 'https://engine.spotscenered.info/link.engine?z=87558&guid=64ce86d5-613e-46af-b41b-6f9885140eab'
    return render_template('load.html', url=url)

@app.route('/load', methods=['POST'])
def load():
    url = request.form.get('url')
    return redirect(url)

@app.route('/firstpage_home')
def firstpage_home():
    try:
        delay = 60
        max = 20
        dur = 0
        default_url = "https://engine.spotscenered.info/link.engine?z=87558&guid=64ce86d5-613e-46af-b41b-6f9885140eab"
        url1 = "https://engine.spotscenered.info/link.engine?z=87558&guid=64ce86d5-613e-46af-b41b-6f9885140eab"
        url2 = "https://xml.revrtb.net/redirect?feed=800738&auth=PEEB&pubid=217546"
        url3 = "https://xml.popmonetizer.net/redirect?feed=800775&auth=2l1V&pubid=217594"
        url4 = "https://xml.adxnexus.com/redirect?feed=800794&auth=OV4I&pubid=217593"
        page_key = 'firstpage'
        
        return render_template('pop_templatex.js', PAR_PAGE_KEY=page_key, 
                                PAR_TRGURL1=url1, PAR_TRGURL2=url2, PAR_TRGURL3=url3, PAR_TRGURL4=url4, 
                                PAR_TRGURL5=url1, PAR_DELAY=delay, PAR_MAX=max, PAR_DUR=dur, PAR_DEFURL=default_url, 
                                PAR_MAX_PP=4)
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/watch_page')
def watch_page():
    try:
        delay = 60
        max = 20
        dur = 0
        default_url = "https://xml.zeusadx.com/redirect?feed=800880&auth=ZQXK&pubid=217595"
        url1 = "https://xml.zeusadx.com/redirect?feed=800880&auth=ZQXK&pubid=217595"
        url2 = "https://xml.acertb.com/redirect?feed=800865&auth=QY6P&pubid=217596"
        url3 = "https://xml.poprtb.com/redirect?feed=800895&auth=U1lO&pubid=217598"
        page_key = 'firstpage'
        
        return render_template('pop_templatex.js', PAR_PAGE_KEY=page_key, 
                                PAR_TRGURL1=url1, PAR_TRGURL2=url2, PAR_TRGURL3=url3, PAR_TRGURL4=url1, 
                                PAR_TRGURL5=url1, PAR_DELAY=delay, PAR_MAX=max, PAR_DUR=dur, PAR_DEFURL=default_url, 
                                PAR_MAX_PP=3)
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/api/genres')
def api_genres():
    """API endpoint to get all movie genres."""
    try:
        genres = tmdb_api.get_movie_genres()
        return jsonify(genres)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tv/genres')
def api_tv_genres():
    """API endpoint to get all TV show genres."""
    try:
        genres = tmdb_api.get_tv_show_genres()
        return jsonify(genres)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/adban')
def adban():
    try:
        
        return render_template(
            'banner.html'
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/')
def index():
    """Render the home page with popular and trending movies."""
    page = request.args.get('page', 1, type=int)
    
    try:
        popular_movies = tmdb_api.get_popular_movies(page)
        trending_movies = tmdb_api.get_trending_movies('week')
        trending_tv_shows = tmdb_api.get_trending_tv_shows('week')
        
        # Check if we got empty results due to an error
        if not popular_movies.get('results') and not trending_movies.get('results') and not trending_tv_shows.get('results'):
            error_message = (
                "Unable to fetch movies. Please make sure you have set a valid TMDB API key "
                "in appconfig.py. You can get an API key from https://www.themoviedb.org/settings/api"
            )
            return render_template('error.html', title='API Error', error_message=error_message)
        
        return render_template(
            'index.html', title='Home',
            popular_movies=popular_movies,
            trending_movies=trending_movies,
            trending_tv_shows=trending_tv_shows,
            current_page=page
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Render the movie detail page."""
    try:
        movie = tmdb_api.get_movie_details(movie_id)
        if not movie:
            return render_template('404.html', title='Movie Not Found'), 404
        
        # Get related movies
        related_movies = tmdb_api.get_related_movies(movie_id)
        
        return render_template(
            'movie_detail.html',
            title=movie['title'],
            movie=movie,
            related_movies=related_movies
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/watch/<int:movie_id>')
def watch_movie(movie_id):
    """Render the movie watch page with player options."""
    try:
        movie = tmdb_api.get_movie_details(movie_id)
        if not movie:
            return render_template('404.html', title='Movie Not Found'), 404
        
        # Get the vidsrc.to URL
        vidsrc_url = tmdb_api.get_vidsrc_url(movie_id)
        
        # Get the embess.ws URL using IMDB ID
        imdb_id = movie.get('external_ids', {}).get('imdb_id')
        embess_url = tmdb_api.get_embess_url(imdb_id) if imdb_id else None
        
        # Get related movies
        related_movies = tmdb_api.get_related_movies(movie_id)
        
        return render_template(
            'watch_movie.html',
            title="Watch {}".format(movie['title']),
            movie=movie,
            vidsrc_url=vidsrc_url,
            embess_url=embess_url,
            imdb_id=imdb_id,
            related_movies=related_movies
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/tv')
def tv_index():
    """Render the TV shows home page with popular and trending TV shows."""
    page = request.args.get('page', 1, type=int)
    
    try:
        popular_shows = tmdb_api.get_popular_tv_shows(page)
        trending_shows = tmdb_api.get_trending_tv_shows('week')
        
        # Check if we got empty results due to an error
        if not popular_shows.get('results') and not trending_shows.get('results'):
            error_message = (
                "Unable to fetch TV shows. Please make sure you have set a valid TMDB API key "
                "in appconfig.py. You can get an API key from https://www.themoviedb.org/settings/api"
            )
            return render_template('error.html', title='API Error', error_message=error_message)
        
        return render_template(
            'tv_index.html', title='TV Shows',
            popular_shows=popular_shows,
            trending_shows=trending_shows,
            current_page=page
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/tv/<int:tv_id>')
def tv_detail(tv_id):
    """Render the TV show detail page."""
    try:
        show = tmdb_api.get_tv_show_details(tv_id)
        if not show:
            return render_template('404.html', title='TV Show Not Found'), 404
        
        # Get related TV shows
        related_shows = tmdb_api.get_related_tv_shows(tv_id)
        
        return render_template(
            'tv_detail.html',
            title=show['name'],
            show=show,
            related_shows=related_shows
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/watch/tv/<int:tv_id>')
def watch_tv(tv_id):
    """Render the TV show watch page with player options."""
    try:
        show = tmdb_api.get_tv_show_details(tv_id)
        if not show:
            return render_template('404.html', title='TV Show Not Found'), 404
        
        # Get the vidsrc.to URL
        vidsrc_url = tmdb_api.get_vidsrc_tv_url(tv_id)
        
        # Get the embess.ws URL using IMDB ID
        imdb_id = show.get('external_ids', {}).get('imdb_id')
        embess_url = tmdb_api.get_embess_url(imdb_id) if imdb_id else None
        
        # Get related TV shows
        related_shows = tmdb_api.get_related_tv_shows(tv_id)
        
        return render_template(
            'watch_tv.html',
            title="Watch {}".format(show['name']),
            show=show,
            vidsrc_url=vidsrc_url,
            embess_url=embess_url,
            imdb_id=imdb_id,
            related_shows=related_shows
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/search')
def search():
    """Search for movies, TV shows, and actors and render results."""
    try:
        query = request.args.get('query', '')
        page = request.args.get('page', 1, type=int)
        media_type = request.args.get('media_type', 'all')  # Default to 'all'
        is_ajax = request.args.get('ajax', '0') == '1'
        
        if not query:
            return redirect(url_for('index'))
        
        # Search based on media type
        if media_type == 'movie':
            results = tmdb_api.search_movies(query, page)
        elif media_type == 'tv':
            results = tmdb_api.search_tv_shows(query, page)
        elif media_type == 'person':
            results = tmdb_api.search_actors(query, page)
        else:
            # Search all types and combine results
            movie_results = tmdb_api.search_movies(query, page)
            tv_results = tmdb_api.search_tv_shows(query, page)
            actor_results = tmdb_api.search_actors(query, page)
            
            # Combine results (first page only for now)
            combined_results = {
                'results': [],
                'total_results': (
                    movie_results.get('total_results', 0) + 
                    tv_results.get('total_results', 0) + 
                    actor_results.get('total_results', 0)
                ),
                'total_pages': max(
                    movie_results.get('total_pages', 0),
                    tv_results.get('total_pages', 0),
                    actor_results.get('total_pages', 0)
                ),
                'page': page
            }
            
            # Add media_type to each result
            for movie in movie_results.get('results', []):
                movie['media_type'] = 'movie'
                combined_results['results'].append(movie)
            
            for show in tv_results.get('results', []):
                show['media_type'] = 'tv'
                combined_results['results'].append(show)
            
            for actor in actor_results.get('results', []):
                actor['media_type'] = 'person'
                combined_results['results'].append(actor)
            
            # Sort by popularity (descending)
            combined_results['results'] = sorted(
                combined_results['results'],
                key=lambda x: x.get('popularity', 0),
                reverse=True
            )
            
            results = combined_results
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            movie_cards_html = render_template(
                'search_results.html',
                results=results,
                current_page=page,
                media_type=media_type,
                query=query,
                ajax=True
            )
            return jsonify({
                'html': movie_cards_html,
                'has_more': page < results.get('total_pages', 1),
                'next_page': page + 1 if page < results.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'search_results.html',
            title='Search Results',
            query=query,
            results=results,
            current_page=page,
            media_type=media_type,
            has_more=page < results.get('total_pages', 1),
            next_page=page + 1 if page < results.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/recent')
def recent_movies():
    """Render all recently released movies with infinite scrolling."""
    page = request.args.get('page', 1, type=int)
    is_ajax = request.args.get('ajax', '0') == '1'
    
    try:
        # Get the first 20 items from the current page
        recent_movies = tmdb_api.get_recently_released_movies(page)
        
        if not recent_movies.get('results'):
            error_message = (
                "Unable to fetch recently released movies. Please make sure you have set a valid TMDB API key "
                "in appconfig.py. You can get an API key from https://www.themoviedb.org/settings/api"
            )
            return render_template('error.html', title='API Error', error_message=error_message)
        
        # Get 4 more items from the next page
        if len(recent_movies.get('results', [])) >= 20 and page < recent_movies.get('total_pages', 1):
            next_page_movies = tmdb_api.get_recently_released_movies(page + 1)
            # Add the first 4 items from the next page
            if next_page_movies.get('results'):
                # Create a set of existing movie IDs to avoid duplicates
                existing_ids = {movie['id'] for movie in recent_movies.get('results', [])}
                
                # Add only non-duplicate movies from the next page
                for movie in next_page_movies['results'][:4]:
                    if movie['id'] not in existing_ids:
                        recent_movies['results'].append(movie)
                        existing_ids.add(movie['id'])
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            movie_cards_html = render_template(
                'search_results.html',
                results=recent_movies,
                current_page=page,
                media_type='movie',
                is_recent=True,
                ajax=True
            )
            return jsonify({
                'html': movie_cards_html,
                'has_more': page < recent_movies.get('total_pages', 1),
                'next_page': page + 1 if page < recent_movies.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'search_results.html',
            title='Recently Released Movies',
            results=recent_movies,
            current_page=page,
            media_type='movie',
            is_recent=True,
            page_type='recent',
            has_more=page < recent_movies.get('total_pages', 1),
            next_page=page + 1 if page < recent_movies.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/popular')
def popular_movies():
    """Render all popular movies with infinite scrolling."""
    page = request.args.get('page', 1, type=int)
    is_ajax = request.args.get('ajax', '0') == '1'
    
    try:
        # Get the first 20 items from the current page
        popular_movies = tmdb_api.get_popular_movies(page)
        
        if not popular_movies.get('results'):
            error_message = (
                "Unable to fetch popular movies. Please make sure you have set a valid TMDB API key "
                "in appconfig.py. You can get an API key from https://www.themoviedb.org/settings/api"
            )
            return render_template('error.html', title='API Error', error_message=error_message)
        
        # Get 4 more items from the next page
        if len(popular_movies.get('results', [])) >= 20 and page < popular_movies.get('total_pages', 1):
            next_page_movies = tmdb_api.get_popular_movies(page + 1)
            # Add the first 4 items from the next page
            if next_page_movies.get('results'):
                # Create a set of existing movie IDs to avoid duplicates
                existing_ids = {movie['id'] for movie in popular_movies.get('results', [])}
                
                # Add only non-duplicate movies from the next page
                for movie in next_page_movies['results'][:4]:
                    if movie['id'] not in existing_ids:
                        popular_movies['results'].append(movie)
                        existing_ids.add(movie['id'])
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            movie_cards_html = render_template(
                'search_results.html',
                results=popular_movies,
                current_page=page,
                media_type='movie',
                is_popular=True,
                ajax=True
            )
            return jsonify({
                'html': movie_cards_html,
                'has_more': page < popular_movies.get('total_pages', 1),
                'next_page': page + 1 if page < popular_movies.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'search_results.html',
            title='Popular Movies',
            results=popular_movies,
            current_page=page,
            media_type='movie',
            is_popular=True,
            has_more=page < popular_movies.get('total_pages', 1),
            next_page=page + 1 if page < popular_movies.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/trending')
def trending_movies():
    """Render all trending movies with infinite scrolling."""
    page = request.args.get('page', 1, type=int)
    time_window = request.args.get('time_window', 'week')
    is_ajax = request.args.get('ajax', '0') == '1'
    
    try:
        # Get the first 20 items from the current page
        trending_movies = tmdb_api.get_trending_movies(time_window, page)
        
        if not trending_movies.get('results'):
            error_message = (
                "Unable to fetch trending movies. Please make sure you have set a valid TMDB API key "
                "in appconfig.py. You can get an API key from https://www.themoviedb.org/settings/api"
            )
            return render_template('error.html', title='API Error', error_message=error_message)
        
        # Get 4 more items from the next page
        if len(trending_movies.get('results', [])) >= 20 and page < trending_movies.get('total_pages', 1):
            next_page_movies = tmdb_api.get_trending_movies(time_window, page + 1)
            # Add the first 4 items from the next page
            if next_page_movies.get('results'):
                # Create a set of existing movie IDs to avoid duplicates
                existing_ids = {movie['id'] for movie in trending_movies.get('results', [])}
                
                # Add only non-duplicate movies from the next page
                for movie in next_page_movies['results'][:4]:
                    if movie['id'] not in existing_ids:
                        trending_movies['results'].append(movie)
                        existing_ids.add(movie['id'])
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            movie_cards_html = render_template(
                'search_results.html',
                results=trending_movies,
                current_page=page,
                media_type='movie',
                is_trending=True,
                time_window=time_window,
                ajax=True
            )
            return jsonify({
                'html': movie_cards_html,
                'has_more': page < trending_movies.get('total_pages', 1),
                'next_page': page + 1 if page < trending_movies.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'search_results.html',
            title='Trending Movies',
            results=trending_movies,
            current_page=page,
            media_type='movie',
            is_trending=True,
            time_window=time_window,
            has_more=page < trending_movies.get('total_pages', 1),
            next_page=page + 1 if page < trending_movies.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/top_rated')
def top_rated_movies():
    """Render all top-rated movies with infinite scrolling."""
    page = request.args.get('page', 1, type=int)
    is_ajax = request.args.get('ajax', '0') == '1'
    
    try:
        # Get the first 20 items from the current page
        top_rated_movies = tmdb_api.get_top_rated_movies(page)
        
        if not top_rated_movies.get('results'):
            error_message = (
                "Unable to fetch top-rated movies. Please make sure you have set a valid TMDB API key "
                "in appconfig.py. You can get an API key from https://www.themoviedb.org/settings/api"
            )
            return render_template('error.html', title='API Error', error_message=error_message)
        
        # Get 4 more items from the next page
        if len(top_rated_movies.get('results', [])) >= 20 and page < top_rated_movies.get('total_pages', 1):
            next_page_movies = tmdb_api.get_top_rated_movies(page + 1)
            # Add the first 4 items from the next page
            if next_page_movies.get('results'):
                # Create a set of existing movie IDs to avoid duplicates
                existing_ids = {movie['id'] for movie in top_rated_movies.get('results', [])}
                
                # Add only non-duplicate movies from the next page
                for movie in next_page_movies['results'][:4]:
                    if movie['id'] not in existing_ids:
                        top_rated_movies['results'].append(movie)
                        existing_ids.add(movie['id'])
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            movie_cards_html = render_template(
                'search_results.html',
                results=top_rated_movies,
                current_page=page,
                media_type='movie',
                is_top_rated=True,
                ajax=True
            )
            return jsonify({
                'html': movie_cards_html,
                'has_more': page < top_rated_movies.get('total_pages', 1),
                'next_page': page + 1 if page < top_rated_movies.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'search_results.html',
            title='Top Rated Movies',
            results=top_rated_movies,
            current_page=page,
            media_type='movie',
            is_top_rated=True,
            has_more=page < top_rated_movies.get('total_pages', 1),
            next_page=page + 1 if page < top_rated_movies.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/tv/recent')
def recent_tv_shows():
    """Render all recently released TV shows with infinite scrolling."""
    page = request.args.get('page', 1, type=int)
    is_ajax = request.args.get('ajax', '0') == '1'
    
    try:
        # Get the first 20 items from the current page
        recent_shows = tmdb_api.get_recently_released_tv_shows(page)
        
        if not recent_shows.get('results'):
            error_message = (
                "Unable to fetch recently released TV shows. Please make sure you have set a valid TMDB API key "
                "in appconfig.py. You can get an API key from https://www.themoviedb.org/settings/api"
            )
            return render_template('error.html', title='API Error', error_message=error_message)
        
        # Get 4 more items from the next page
        if len(recent_shows.get('results', [])) >= 20 and page < recent_shows.get('total_pages', 1):
            next_page_shows = tmdb_api.get_recently_released_tv_shows(page + 1)
            # Add the first 4 items from the next page
            if next_page_shows.get('results'):
                # Create a set of existing show IDs to avoid duplicates
                existing_ids = {show['id'] for show in recent_shows.get('results', [])}
                
                # Add only non-duplicate shows from the next page
                for show in next_page_shows['results'][:4]:
                    if show['id'] not in existing_ids:
                        recent_shows['results'].append(show)
                        existing_ids.add(show['id'])
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            movie_cards_html = render_template(
                'search_results.html',
                results=recent_shows,
                current_page=page,
                media_type='tv',
                is_recent=True,
                ajax=True
            )
            return jsonify({
                'html': movie_cards_html,
                'has_more': page < recent_shows.get('total_pages', 1),
                'next_page': page + 1 if page < recent_shows.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'search_results.html',
            title='Recently Released TV Shows',
            results=recent_shows,
            current_page=page,
            media_type='tv',
            is_recent=True,
            page_type='recent',
            has_more=page < recent_shows.get('total_pages', 1),
            next_page=page + 1 if page < recent_shows.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/tv/popular')
def popular_tv_shows():
    """Render all popular TV shows with infinite scrolling."""
    page = request.args.get('page', 1, type=int)
    is_ajax = request.args.get('ajax', '0') == '1'
    
    try:
        # Get the first 20 items from the current page
        popular_shows = tmdb_api.get_popular_tv_shows(page)
        
        if not popular_shows.get('results'):
            error_message = (
                "Unable to fetch popular TV shows. Please make sure you have set a valid TMDB API key "
                "in appconfig.py. You can get an API key from https://www.themoviedb.org/settings/api"
            )
            return render_template('error.html', title='API Error', error_message=error_message)
        
        # Get 4 more items from the next page
        if len(popular_shows.get('results', [])) >= 20 and page < popular_shows.get('total_pages', 1):
            next_page_shows = tmdb_api.get_popular_tv_shows(page + 1)
            # Add the first 4 items from the next page
            if next_page_shows.get('results'):
                # Create a set of existing show IDs to avoid duplicates
                existing_ids = {show['id'] for show in popular_shows.get('results', [])}
                
                # Add only non-duplicate shows from the next page
                for show in next_page_shows['results'][:4]:
                    if show['id'] not in existing_ids:
                        popular_shows['results'].append(show)
                        existing_ids.add(show['id'])
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            movie_cards_html = render_template(
                'search_results.html',
                results=popular_shows,
                current_page=page,
                media_type='tv',
                is_popular=True,
                ajax=True
            )
            return jsonify({
                'html': movie_cards_html,
                'has_more': page < popular_shows.get('total_pages', 1),
                'next_page': page + 1 if page < popular_shows.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'search_results.html',
            title='Popular TV Shows',
            results=popular_shows,
            current_page=page,
            media_type='tv',
            is_popular=True,
            has_more=page < popular_shows.get('total_pages', 1),
            next_page=page + 1 if page < popular_shows.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/tv/trending')
def trending_tv_shows():
    """Render all trending TV shows with infinite scrolling."""
    page = request.args.get('page', 1, type=int)
    time_window = request.args.get('time_window', 'week')
    is_ajax = request.args.get('ajax', '0') == '1'
    
    try:
        # Get the first 20 items from the current page
        trending_shows = tmdb_api.get_trending_tv_shows(time_window, page)
        
        if not trending_shows.get('results'):
            error_message = (
                "Unable to fetch trending TV shows. Please make sure you have set a valid TMDB API key "
                "in appconfig.py. You can get an API key from https://www.themoviedb.org/settings/api"
            )
            return render_template('error.html', title='API Error', error_message=error_message)
        
        # Get 4 more items from the next page
        if len(trending_shows.get('results', [])) >= 20 and page < trending_shows.get('total_pages', 1):
            next_page_shows = tmdb_api.get_trending_tv_shows(time_window, page + 1)
            # Add the first 4 items from the next page
            if next_page_shows.get('results'):
                # Create a set of existing show IDs to avoid duplicates
                existing_ids = {show['id'] for show in trending_shows.get('results', [])}
                
                # Add only non-duplicate shows from the next page
                for show in next_page_shows['results'][:4]:
                    if show['id'] not in existing_ids:
                        trending_shows['results'].append(show)
                        existing_ids.add(show['id'])
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            movie_cards_html = render_template(
                'search_results.html',
                results=trending_shows,
                current_page=page,
                media_type='tv',
                is_trending=True,
                time_window=time_window,
                ajax=True
            )
            return jsonify({
                'html': movie_cards_html,
                'has_more': page < trending_shows.get('total_pages', 1),
                'next_page': page + 1 if page < trending_shows.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'search_results.html',
            title='Trending TV Shows',
            results=trending_shows,
            current_page=page,
            media_type='tv',
            is_trending=True,
            time_window=time_window,
            has_more=page < trending_shows.get('total_pages', 1),
            next_page=page + 1 if page < trending_shows.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/tv/top_rated')
def top_rated_tv_shows():
    """Render all top-rated TV shows with infinite scrolling."""
    page = request.args.get('page', 1, type=int)
    is_ajax = request.args.get('ajax', '0') == '1'
    
    try:
        # Get the first 20 items from the current page
        top_rated_shows = tmdb_api.get_top_rated_tv_shows(page)
        
        if not top_rated_shows.get('results'):
            error_message = (
                "Unable to fetch top-rated TV shows. Please make sure you have set a valid TMDB API key "
                "in appconfig.py. You can get an API key from https://www.themoviedb.org/settings/api"
            )
            return render_template('error.html', title='API Error', error_message=error_message)
        
        # Get 4 more items from the next page
        if len(top_rated_shows.get('results', [])) >= 20 and page < top_rated_shows.get('total_pages', 1):
            next_page_shows = tmdb_api.get_top_rated_tv_shows(page + 1)
            # Add the first 4 items from the next page
            if next_page_shows.get('results'):
                # Create a set of existing show IDs to avoid duplicates
                existing_ids = {show['id'] for show in top_rated_shows.get('results', [])}
                
                # Add only non-duplicate shows from the next page
                for show in next_page_shows['results'][:4]:
                    if show['id'] not in existing_ids:
                        top_rated_shows['results'].append(show)
                        existing_ids.add(show['id'])
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            movie_cards_html = render_template(
                'search_results.html',
                results=top_rated_shows,
                current_page=page,
                media_type='tv',
                is_top_rated=True,
                ajax=True
            )
            return jsonify({
                'html': movie_cards_html,
                'has_more': page < top_rated_shows.get('total_pages', 1),
                'next_page': page + 1 if page < top_rated_shows.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'search_results.html',
            title='Top Rated TV Shows',
            results=top_rated_shows,
            current_page=page,
            media_type='tv',
            is_top_rated=True,
            has_more=page < top_rated_shows.get('total_pages', 1),
            next_page=page + 1 if page < top_rated_shows.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/search/tv')
def search_tv():
    """Search for TV shows and render results."""
    try:
        query = request.args.get('query', '')
        page = request.args.get('page', 1, type=int)
        is_ajax = request.args.get('ajax', '0') == '1'
        
        if not query:
            return redirect(url_for('tv_index'))
        
        results = tmdb_api.search_tv_shows(query, page)
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            movie_cards_html = render_template(
                'search_results.html',
                results=results,
                current_page=page,
                media_type='tv',
                query=query,
                ajax=True
            )
            return jsonify({
                'html': movie_cards_html,
                'has_more': page < results.get('total_pages', 1),
                'next_page': page + 1 if page < results.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'search_results.html',
            title='TV Show Search Results',
            query=query,
            results=results,
            current_page=page,
            media_type='tv',
            has_more=page < results.get('total_pages', 1),
            next_page=page + 1 if page < results.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/genre/<int:genre_id>')
def genre(genre_id):
    """Render movies by genre with infinite scrolling."""
    try:
        page = request.args.get('page', 1, type=int)
        is_ajax = request.args.get('ajax', '0') == '1'
        
        movies = tmdb_api.get_movies_by_genre(genre_id, page)
        
        # Get all genres to find the current genre name
        genres = tmdb_api.get_movie_genres()
        genre_name = next((g['name'] for g in genres if g['id'] == genre_id), 'Unknown Genre')
        
        # If it's an AJAX request, return only the movie cards HTML
        if is_ajax:
            return jsonify({
                'results': movies.get('results', []),
                'has_more': page < movies.get('total_pages', 1),
                'next_page': page + 1 if page < movies.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'genre.html',
            title='{} Movies'.format(genre_name),
            genre_name=genre_name,
            genre_id=genre_id,
            movies=movies,
            current_page=page,
            media_type='movie',
            has_more=page < movies.get('total_pages', 1),
            next_page=page + 1 if page < movies.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/tv/genre/<int:genre_id>')
def tv_genre(genre_id):
    """Render TV shows by genre with infinite scrolling."""
    try:
        page = request.args.get('page', 1, type=int)
        is_ajax = request.args.get('ajax', '0') == '1'
        
        shows = tmdb_api.get_tv_shows_by_genre(genre_id, page)
        
        # Get all genres to find the current genre name
        genres = tmdb_api.get_tv_show_genres()
        genre_name = next((g['name'] for g in genres if g['id'] == genre_id), 'Unknown Genre')
        
        # If it's an AJAX request, return only the TV show cards HTML
        if is_ajax:
            return jsonify({
                'results': shows.get('results', []),
                'has_more': page < shows.get('total_pages', 1),
                'next_page': page + 1 if page < shows.get('total_pages', 1) else None
            })
        
        # Regular request - return the full page
        return render_template(
            'genre.html',
            title='{} TV Shows'.format(genre_name),
            genre_name=genre_name,
            genre_id=genre_id,
            movies=shows,  # Reuse the same template variable for consistency
            current_page=page,
            media_type='tv',
            has_more=page < shows.get('total_pages', 1),
            next_page=page + 1 if page < shows.get('total_pages', 1) else None
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', title='About')

@app.route('/contact')
def contact():
    """Render the contact page."""
    return render_template('contact.html', title='Contact')

@app.route('/privacy')
def privacy_policy():
    """Render the privacy policy page."""
    return render_template('privacy_policy.html', title='Privacy Policy')

@app.route('/terms')
def terms_of_service():
    """Render the terms of service page."""
    return render_template('terms_of_service.html', title='Terms of Service')

@app.route('/sitemap')
def html_sitemap():
    """Render the HTML sitemap page."""
    return render_template('sitemap.html', title='Sitemap')

def get_latest_apk():
    """Find the latest APK version based on naming pattern Mooviestream-X.X.X.apk"""
    apps_dir = os.path.join(app.static_folder, 'apps')
    if not os.path.exists(apps_dir):
        return None, None
    
    # Pattern to match Mooviestream-X.X.X.apk
    pattern = os.path.join(apps_dir, 'Mooviestream-*.apk')
    apk_files = glob.glob(pattern)
    
    if not apk_files:
        return None, None
    
    # Extract version numbers and find the latest
    def extract_version(filename):
        match = re.search(r'Mooviestream-(\d+)\.(\d+)\.(\d+)\.apk', os.path.basename(filename))
        if match:
            return tuple(map(int, match.groups()))
        return (0, 0, 0)
    
    # Sort by version number (latest first)
    apk_files.sort(key=extract_version, reverse=True)
    latest_apk = apk_files[0]
    
    # Extract version string
    version_match = re.search(r'Mooviestream-(\d+\.\d+\.\d+)\.apk', os.path.basename(latest_apk))
    version = version_match.group(1) if version_match else "Unknown"
    
    return latest_apk, version

@app.route('/mobile-app')
def mobile_app():
    """Render the mobile app download page."""
    latest_apk, version = get_latest_apk()
    return render_template('mobile_app.html', title='Mobile App', apk_version=version)

@app.route('/download/android')
def download_android():
    """Serve the latest Android APK file for download."""
    latest_apk, version = get_latest_apk()
    
    if not latest_apk or not os.path.exists(latest_apk):
        return render_template('404.html', title='File Not Found'), 404
    
    # Get file size
    file_size = os.path.getsize(latest_apk)
    size_mb = round(file_size / (1024 * 1024), 1)
    
    # Send file with proper headers
    return send_file(
        latest_apk,
        as_attachment=True,
        download_name=f'Mooviestream-{version}.apk',
        mimetype='application/vnd.android.package-archive'
    )

@app.route('/actor/<int:actor_id>')
def actor_detail(actor_id):
    """Render the actor detail page."""
    try:
        actor = tmdb_api.get_actor_details(actor_id)
        if not actor:
            return render_template('404.html', title='Actor Not Found'), 404
        
        return render_template(
            'actor_detail.html',
            title=actor['name'],
            actor=actor
        )
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return render_template('error.html', title='Error', error_message=error_message)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html', title='Page Not Found'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    return render_template('500.html', title='Server Error'), 500

@app.route('/robots.txt')
def robots():
    """Serve robots.txt file."""
    return app.send_static_file('robots.txt')

@app.route('/manifest.json')
def manifest():
    """Serve manifest.json file."""
    return app.send_static_file('manifest.json')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon for browsers that look for it at the root."""
    return app.send_static_file('images/logo_fav.png')

@app.route('/apple-touch-icon.png')
@app.route('/apple-touch-icon-<int:size>.png')
def apple_touch_icon(size=180):
    """Serve apple-touch-icon with no-cache headers to prevent iOS caching issues."""
    from flask import Response
    import os
    
    # Map sizes to actual files
    size_map = {
        76: 'logo-76.png',
        120: 'logo-120.png',
        152: 'logo-152.png',
        180: 'logo-180.png'
    }
    
    filename = size_map.get(size, 'logo-180.png')
    file_path = os.path.join(app.static_folder, 'images', filename)
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            image_data = f.read()
        
        response = Response(image_data, mimetype='image/png')
        # Add headers to prevent caching - critical for iOS share sheet
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['ETag'] = 'v2'  # Version identifier
        response.headers['Last-Modified'] = 'Thu, 01 Jan 1970 00:00:00 GMT'  # Force revalidation
        return response
    else:
        return app.send_static_file('images/logo-180.png')

@app.route('/vast-mock.xml')
def vast_mock():
    """Serve mock VAST XML for testing."""
    return app.send_static_file('vast-mock.xml')

@app.route('/sitemap.xml')
def sitemap():
    """Generate a dynamic sitemap.xml."""
    try:
        # Create a list to store all URLs
        urls = []
        host_base = request.host_url.rstrip('/')
        
        # Add static pages
        urls.append({
            'loc': host_base,
            'priority': '1.0',
            'changefreq': 'daily'
        })
        urls.append({
            'loc': "{}/about".format(host_base),
            'priority': '0.7',
            'changefreq': 'monthly'
        })
        urls.append({
            'loc': "{}/contact".format(host_base),
            'priority': '0.7',
            'changefreq': 'monthly'
        })
        urls.append({
            'loc': f"{host_base}/privacy",
            'priority': '0.5',
            'changefreq': 'yearly'
        })
        urls.append({
            'loc': f"{host_base}/terms",
            'priority': '0.5',
            'changefreq': 'yearly'
        })
        
        # Add movie listing pages
        urls.append({
            'loc': f"{host_base}/popular",
            'priority': '0.8',
            'changefreq': 'daily'
        })
        urls.append({
            'loc': f"{host_base}/recent",
            'priority': '0.8',
            'changefreq': 'daily'
        })
        urls.append({
            'loc': f"{host_base}/top_rated",
            'priority': '0.8',
            'changefreq': 'weekly'
        })
        
        # Add TV show listing pages
        urls.append({
            'loc': f"{host_base}/tv",
            'priority': '0.8',
            'changefreq': 'daily'
        })
        urls.append({
            'loc': f"{host_base}/tv/popular",
            'priority': '0.8',
            'changefreq': 'daily'
        })
        urls.append({
            'loc': f"{host_base}/tv/recent",
            'priority': '0.8',
            'changefreq': 'daily'
        })
        urls.append({
            'loc': f"{host_base}/tv/top_rated",
            'priority': '0.8',
            'changefreq': 'weekly'
        })
        
        # Add movie genres
        try:
            movie_genres = tmdb_api.get_movie_genres()
            for genre in movie_genres:
                urls.append({
                    'loc': f"{host_base}/genre/{genre['id']}",
                    'priority': '0.7',
                    'changefreq': 'weekly'
                })
        except Exception as e:
            app.logger.error(f"Error fetching movie genres for sitemap: {str(e)}")
        
        # Add TV show genres
        try:
            tv_genres = tmdb_api.get_tv_show_genres()
            for genre in tv_genres:
                urls.append({
                    'loc': f"{host_base}/tv/genre/{genre['id']}",
                    'priority': '0.7',
                    'changefreq': 'weekly'
                })
        except Exception as e:
            app.logger.error(f"Error fetching TV genres for sitemap: {str(e)}")
        
        # Generate XML sitemap
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url in urls:
            xml += '  <url>\n'
            xml += f'    <loc>{url["loc"]}</loc>\n'
            xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
            xml += f'    <priority>{url["priority"]}</priority>\n'
            xml += '  </url>\n'
        
        xml += '</urlset>'
        
        response = app.response_class(
            response=xml,
            status=200,
            mimetype='application/xml'
        )
        return response
    except Exception as e:
        app.logger.error(f"Error generating sitemap: {str(e)}")
        return render_template('error.html', title='Error', error_message=f"Error generating sitemap: {str(e)}")

if __name__ == '__main__':
    app.run(debug=appconfig.Config.DEBUG, port=5003)
