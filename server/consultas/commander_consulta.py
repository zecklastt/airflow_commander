import os
import requests
import json
from datetime import datetime


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

    def commander_data(self):
        response = requests.get(
            'https://json.edhrec.com/static/daily', headers=self.headers)
        content = json.loads(response.content)
        daily = content['daily']
        name = daily['name']
        url = daily['url']
        return name, url

    def _create_file_name(self):
        data_inicio = datetime.today().strftime('%d-%m-%Y')
        file_name = f'Commander_of_day-{data_inicio}.txt'
        return file_name

    def _save_data(self, data):
        file_path = Configuration.COMMANDER_PATH
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_name = self._create_file_name()
        file_path = os.path.join(file_path, file_name)

        try:
            with open(file_path, 'x') as commander_file:
                commander_file.write(str(data))
        except FileExistsError:
            raise FileExistsError(f'Arquivo de hoje já existe na pasta {file_path}.')

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