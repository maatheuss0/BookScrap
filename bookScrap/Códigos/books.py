import time
from datetime import date
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.instagram.com/"

driver.get(url)
time.sleep(3)

"""

Rolagem pagina WEB

"""

scroll_pause_time = 2  # pausa no tempo do scroll para acompanhar o processo
screen_height = driver.execute_script("return window.screen.height;")  # pega o tamanho da pagina
i = 1
while True:
    # desce a pagina no tamanho de uma tela por vez
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # atualize a altura da rolagem sempre que rolar, pois a altura da rolagem pode mudar depois que rolamos a página
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # interrompa o loop quando a altura que precisamos rolar for maior que a altura total da rolagem
    if (screen_height) * i > scroll_height:
        break
"""

Login

"""

driver.find_element(By.NAME, "username").send_keys("mamaeubarco")
driver.find_element(By.NAME, "password").send_keys("passhard123")
driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
time.sleep(7)

"""

Caminho da paginá

"""

pesquisa = driver.find_elements(By.TAG_NAME,value='svg')[2]
pesquisa.click()
time.sleep(2)

driver.find_element(By.TAG_NAME, "input").send_keys("remama")
driver.find_element(By.TAG_NAME, "input").send_keys(Keys.ENTER)
time.sleep(2)

pesquisar = driver.find_elements(By.TAG_NAME, value="a")[0:15]
pesquisar[11].click()
time.sleep(5)

"""

Comeco raspagem de dados

"""

"""

Leitura das publicacoes, seguidores e seguindo

"""

indice = driver.find_elements(By.CLASS_NAME, value="html-span")[0:3]

indiceDicio = {"Data": date.today().strftime('%d/%m/%Y')
    , "Publicacoes": indice[0].text
    , "Seguidores": indice[1].text
    , "Seguindo": indice[2].text
               }
print(indiceDicio)

quantidade = int(indice[0].text)

"""

Leitura das curtidas e data das publicacoes

"""

publicacao = driver.find_elements(By.CLASS_NAME, value="_aagw")[0:quantidade]

curtidaLista = []
dataLista = []

for p in publicacao:

    p.click()
    time.sleep(3)

    curtida = driver.find_elements(By.CLASS_NAME, value="html-span")[3:]
    curtidaPublicacao=(len(curtida))

    data = driver.find_elements(By.CLASS_NAME, value="x1p4m5qa")[0].text

    for c in range(1, curtidaPublicacao):
        print(data, curtida[c].text)
        curtidaLista.append(curtida[c].text)
        dataLista.append(data)

    driver.back()
    time.sleep(2)

"""

Exportacao de dados para excel

"""

#indiceDicio = {"Data da publicacao": dataLista, "Número de curtidas": curtidaLista}
indiceDicio["Data da publicacao"] = dataLista
indiceDicio["Número de curtidas"] = curtidaLista

dfexel = pd.DataFrame(indiceDicio)

dfexel.to_excel("dados.xlsx", sheet_name="Dados REMAMA")
