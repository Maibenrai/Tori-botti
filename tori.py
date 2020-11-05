from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import bot
import item

# Metodi lähettää telegram-viestin minulle
def send_telegram_message(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot.token + '/sendMessage?chat_id=' + bot.chatID + '&parse_mode=Markdown&text=' + bot_message
    requests.get(send_text)

def search():
    URL = f'https://www.tori.fi/koko_suomi?q={item.item}' 

    class bcolors:
        HEADER = '\033[95m'
        WARNING = '\033[93m'
        OKGREEN = '\033[92m'
        ENDC = '\033[0m' 
    
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    # Voidaan tarkastella vain ensimmäistä tuotetta, koska niitä tulee niin harvoin myyntiin
    product_list = soup.findAll('div', attrs={'class': 'list_mode_thumb'})
    first_product = soup.find('a', attrs={'class': 'item_row_flex'})

    def get_info(div, class_name):
        return first_product.find(div, attrs={'class': class_name}).text

    # Puretaan tarkasteltavan tuotteen tiedot pienempiin osiin
    desc = get_info('div', 'li-title')
    price = get_info('div', 'list-details-container').replace(" ", "")
    date = " ".join(get_info('div', 'date_image').split())

    # Avataan tiedosto johon on tallennettuna vanhimman clavinovan tiedot
    file = open('latest_item.txt')
    old_clavinova = file.read().strip()
    file.close()

    # Tutkitaan onko sivulta haettu clavinova sama vai eri kuin tiedostossa oleva
    if old_clavinova == desc:
        print('Uusin tuote oli sama, ei tehdä mitään')
    else:
        print('Ei ollut sama, lähetään viesti')
        # Päivitetään uusin tuote listalle
        file = open('latest_item.txt', 'w')
        file.write(desc)
        file.close()
        send_telegram_message(f"Uusi {item.item} löytynyt: { desc }")


    # Alla oleva koodi tulostaa nätin rimpsun haetuista tuotteista käyttäjän terminaaliin
    for product in product_list:
        descriptions = product.findAll('div', attrs={'class': 'li-title'})
        prices = product.findAll('div', attrs={'class': 'list-details-container'})
        dates = product.findAll('div', attrs={'class': 'date_image'})

        for desc, price, date in zip(descriptions, prices, dates):
        # Jos price.text > 2 eli tuotteella on hinta
            if len(price.text) > 2:
                    price_no_linebreak = price.text.replace("\n", "")
                    date_no_linebreak = " ".join(date.text.split())
                    print(f"{bcolors.HEADER}TUOTE:{bcolors.ENDC} { desc.text }, {bcolors.WARNING}HINTA:{bcolors.ENDC} { price_no_linebreak }, {bcolors.OKGREEN}PÄIVÄMÄÄRÄ:{bcolors.ENDC} { date_no_linebreak }")

# Hakee joka 30min uudet tiedot netistä
scheduler = BlockingScheduler()
scheduler.add_job(search, 'interval', seconds=120)
search()

scheduler.start()
