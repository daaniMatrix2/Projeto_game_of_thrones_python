from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pyautogui
import os
import mysql.connector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    # Abrir a página desejada
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
    driver.find_element(By.XPATH, "//input[@name='neutralFB']").click()

    # Definir o tipo da carta
    driver.find_element(By.XPATH, "//div[@id='s2id_filterUnique']/a[@class='select2-choice']").click()
    driver.find_element(By.XPATH, "//div[@class='select2-result-label' and contains(text(), 'Any')]").click()
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

    # Pegar o array de nomes
    for card in names_cards:
        text = driver.execute_script("return arguments[0].firstChild.textContent;", card).strip()
        text = str(text)

    # Achar o atributo
    atributo_card = driver.find_element(By.XPATH, "//div[@id='viewDiv']/b")

    # Definir o caminho da pasta onde deseja salvar as imagens
    save_folder = r"E:\Cartas do Game of thrones\cartasGOT\Barath"
    os.makedirs(save_folder, exist_ok=True)

    
    for card in names_cards:
        text = driver.execute_script("return arguments[0].firstChild.textContent;", card).strip()
        card.click()
        time.sleep(2)

        # Pegar o texto do efeito
        card_effect = driver.find_element(By.XPATH, "//div[@id='viewDiv']")
        card_effect_text = driver.execute_script("return arguments[0].lastChild.textContent;", card_effect).strip()

        try:
            # Pegar o elemento <b> que contém o texto "Brotherhood."
            atributo_text_element = driver.find_element(By.XPATH, "//div[@id='viewDiv']/b")
            # Obter o texto do elemento <b> e fazer o strip para remover espaços em branco
            atributo_text = atributo_text_element.text.strip()
        except Exception as e:
            atributo_text = ""
        

        try:
            # Pegar o elemento pai que contém os textos
            view_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "viewDiv")))

            # Capturar o texto "Deadly." diretamente
            texts = view_div.find_elements(By.XPATH, ".//text()")

            card_palavra_chave_text = atributo_text.find_element(By.XPATH, "following-sibling::text()[1]").strip()  # Pega o texto logo após
            
        except Exception as e:
            card_palavra_chave_text = ""  # Caso ocorra erro, atribuimos uma string vazia

        # Usar JavaScript para obter o texto "Maester"
        # try:
        #     atributo_text = driver.execute_script("return arguments[0].childNodes[3].textContent;", card_effect).strip()
        # except Exception as e:
        #     atributo_text = ""
        # Localizando a imagem dentro da `div` especificada
        image_element = driver.find_element(By.XPATH, '//div[@style="height:310px"]/img[@class="viewImage"]')

        # ==================SALVA AS IMAGENS =======================
        # Obter a posição da imagem na tela
        location = image_element.location
        size = image_element.size
        
        center_x = location['x'] + size['width'] // 2
        center_y = location['y'] + size['height'] // 1

        # Movendo o mouse para a posição da imagem e clicando com o botão direito
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click(button='right')

        # Espera para o menu de contexto abrir
        time.sleep(1)

        # Navegar no menu de contexto e selecionar "Salvar imagem como..."
        for _ in range(2):
            pyautogui.press('down')
        time.sleep(3)
        pyautogui.press('enter')

        # Aguardar o tempo necessário para a janela de salvar abrir
        time.sleep(2)

        # Digitar o nome do arquivo com o caminho completo
        pyautogui.write(os.path.join(save_folder, f"{text}.jpg"))
        time.sleep(1)
        pyautogui.press('enter')

        # ==================BANCO =======================
        # # SQL para inserir o nome na tabela 'personagem'
        # query = """
        # INSERT INTO personagem (nome, descricao, casa, ataque_machado, ataque_intriga, atributos, custo, palavra_chave)
        # VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        # """
        # cursor.execute(query, (text, card_effect_text, 'teste', 1, 1, 1, 4, 'teste'))

        # # Confirma a transação
        # conn.commit()

        print(f"Resultado final: \n\nNome: {str(text).upper()}, \nefeito: {str(card_effect_text).upper()}\n, casa :'Baratheon',atributo: {atributo_text.upper()}\n, Palavra chave: {card_palavra_chave_text.upper()} \n===== next =====")
        # print(f"argurmento: {argumentos1}, argumento2: {argumentos2}, argumento3: {argumentos3}")

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
