from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import bot

def send_telegram_message(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot.token + '/sendMessage?chat_id=' + bot.chatID + '&parse_mode=HTML&text=' + bot_message
    requests.get(send_text)

def search():
    URL = f'https://www.tori.fi/pohjois-pohjanmaa?q=&cg=0&w=1&st=g&ca=2&l=0&md=th'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    counter = 0
    for link in soup.find_all('a', attrs={'class': 'item_row_flex'}, href=True, id=True):
        item_url = link['href']
        item = link['id']
        if counter == 0:
            file = open('latest_item.txt')
            old_item = file.read().strip()
            file.close()
            if old_item == item:
                print('Same, nothing to do')
            else:
                print('New, time to send a Telegram message')
                file = open('latest_item.txt', 'w')
                file.write(item)
                file.close()
                send_telegram_message(f"{item_url}")
        counter = counter + 1
        print(item_url)
scheduler = BlockingScheduler()
scheduler.add_job(search, 'interval', seconds=120)
search()
scheduler.start()

