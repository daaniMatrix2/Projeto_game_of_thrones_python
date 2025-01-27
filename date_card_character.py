import os
import time
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Web_Scraper:
    def __init__(self, driver, save_folder):
        self.driver = driver
        self.save_folder = save_folder
        os.makedirs(save_folder, exist_ok=True)

    def process_card_character(self, names_cards,save_folder):
        print("============== CARTA PERSONAGEM =======================")
        for card in names_cards:
            # =============== PEGANDO O NOME DA CARTA==================
            text = self.driver.execute_script("return arguments[0].firstChild.textContent;", card).strip().upper()
            card.click()
            time.sleep(2)
            # =============== PEGANDO EFEITO ===================
            card_effect = self.driver.find_element(By.XPATH, "//div[@id='viewDiv']")
            try:
                card_effect_text = self.driver.execute_script("return arguments[0].lastChild.textContent;", card_effect).strip()
            except:
                card_effect_text = "Não tem efeito"
            # Encontrar todos os elementos dentro da div
            elements = card_effect.find_elements(By.XPATH, ".//*")
            # # Converter a lista de elementos em uma lista de strings
            element_texts = list(map(lambda element: element.text, elements))



            # Iterar pelos elementos e buscar o valor entre as tags <br>
            valor_desejado = None
            for i in range(1, len(elements) - 1):  # Começa do segundo e termina no penúltimo
                elemento_anterior = elements[i - 1]
                elemento_atual = elements[i]
                elemento_posterior = elements[i + 1]
                

                # Verificar se o elemento atual está entre tags <br> e se é a única coisa na linha
                if elemento_anterior.tag_name == 'br' and elemento_posterior.tag_name == 'br' and elemento_atual.text.strip() == elemento_atual.text:
                    valor_desejado = elemento_atual.text.strip()
                
                    break

            # # Atribuir o valor encontrado à variável card_palavra_chave_text
            # if valor_desejado:
            #     card_palavra_chave_text = valor_desejado
            # else:
            #     card_palavra_chave_text = ""
            
            # ============== PEGANDO A PALAVRA CHAVE ======================
            elemneto_completo_Card = self.driver.find_element(By.XPATH, "//div[@id='viewDiv']")

            # Encontrar todos os elementos dentro da div com id 'viewDiv'
            elementos_dentro_da_div = elemneto_completo_Card.find_elements(By.XPATH, ".//*")
            if len(elementos_dentro_da_div) == 8:

                # Aguarde ou navegue até o elemento desejado antes de capturar
                elementos3 = self.driver.find_elements(By.XPATH, "//*[@id='viewDiv']")

                # Iterar pelos elementos para capturar o texto
                for elemento4 in elementos3:
                    texto_completo1 = elemento4.text  # Captura o texto do elemento
                    partes = texto_completo1.split('.')  # Divide o texto pelo ponto (.)
                    
                    # Verifica se existem ao menos 2 partes após a divisão
                    if len(partes) > 1:
                        segundo_valor = partes[1].strip()  # Pega o segundo valor e remove espaços extras
                        # print('SEGUNDO VALOR:', segundo_valor)
                        palavra_chave = segundo_valor
            
            elif len(elementos_dentro_da_div) == 7:
                palavra_chave = "Não tem"

            # ============= PEGANDO ATRIBUTO =================
            try:
                atributo_text = element_texts[5].strip()
            except Exception as e:
                atributo_text = ""


            # Localizando a imagem dentro da `div` especificada
            image_element = self.driver.find_element(By.XPATH, '//div[@style="height:310px"]/img[@class="viewImage"]')

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

            print(f"\n\n======== Resultado ========\nNome: {str(text).upper()}, \nEfeito: {str(card_effect_text).upper()}\nCasa :'Baratheon',\nAtributo: {atributo_text.upper()},\nPalavra chave: {palavra_chave.upper()}\n  Tipo de carta: Personagem\n")

    def process_card_agenda(self, names_cards,save_folder):
        print("============== CARTA AGENDA =======================")
        for card in names_cards:
            # =============== PEGANDO O NOME DA CARTA==================
            text = self.driver.execute_script("return arguments[0].firstChild.textContent;", card).strip().upper()
            card.click()
            time.sleep(2)
            # =============== PEGANDO EFEITO ===================
            card_effect = self.driver.find_element(By.XPATH, "//div[@id='viewDiv']")
            try:
                card_effect_text = self.driver.execute_script("return arguments[0].lastChild.textContent;", card_effect).strip()
            except:
                card_effect_text = "Não tem efeito"
            # =============== RESULTADO ===================

            print(f"\n\n======== Resultado ========\nNome: {str(text).upper()}, \nEfeito: {str(card_effect_text).upper()}\nCasa :'Baratheon',\nTipo de carta: Agenda\n")
