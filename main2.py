from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pyautogui
import os
import mysql.connector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from date_card_character import Web_Scraper
# Configurações de conexão
conn = mysql.connector.connect(
    user='root',
    password='123456789',
    host='127.0.0.1',
    database='cartasGOT'
)

cursor = conn.cursor()

# Configurar as opções do Chrome para ignorar avisos de segurança
chrome_options = Options()
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--incognito")  # Modo anônimo

# Criar um driver para o navegador Chrome com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.cardgamedb.com/index.php/gameofthrones/game-of-thrones-deck-builder")
    time.sleep(2)

    # Encontrar o elemento usando XPath e clicar nele
    card_option_element = driver.find_element(By.XPATH, "//li[@class='cardOption']")
    card_option_element.click()

    # Encontrar todos os elementos <input> que estão checked e não contêm a classe "ui-helper-hidden-accessible"
    input_elements = driver.find_elements(By.XPATH, "//input[@checked and not(contains(@class, 'ui-helper-hidden-accessible')) and not(@name='rememberMe')]")
    time.sleep(1)

    # Iterar sobre cada elemento e clicar
    for input_element in input_elements:
        input_element.click()

    time.sleep(1)

    # Selecionar a casa que vai procurar
    driver.find_element(By.XPATH, "//input[@name='baratheonFB']").click()

    # Definir o tipo da carta
    driver.find_element(By.XPATH, "//div[@id='s2id_filterUnique']/a[@class='select2-choice']").click()
    driver.find_element(By.XPATH, "//div[@class='select2-result-label' and contains(text(), 'Any')]").click()
    time.sleep(1)

    # Encontrar e clicar na opção "Character"
    driver.find_element(By.XPATH, "//div[@id='s2id_filterType']").click()
    driver.find_element(By.XPATH, "//div[@class='select2-result-label' and contains(text(), 'Agenda')]").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@value='Search']").click()
    time.sleep(3)

    names_cards = driver.find_elements(By.XPATH, "//tr/td[2]")
    names_cards[0].click()
    time.sleep(2)

    # Definir o caminho da pasta onde deseja salvar as imagens
    save_folder = r"E:\Cartas do Game of thrones\cartasGOT\Barath"
    os.makedirs(save_folder, exist_ok=True)

    webscraping =  Web_Scraper(driver, save_folder)
    view_search_cristeria = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@id='searchandresults']"))
)

    # =============== PEGANDO AS CARTAS AGENDAS ========================
    webscraping.process_card_agenda( names_cards,save_folder)
    time.sleep(2)
    view_search_cristeria.click()
    # Definir o tipo da carta
    driver.find_element(By.XPATH, "//div[@id='s2id_filterType']/a[@class='select2-choice']").click()
    time.sleep(10)
    driver.find_element(By.XPATH, "//div[@class='select2-result-label' and contains(text(), 'Agenda')]").click()
    time.sleep(1)
    # Encontrar e clicar na opção "Character"
    driver.find_element(By.XPATH, "//div[@id='s2id_filterType']").click()
    driver.find_element(By.XPATH, "//div[@class='select2-result-label' and contains(text(), 'Character')]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@value='Search']").click()
    time.sleep(3)
    names_cards = driver.find_elements(By.XPATH, "//tr/td[2]")
    names_cards[0].click()
    time.sleep(2)
    # =============== PEGANDO AS CARTAS PERSONAGEM ========================
    webscraping.process_card_character( names_cards,save_folder)
    view_search_cristeria.click()

   
except Exception as e:
    print(f"Ocorreu um erro durante a execução: {str(e)}")
finally:
    # Garantir que a conexão com o banco e o driver sejam fechados
    if cursor:
        cursor.close()

    if conn:
        conn.close()
    if driver:
        driver.quit()