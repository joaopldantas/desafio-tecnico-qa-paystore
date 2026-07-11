from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import warnings
from pytest_html import extras

warnings.filterwarnings("ignore")

def test_linha_do_tempo(extra):
    opcoes = Options()
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1920,1080") 
    
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico, options=opcoes)
    
    extra.append(extras.html("<p><b>1:</b> Acessando o site Phoebus.</p>")) # pra evidenciar no relatório
    navegador.get("https://www.phoebus.com.br/")
    time.sleep(2)
    
    try: # percebi q o botao de cookie comprometia a tela
        botao_cookie = navegador.find_element(By.XPATH, "//button[contains(text(), 'Aceitar')]")
        botao_cookie.click()
        time.sleep(1)
        extra.append(extras.html("<p><b>2:</b> Banner de cookies fechado.</p>"))
    except:
        pass

    extra.append(extras.html("<p><b>3:</b> Clicando no menu HISTÓRIA.</p>"))
    botao_historia = navegador.find_element(By.XPATH, "//span[text()='HISTÓRIA']")
    botao_historia.click()
    
    time.sleep(5)
    
    navegador.execute_script("window.scrollBy(0, 200);") # scrollada pra caber todos os anos na tela
    time.sleep(1)
    extra.append(extras.html("<p><b>4:</b> Scroll na tela para enquadrar os elementos.</p>"))

    anos_teste = ["1997", "2000", "2022"]
    for ano in anos_teste:
        extra.append(extras.html(f"<br><b>Iniciando teste para o ano {ano}</b>"))
        botao_ano = navegador.find_element(By.XPATH, f"//button[@aria-label='{ano}']")
        botao_ano.click()
        time.sleep(2)
        extra.append(extras.html(f"<p>- Clicou no botão do ano {ano}.</p>"))
    
        titulo_elemento = navegador.find_element(By.XPATH, f"//span[contains(text(), '{ano} -')]")
        texto_visivel = titulo_elemento.text
    
        assert ano in texto_visivel, f"Falha: O texto '{texto_visivel}' não corresponde ao ano {ano}."
        extra.append(extras.html(f"<p style='color: green;'>- Sucesso: Título validado ('{texto_visivel}').</p>"))
    
        nome_print = f"evidencia_historia_{ano}.png"
        navegador.save_screenshot(nome_print)
        extra.append(extras.image(nome_print))

    extra.append(extras.html("<br><h3>Teste concluído com sucesso!</h3>"))
    navegador.quit()