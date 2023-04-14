import datetime
import json
import time

import requests
import aiohttp
from random import randint

from constants import Constants

from logger import Logger


class Requests:
    def __init__(self):
        self.url = Constants.REQUEST_URL
        self.logger = Logger

    async def request(self, count, user_id):
        self.check_server_availavlity(user_id)
        async with aiohttp.ClientSession() as session:
            for _ in range(count):
                box_num = randint(1, 20)
                payload = Constants.PAYLOAD
                payload['userID'] = user_id
                payload['boxNum'] = f'{box_num}'
                async with session.post(url=self.url, data=payload) as response:
                    self.logger.info(f'fast request status code is {response.status}')

    async def request_periodical(self, user, user_list, period, duration):
        self.check_server_availavlity(user[2].cget('text'))
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
                    async with session.post(url=self.url, data=payload) as response:
                        self.logger.info(
                            f'periodical request status code is {response.status} for user {user_id_header.cget("text")}')
                        self.logger.info(f'wait {period / 40}')
            time.sleep(float(period / 40))

    def get_prize_chance_count(self, user_id):
        self.check_server_availavlity(user_id)
        payload = Constants.PRIZE_PAYLOAD
        payload['userID'] = user_id
        response = requests.post(url=self.url, data=payload)
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
        while True:
            start = datetime.datetime.now()
            payload = Constants.PRIZE_PAYLOAD
            payload['userID'] = user_id
            response = requests.post(url=self.url, data=payload)
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


if __name__ == '__main__':
    start = datetime.datetime.now()
    obj = Requests()
    # asyncio.run(obj.request(count=5, user_id='2852619'))
    # end = datetime.datetime.now()
    # print(end - start)
    # dict_1 = obj.get_prize_chance_count(user_id='2852619').get("SpinIds").get('avialable_try')
    # print(dict_1)
    start_tict = obj.get_prize_chance_count(user_id='2852619')
