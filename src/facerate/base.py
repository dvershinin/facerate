from bs4 import BeautifulSoup


class BaseFaceRate:
    def __init__(self):
        self.base_url = 'https://face-score.com/en'
        self.timeout = 60

    def parse_response(self, response_text):
        soup = BeautifulSoup(response_text, 'lxml')
        score = soup.find(class_='facescore-text10').text.strip()
        top_percentage = soup.find(class_='facescore-text12').text.replace(
            'TOP', '').strip().replace('%', '')

        return {
            'score': float(score),
            'top': float(top_percentage)
        }
