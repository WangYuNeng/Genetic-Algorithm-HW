'''
Modified from Ray Wu's code
https://github.com/raywu0123
'''

import requests
import pprint
import os

class LabClient:

    def __init__(self, url, student_id):
        self.base_url = url
        self.get_url = f'{self.base_url}population/{student_id}/'
        self.post_url = f'{self.base_url}api/{student_id}'

    def get_population(self, filename, dir_name):
        with open(os.path.join(dir_name, filename), 'w') as f:
            r = requests.get(f'{self.get_url}{filename}')
            f.write(r.text)

    def post_mpm(self, file_path, generation):
        with open(file_path, 'rb') as f:
            r = requests.post(
                self.post_url,
                data={'gen': generation},
                files={'file': f},
            )
        fitness_str = r.json()['fitness']
        target = "Fitness:(Max/Mean/Min):"
        target_idx = fitness_str.find(target)
        max_fitness = float(fitness_str[target_idx + len(target):target_idx + len(target)+5])
        return max_fitness

