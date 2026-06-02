import time
import requests
import re
import os
import pyperclip
import undetected_chromedriver as uc
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def cria_post():

    #cria pasta para salvar as imagens 
    pasta = "Imagens"
    os.makedirs(pasta, exist_ok=True)


    link = "amazon.fr/"
    link_produto = pyautogui.prompt("Cole o link do produto aqui: ")

    if link in link_produto:
        

        # =========================================
        # CHROME
        # =========================================

        options = uc.ChromeOptions()

        options.add_argument(r"--user-data-dir=C:\ChromeBot")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = uc.Chrome(
            version_main=148,
            options=options,
            use_subprocess=True
        )

        wait = WebDriverWait(driver, 20)



        driver.get(link_produto)



        #pega o titulo do produto
        titulo = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "productTitle"))
        ).text.strip()


        #pega o primeiro número do dinheiro, depois o centavos e junta tudo 
        parte_inteira = driver.find_element(
            By.CSS_SELECTOR,
            ".a-price-whole"
        ).text.strip()

        parte_decimal = driver.find_element(
            By.CSS_SELECTOR,
            ".a-price-fraction"
        ).text.strip()

        preco = f"{parte_inteira},{parte_decimal} €"

        # CLICA NO BOTÃO
        driver.find_element(
            By.ID,
            "amzn-ss-get-link-button"
        ).click()

        # ESPERA O LINK APARECER
        link_afiliado = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.ID, "amzn-ss-text-shortlink-textarea")
            )
        ).get_attribute("value")


        # baixa a imagem
        imagem_url = driver.find_element(
            By.ID,
            "landingImage"
        ).get_attribute("data-old-hires")

        nome_arquivo = re.sub(r'[\\/*?:"<>|]', '', titulo)
        nome_arquivo = nome_arquivo.replace(" ", "_")
        nome_arquivo = nome_arquivo[:40] + ".jpg"

        response = requests.get(imagem_url, timeout=30)

        caminho_imagem = os.path.join("Imagens", nome_arquivo)

        with open(caminho_imagem, "wb") as f:
            f.write(response.content)





        promptIA = f"""
        Tu es un rédacteur spécialisé dans les bons plans Amazon.

        Crée un post X (Twitter) en français.

        Format obligatoire :

        [Accroche courte avec emoji]

        🔥 Nom du produit
        💰 Prix

        [1 ou 2 phrases courtes sur le principal avantage]

        [D'urgence ou appel à l'action]

        🛒 URL

        Règles :

        - Français naturel.
        - Ton vendeur et convivial.
        - Ne jamais inventer d'informations.
        - Phrases courtes.
        - Utiliser peu d'emojis.
        - Retourner uniquement le texte final.
        - L'URL doit être affichée en texte brut.

        IMPORTANT :

        - Longueur cible : 180 à 240 caractères.
        - Limite absolue : 280 caractères.
        - Si le texte dépasse 280 caractères, raccourcis-le automatiquement avant de répondre.
        - Privilégie toujours la concision.

        Données :

        Titre : {titulo}
        Prix : {preco}
        Lien : {link_afiliado}
        """




        print(f"\nTÍTULO: {titulo}")
        print(f"\nPREÇO: {preco}")
        print(f"\nLINK DE AFILIADO: {link_afiliado}")

        driver.execute_script("window.open('https://gemini.google.com', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])

        pyperclip.copy(promptIA)

        campo = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.ql-editor[contenteditable='true']")
            )
        )

        campo.click()
        campo.send_keys(Keys.CONTROL, "v")
        campo.send_keys(Keys.ENTER)


        time.sleep(15)

        botoes = driver.find_elements(
            By.CSS_SELECTOR,
            'mat-icon[fonticon="copy"]'
        )

        print("Botões encontrados:", len(botoes))

        botao_copiar = botoes[1]

        driver.execute_script(
            "arguments[0].click();",
            botao_copiar
        )

        time.sleep(1)

        tweet = pyperclip.paste()


        print(tweet+ "\n")

        #Twitter

        driver.execute_script("window.open('https://x.com/home', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])


        campo_tweet = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div[data-testid="tweetTextarea_0"]')
            )
        )

        campo_tweet.click()
        campo_tweet.send_keys(Keys.CONTROL, "v")


        upload = driver.find_element(
            By.CSS_SELECTOR,
            'input[data-testid="fileInput"]'
        )

        upload.send_keys(os.path.abspath(caminho_imagem))


        time.sleep(5)

        # publica
        botao_postar = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]')
            ))

        time.sleep(2)

        botao_postar.click()

        time.sleep(10)
        
        driver.quit()
    else:
        pyautogui.alert("O link inserido não é válido. Por favor, insira um link do Amazon.fr.")





def fazLogin():

    options = uc.ChromeOptions()

    options.add_argument(r"--user-data-dir=C:\ChromeBot")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(
        version_main=148,
        options=options,
        use_subprocess=True
    )

    driver.get("https://www.amazon.fr/")


    driver.execute_script("window.open('https://gemini.google.com', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.execute_script("window.open('https://x.com', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])

    input("enter")

    driver.quit()


login = pyautogui.confirm(text='Já fez login no amazon afiliados? fazer login para continuar', title='Verifica login', buttons=['SIM', 'Não Fiz Login'])

if login == 'SIM':
    cria_post()
else:
    fazLogin()

