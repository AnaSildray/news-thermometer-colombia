"""
News sources configuration for Colombian news portals
"""

NEWS_SOURCES = {
    'el_tiempo': {
        'name': 'El Tiempo',
        'url': 'https://www.eltiempo.com',
        'sections': [
            'https://www.eltiempo.com/colombia',
            'https://www.eltiempo.com/politica'
        ],
        'article_selector': 'article.lista',
        'title_selector': 'h2.titulo a',
        'comments_selector': 'div.comentarios'
    },
    'caracol': {
        'name': 'Caracol Noticias',
        'url': 'https://www.caracolnoticias.com',
        'sections': [
            'https://www.caracolnoticias.com',
            'https://www.caracolnoticias.com/noticias'
        ],
        'article_selector': 'div.article',
        'title_selector': 'h3.article-title',
        'comments_selector': 'div.comments'
    },
    'rcn': {
        'name': 'RCN Noticias',
        'url': 'https://www.rcnradio.com',
        'sections': [
            'https://www.rcnradio.com/noticias',
            'https://www.rcnradio.com'
        ],
        'article_selector': 'article.post',
        'title_selector': 'h2',
        'comments_selector': 'div.comments'
    },
    'lafm': {
        'name': 'La FM',
        'url': 'https://www.lafm.com.co',
        'sections': [
            'https://www.lafm.com.co/noticias',
            'https://www.lafm.com.co'
        ],
        'article_selector': 'div.news',
        'title_selector': 'h3',
        'comments_selector': 'div.reactions'
    }
}

def get_source_config(source_name):
    """Get configuration for a specific news source"""
    return NEWS_SOURCES.get(source_name)

def get_all_sources():
    """Get all available sources"""
    return list(NEWS_SOURCES.keys())

def get_source_names():
    """Get human-readable names of all sources"""
    return {key: value['name'] for key, value in NEWS_SOURCES.items()}
