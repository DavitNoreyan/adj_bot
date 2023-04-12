import os

current_file_path = os.path.abspath(__file__)


class Constants:
    AUTHORIZATION_PAGE_URL = 'https://www.adjarabet.am/hy/Promo/volcanicwinnings'
    DB_PATH = os.path.join(os.path.dirname(current_file_path), 'app_db.db')
    REQUEST_URL = "https://promos.www.adjarabet.am/volcanicwinnings/WebServices/handler.php"
    PAYLOAD = {
        'userID': '2852619',
        'curLang': 'hy',
        'boxNum': '2',
        'Level': 'NaN',
        'spinType': '1',
        'pMultiplier': '1',
        'wsfilename': 'Ajax-Game.php',
        'env': 'production',
        'domain': 'am',
        'promoCorePath': '/var/www/html/promo.v.5',
    }
    PRIZE_PAYLOAD = {
        'userID': '2852619',
        'curLang': 'hy',
        'PeriodCurr': '7',
        'wsfilename': 'Ajax-Main.php',
        'env': 'production',
        'domain': 'am',
        'promoCorePath': '/var/www/html/promo.v.5',
    }
