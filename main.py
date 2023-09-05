import urllib.parse
import posixpath
import requests
from bs4 import BeautifulSoup


class Datasheet:

    base_url = 'https://www.datasheetcatalog.com/datasheets_pdf/'

    def __init__(self, key):
        self.key = key.upper()
    
    def split_key(self):
        return [*self.key]
    
    def join_splitted_key(self):
        joined_key = ''

        for char in self.split_key()[:5]:
            joined_key = posixpath.join(joined_key, char)

        return joined_key

    def search(self):
        web = f'{urllib.parse.urljoin(self.base_url, self.join_splitted_key())}'
        web = f'{urllib.parse.urljoin(web, self.key)}'

        return f'{urllib.parse.urljoin(web, f"{self.key}.shtml")}'
    
    def download(self):
        url = self.search()
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find_all('table')[1]
            row = table.find('tr')
            column = row.find_all('td')[2]
            document = column.find('a')

            if document:
                link = document.get('href')
                file = requests.get(link)

                if file.status_code == 200:
                    with open(f'{self.key.lower()}.pdf', 'wb') as local_file:
                        local_file.write(file.content)
                    print('File downloaded successfully')
                else:
                    print('Error downloading file')
            else:
                print('No document finded')
        else:
            print('Error trying to get webpage')

