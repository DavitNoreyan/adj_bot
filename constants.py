import os

current_file_path = os.path.abspath(__file__)


class Constants:
    AUTHORIZATION_PAGE_URL = 'https://www.adjarabet.am/hy/Promo/volcanicwinnings'
    DB_PATH = os.path.join(os.path.dirname(current_file_path), 'app_db.db')
    REQUEST_URL = "https://promos.www.adjarabet.am/xaxerikarusel/WebServices/handler.php"
    PAYLOAD = {
        'userID': '',
        'curLang': 'hy',
        'boxNum': '4',
        'spinType': '1',
        'gameID': '1',
        'pMultiplier': '1',
        'wsfilename': 'Ajax-Game.php',
        'env': 'production',
        'domain': 'am',
        'promoCorePath': '/var/www/html/promo.v.5',
    }
    PRIZE_PAYLOAD = {
    'userID': '',
    'curLang': 'hy',
    'wsfilename': 'Ajax-Live.php',
    'env': 'production',
    'domain': 'am',
    'promoCorePath': '/var/www/html/promo.v.5',
    'handlerHash': 'a718cbda40712cc3adea089ac6a1d571082767efde80a381f179aa98bc2846b7'
}
    REFRESH_PAYLOAD = {
    "userID": "",
    "gameID": "1",
    "curLang": "hy",
    "wsfilename": "Ajax-Cashout.php",
    "env": "production",
    "domain": "am",
    "promoCorePath": "/var/www/html/promo.v.5",
    "handlerHash": "a718cbda40712cc3adea089ac6a1d571082767efde80a381f179aa98bc2846b7"
}
    REQUEST_HEADERS = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7,hy;q=0.6',
        'Content-Length': '256',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://promos.www.adjarabet.am',
        'Referer': 'https://promos.www.adjarabet.am/slotboyard/',
        'Sec-Ch-Ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'


    }
    star_box_payload = {
        "userID": "2632365",
        "curLang": "hy",
        "boxNum": "1",
        "wsfilename": "Ajax-StarGame.php",
        "env": "production",
        "domain": "am",
        "promoCorePath": "/var/www/html/promo.v.5",
        "handlerHash": "a718cbda40712cc3adea089ac6a1d571082767efde80a381f179aa98bc2846b7"
    }
    VALID_PRIZE = ['206', '205', '1', '204', '2', '3', '35', '36', '33', '34']
