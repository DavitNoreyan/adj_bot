import asyncio
import datetime
import json
import threading
import time

import requests
import aiohttp
from random import randint, choice
from concurrent.futures import ThreadPoolExecutor

from constants import Constants
from database import Database

from logger import Logger


class Requests:
    def __init__(self):
        self.url = Constants.REQUEST_URL
        self.logger = Logger
        self.prize_mapper = {
            '206': '300K Symbol',
            '205': '500K Symbol',
            '204': '1mln Symbol',
            '1': '5mln Symbol',
            '2': '20mln Symbol',
            '3': 'Car Symbol',
            '35': '100000',
            '36': '1000000',
            '33': '50000',
            '34': '20000'
        }

    def request_for_prize(self, user_id, period):
        try:
            self.check_server_availavlity(user_id)
            start = datetime.datetime.now()
            db = Database()
            user_hash = db.get_one_user(user_id)[4]
            PRIZE_PAYLOAD = Constants.PAYLOAD
            PRIZE_PAYLOAD['userID'] = f'{user_id}'
            REFRESH_PAYLOAD = Constants.REFRESH_PAYLOAD
            REFRESH_PAYLOAD['userID'] = f'{user_id}'
            REFRESH_PAYLOAD['handlerHash'] = user_hash
            headers = Constants.REQUEST_HEADERS
            while True:
                spinids = self.get_prize_chance_count(user_id).get("SpinIds")
                chance_count = spinids.get('avialable_try')
                if int(chance_count) > 0:
                    self.logger.info(f"user is {user_id}  chance count is {chance_count}")
                    box = randint(0, 19)
                    PRIZE_PAYLOAD['boxNum'] = f'{box}'
                    resource = requests.post(url=self.url, data=PRIZE_PAYLOAD, headers=headers)
                    if resource.json().get('PrizeID') in self.prize_mapper:
                        self.logger.info(f"prize is {self.prize_mapper.get(resource.json().get('PrizeID'))}")
                    else:
                        self.logger.info(f"prize is NOT VALID")
                    prize_id = resource.json().get('PrizeID')
                    if prize_id in Constants.VALID_PRIZE:
                        if prize_id == '206':
                            if prize_id in self.prize:
                                self.random_request(url=self.url, payload=PRIZE_PAYLOAD, headers=headers)
                                self.logger.info(f'user {user_id} your prize symbol is 300K!...')
                                return
                            self.prize.append(prize_id)
                        if prize_id == '205':
                            if prize_id in self.prize:
                                self.random_request(url=self.url, payload=PRIZE_PAYLOAD, headers=headers)
                                self.logger.info(f'user {user_id} your prize symbol is 500K!...')
                                return
                            self.prize.append(prize_id)
                        if prize_id == '204':
                            if prize_id in self.prize:
                                self.random_request(url=self.url, payload=PRIZE_PAYLOAD, headers=headers)
                                self.logger.info(f'user {user_id} your prize symbol is 1mln!...')
                                return
                            self.prize.append(prize_id)
                        if prize_id == '1':
                            if prize_id in self.prize:
                                self.random_request(url=self.url, payload=PRIZE_PAYLOAD, headers=headers)
                                self.logger.info(f'user {user_id} your prize symbol is 5mln!...')
                                return
                            self.prize.append(prize_id)
                        if prize_id == '2':
                            if prize_id in self.prize:
                                self.random_request(url=self.url, payload=PRIZE_PAYLOAD, headers=headers)
                                self.logger.info(f'user {user_id} your prize symbol is 20mln!...')
                                return
                            self.prize.append(prize_id)
                        if prize_id == '3':
                            if prize_id in self.prize:
                                self.random_request(url=self.url, payload=PRIZE_PAYLOAD, headers=headers)
                                self.logger.info(f'user {user_id} your prize symbol is Car!...')
                                return
                            self.prize.append(prize_id)
                        time.sleep(period)
                        continue
                    else:
                        end = datetime.datetime.now()
                        delta = end - start
                        self.logger.info(f'searching symbol for user  {user_id} period is {delta.seconds}!...')
                        if delta.seconds > 120:
                            requests.post(url=self.url, data=REFRESH_PAYLOAD, headers=headers)
                            return
                        requests.post(url=self.url, data=REFRESH_PAYLOAD, headers=headers)
                        self.prize = []
                        self.logger.info(f'user {user_id} it is refresh!...')
                else:
                    self.logger.info(f'user {user_id} dont have a chance!...')
                    return
        except Exception:
            return

    @staticmethod
    def random_request(url, payload, headers):
        for _ in range(10):
            box = randint(0, 19)
            payload['boxNum'] = f'{box}'
            requests.post(url=url, data=payload, headers=headers)

    async def request(self, count, user_list, user):
        self.check_server_availavlity(user[2].cget('text'))
        async with aiohttp.ClientSession() as session:
            tasks = []
            for one_user in user_list:
                task = asyncio.create_task(self.request_by_user(session=session, count=count, one_user=one_user))
                tasks.append(task)

            await asyncio.gather(*tasks)

    async def pyramid_fast(self, count, user_list, user):
        self.check_server_availavlity(user[2].cget('text'))
        tasks = [self.request_pyramid(user) for user in user_list]
        await asyncio.gather(*tasks)

    async def request_by_user(self, session, count, one_user):
        for _ in range(count):
            box_num = randint(1, 20)
            payload = Constants.PAYLOAD
            payload['userID'] = one_user[2].cget('text')
            payload['boxNum'] = f'{box_num}'
            async with session.post(url=self.url, data=payload) as response:
                pass
                self.logger.info(f'fast request status code is {response.status} user is {one_user[2].cget("text")}')

    async def request_pyramid(self, user):
        user_num = user[2].cget('text')
        for gamelevel in range(5):
            box_num = choice([num for num in range(1, 5 - gamelevel + 1)])
            payload = Constants.pyramid_payload
            payload['boxNum'] = f'{box_num}'
            payload['gameLevel'] = f'{gamelevel}'
            payload['userID'] = f"{user_num}"
            payload['hour'] = f'{datetime.datetime.now().hour}'
            url = Constants.REQUEST_URL
            headers = Constants.REQUEST_HEADERS
            response = requests.post(url=url, data=payload,headers=headers)
            self.logger.info(f' request for user {user_num} game level is {gamelevel} box_ num is  {box_num} status code is {response.status_code}')


    async def request_periodical(self, user, user_list, period, duration):
        self.check_server_availavlity(user[2].cget('text'))
        headers = Constants.REQUEST_HEADERS
        start = datetime.datetime.now()
        while True:
            for var, checkbox, user_id_header, username_header, chance_count, delete_button in user_list:
                end = datetime.datetime.now()
                delta = end - start
                if delta.seconds > duration:
                    break
                box_num = randint(1, 20)
                async with aiohttp.ClientSession() as session:
                    # for _ in range(10):
                    payload = Constants.PAYLOAD
                    payload['userID'] = user_id_header.cget('text')
                    payload['boxNum'] = f'{box_num}'
                    async with session.post(url=self.url, data=payload, headers=headers) as response:
                        self.logger.info(
                            f'periodical request status code is {response.status} for user {user_id_header.cget("text")}')
                        self.logger.info(f'wait {period / 40}')
            time.sleep(float(period / 40))

    def get_prize_chance_count(self, user_id):
        self.check_server_availavlity(user_id)
        payload = Constants.PRIZE_PAYLOAD
        payload['userID'] = user_id
        headers = Constants.REQUEST_HEADERS
        response = requests.post(url=self.url, data=payload, headers=headers)
        self.logger.info(f'prize and chance checking request status code is {response.status_code}')
        return json.loads(response.content)

    def check_bodies(self, start_json, end_json):
        if start_json.get('cnt').get('count_car') != end_json.get('cnt').get('count_car'):
            self.logger.info(f'available is change in Car...')
            return 'Car'
        elif start_json.get('cnt').get('count_iphone') != end_json.get('cnt').get('count_iphone'):
            self.logger.info(f'available is change in 20 mln...')
            return '20 mln'
        elif start_json.get('cnt').get('count_cash_high') != end_json.get('cnt').get('count_cash_high'):
            self.logger.info(f'available is change in 5mln...')
            return '5 mln'
        elif start_json.get('cnt').get('othericon1_1Mln') != end_json.get('cnt').get('othericon1_1Mln'):
            self.logger.info(f'available is change in 1mln...')
            return '1 mln'
        elif start_json.get('cnt').get('othericon2_500k') != end_json.get('cnt').get('othericon2_500k'):
            self.logger.info(f'available is change in 500k...')
            return '500k'
        elif start_json.get('cnt').get('othericon3_300k') != end_json.get('cnt').get('othericon3_300k'):
            self.logger.info(f'available is change in 300k...')
            return '300k'
        else:
            self.logger.info(f'not available is change...')
            return ''

    def check_server_availavlity(self, user_id):
        headers = Constants.REQUEST_HEADERS
        while True:
            start = datetime.datetime.now()
            payload = Constants.PRIZE_PAYLOAD
            payload['userID'] = user_id
            response = requests.post(url=self.url, data=payload, headers=headers)
            if response.status_code == 200:
                end = datetime.datetime.now()
                delta = end - start
                if delta.seconds > 2:
                    self.logger.info(f'server is not available...')
                    continue
                else:
                    self.logger.info(f'server is available...')
                    break
            else:
                continue

    def tracking_request(self, period, user_id, start_json):
        self.check_server_availavlity(user_id)
        while True:
            self.logger.info(f'Tracking is started...')
            end_json = self.get_prize_chance_count(user_id)
            result = self.check_bodies(start_json=start_json, end_json=end_json)
            if result:
                return result
            self.logger.info(f'wait {period} seconds')
            time.sleep(period)

    def standart_request(self, user, box):
        payload = Constants.PAYLOAD
        payload['userID'] = f'{user}'
        payload['boxNum'] = f'{box}'
        headers = Constants.REQUEST_HEADERS
        url = Constants.REQUEST_URL
        response = requests.post(url=url, data=payload, headers=headers)
        return response.json().get('PrizeID')

    def get_chance_and_board(self, user):
        payload = Constants.PRIZE_PAYLOAD
        payload['userID'] = f'{user}'
        headers = Constants.REQUEST_HEADERS
        response = json.loads(requests.post(url=self.url, data=payload, headers=headers).content)
        spinids = response.get("SpinIds")
        chance_count = spinids.get('avialable_try')
        board = response.get('arrLive')
        chance_and_board = {
            'chance': int(chance_count),
            'board': board
        }
        return chance_and_board

    def standart_request_functionality(self, user, period):
        while True:

            chance_and_board = self.get_chance_and_board(user)
            chance = chance_and_board.get('chance')
            board = chance_and_board.get('board')
            board_places = [f'{num}' for num in range(1, 21)]
            board_stack = [av_prize.get('PRIZE_ID') for av_prize in board]
            if chance:
                self.logger.info(f'opening for user {user} chance count is {chance}')
                if board:
                    places = [place.get('PLACE_') for place in board]
                    for n in places:
                        board_places.remove(n)
                    box = choice(board_places)
                else:
                    box = f"{randint(1, 20)}"
                if '301' in board_stack or '302' in board_stack or '303' in board_stack or '304' in board_stack:
                    self.refresh_request(user)
                    self.logger.info(f'trying refresh for user {user}')
                    time.sleep(2)
                prize = self.standart_request(user=user, box=box)
                self.logger.info(f'prize is {prize}')
                if not prize:
                    payload = Constants.star_box_payload
                    payload['userID'] = f"{user}"
                    payload['boxNum'] = f"{randint(1, 4)}"
                    requests.post(url=self.url, headers=Constants.REQUEST_HEADERS, data=payload)
            else:
                self.logger.info(f'chance count is 0 for user {user}')
                return
            self.logger.info(f'wait {period} seconds for user {user}')
            time.sleep(period)

    def standart_requests_by_user_list(self, user_list, period):
        while True:
            with ThreadPoolExecutor(max_workers=30) as executor:
                for user in user_list:
                    executor.submit(self.standart_request_functionality, user, period)
            time.sleep(5)



    def refresh_request(self, user):
        refresh_payload = Constants.REFRESH_PAYLOAD
        refresh_payload['userID'] = f"{user}"
        requests.post(url=self.url, headers=Constants.REQUEST_HEADERS, data=refresh_payload)


if __name__ == '__main__':
    start = datetime.datetime.now()
    obj = Requests()
    start_tict = obj.get_prize_chance_count(user_id='2852619')
