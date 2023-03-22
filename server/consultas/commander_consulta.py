import os
import requests
import json
from datetime import datetime
from server.config.MongoDBConfig import get_connection
import pytz


class Configuration:
    COMMANDER_PATH = os.path.join(os.getcwd(), 'commander/')
    HEADERS = {
        'authority': 'json.edhrec.com',
        'accept': '*/*',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'origin': 'https://edhrec.com',
        'pragma': 'no-cache',
        'referer': 'https://edhrec.com/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    }


class CommanderScraper:
    def __init__(self):
        self.headers = Configuration.HEADERS
        self.collection = get_connection()['commanders']

    def _save_data(self, data):
        commander = {
            'name': data[0],
            'url': data[1],
            'date': datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M'),
        }

        try:
            result = self.collection.insert_one(commander)
            print(
                f"Commander {commander['name']} salvo com o ID {result.inserted_id}")
        except Exception as e:
            raise Exception(f'Erro ao salvar o commander: {str(e)}')

    def commander_data(self):
        response = requests.get(
            'https://json.edhrec.com/static/daily', headers=self.headers)
        content = json.loads(response.content)
        daily = content['daily']
        name = daily['name']
        url = daily['url']
        return name, url

    def save_commander(self):
        try:
            data = self.commander_data()
            self._save_data(data)
        except requests.exceptions.RequestException:
            raise Exception('Erro ao obter dados da API.')
        except FileExistsError as e:
            print(str(e))
        except Exception as e:
            raise Exception(f'Erro ao salvar o arquivo: {str(e)}')


scrapper = CommanderScraper()
scrapper.save_commander()
