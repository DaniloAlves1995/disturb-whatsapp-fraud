import time
import re
import argparse
import os

from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from nltk.corpus import stopwords


stopwords_list = stopwords.words('portuguese')
driver = None


def setup_driver():
    """Configure the navigation driver to process
    """
    global driver
    data_path = "./data"

    if not os.path.isdir(data_path):
        os.mkdir(data_path)
    options = webdriver.ChromeOptions()
    options.add_argument(r"user-data-dir="+data_path) # path to storage whatsapp session
    driver = webdriver.Chrome(executable_path='/usr/local/chromedriver/chromedriver', options=options) # path to chromedriver
    driver.get('https://web.whatsapp.com/')

# fraud message used for spam
msg_fraud = "Olá, sou o gerente geral do projeto Am e atualmente estou recrutando uma equipe de meio período. Você pode trabalhar meio período no seu telefone. \
    Um trabalho de meio período leva de 10 a 20 minutos! \
    diário: 500-1500 reais. \
    Este trabalho exige que você tenha pelo menos 20 anos de idade.\
    https://wa.me/559791549659"

def wait_load(tag, type):
    """Wait for certain component on the page finished loading

    Parameters
    ----------

    tag: str
        Attribute value to found an element. Ex: Class name or id value
    type: str
        Type of property use to found an element. Constants from "By" class. Ex: id, class and xpath
    """
    delay = 30
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((type, tag)))
        print("Success loaded!")
    except TimeoutException:
        print("Page no respond")

def is_noContact(title):
    """Gets a chat title and check if it's an unsaved contact

    Parameters
    ----------
    title: str
        The title to be checked

    Returns
    -------
    value bool
        Value of check result if title is a unsaved contact
    """
    return re.sub('\+|\-|\ ','', title).isnumeric()

def get_tokens(txt):
    """Gets a text message and extract an array with just important words

    Parameters
    ----------
    txt: str
        The message to be process

    Returns
    -------
    array
        Array with key-words from the message
    """
    msg_arr = txt.split(' ')
    return [word for word in msg_arr if not word in stopwords_list and word != '']

def check_lastMessage(msg, fraud_tokens):
    """Check if the message received has match with spam key-words

    Parameters
    ----------
    msg: str
        Message to be checked
    fraud_tokens: array
        Array with key-words of spam message

    Returns
    -------
    value bool
        Value indicating if message received is at least 85% similar to spam tokens
    """
    msg_arr = msg.split(' ')
    msg_tokens = [word for word in msg_arr if not word in stopwords_list and word != '']
    rate_match = len(set(fraud_tokens) & set(msg_tokens)) / len(set(fraud_tokens))
    return rate_match > 0.85

def send_crookContact(contact, txt_message, message_number=1):
    """Process to send many messages to crook contact or number

    Parameters
    ----------
    contact: str
        Name or number phone to send messages
    txt_message: str
        Message to be send to crook contact. If it's empty, will be send shrek script
    message_number: int
        Messages amount to send
    """
    setup_driver()
    
    wait_load('pane-side', By.ID)

    # get element with search text field, write the contact name (or number), search and start the conversation
    search_box = driver.find_elements(By.XPATH, "//div[@role='textbox']")[0]
    search_box.send_keys(contact)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)

    # read text file with message to send
    if txt_message == None:
        with open('shrek_script.txt') as file:
            txt_message = file.readlines()

    print("Executing process...")

    # get text input to write the message and send 
    txt_box = driver.find_elements(By.XPATH, "//div[@role='textbox']")[1]
    for i in range(message_number):
        for line in txt_message:
            txt_box.send_keys(line)
            txt_box.send_keys(Keys.ENTER)
            time.sleep(0.2)
    
    print('Process finished!')
        

def send_manyContacts(txt_message):
    """Process to send messages to many contacts used as spam spread

    Parameters
    ----------
    txt_message: str
        Message to be send to all spam contacts
    """
    setup_driver()
    fraud_tokens = get_tokens(msg_fraud)

    # wait for the pane side finish the loading
    wait_load('pane-side', By.ID)

    condition = True
    chat_old, chat_list_processed  = [], []
    scroll_step = 0
    print("Executing process...")

    # execute until check all conversations
    while condition:
        if scroll_step > 0:
            driver.execute_script("document.getElementById('pane-side').scrollTo(0, "+str(scroll_step)+");")
        
        # get elements of each chat on pane-side and a list with chats names
        chat_list = driver.find_elements(By.CLASS_NAME, 'zoWT4')
        chat_current = [chat.get_attribute("textContent") for chat in chat_list]

        # finish if has no new chat clicked and the contact's lists old and current are equals
        if sorted(chat_current) == sorted(chat_old) and not is_newChat:
            print('Process finished!')
            break

        is_newChat = False

        for chat in chat_list: 
        
            # get text of chat (number or contact name)
            title = chat.get_attribute("textContent")
            
            if is_noContact(title) and not title in chat_list_processed:
                # click on the chat, wait load last message and get message text
                chat.click()
                wait_load('_1Gy50', By.CLASS_NAME)
                text = driver.find_element(By.CLASS_NAME, '_1Gy50').find_element(By.CSS_SELECTOR, 'span span').text

                # check if last message is a span message
                if check_lastMessage(text, fraud_tokens):
                    # get chat input and send message
                    textbox = chat.find_elements(By.XPATH, "//div[@role='textbox']")[1]
                    if '\\n' in txt_message:
                        arr_message = txt_message.split('\\n')
                    else:
                        arr_message = [txt_message]

                    for message in arr_message:
                        textbox.send_keys(message)
                        textbox.send_keys(Keys.ENTER)
                        time.sleep(1.0)
                # finish this intaration because is necessary load the elements again after click on conversation
                is_newChat = True
                chat_list_processed.append(title)
                break
        # change the scroll only if there isn't another chat clicked
        if not is_newChat:
            scroll_step += 660

        chat_old = chat_current

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument("-type", '--type', type=int, required=True, 
        help='Process type: 1 - Send messages to many contacts based on spam message;\n2 - Send messages to crash the one crook contact by phone number or contact name')
    argp.add_argument('-messages_number', '--messages_number', type=int, required=False)    
    argp.add_argument('-contact', '--contact', type=str, required=False)
    argp.add_argument('-message', '--message', type=str, required=False)

    args = vars(argp.parse_args())

    if args['type'] == 1:
        msg = args['message']
        if not msg:
            msg = "Olá,\nNa sexta-feira passada você me enviou mensagens de spam oferecendo emprego com um link para o contato de fraude. \
                    Seu whatsApp provavelmente foi clonado por algum golpista que utilizou para enviar essas mensagens, acredito que não apenas para mim. \
                    \nQueria te recomendar que proteja sua conta de whatsApp ativando a verificação em dois fatores, dessa forma eles não podem mais acessar \
                    o seu número. Vou enviar um tutorial de como fazer isso:\n https://www.youtube.com/watch?v=SpCONE_gYKE\n Tenha uma boa noite e se cuide!"
        send_manyContacts(msg)
    elif args['type'] == 2:
        print('\n',50 * '*', '\n* Please use this option just for crook contacts *\n', 50 * '*', '\n', sep='')
        if args['contact']:
            send_crookContact(args['contact'], args['message'], args['messages_number'])
        else:
            print("The argument contact is require for type 2")      
    else:
        print("Type selected doesn't exist, please select one: \n1 - Send messages to many contacts based on spam message;\n2 - Send messages to crash the one crook contact by phone number or contact name")

driver.close()