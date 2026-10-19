import pandas
import pyautogui
import time

link= ("https://dlp.hashtagtreinamentos.com/python/intensivao/login")

pyautogui.PAUSE=(3)
pyautogui.press("win")
pyautogui.write("google")
pyautogui.press("enter")
pyautogui.write(link)
pyautogui.press("enter")
pyautogui.click(x=692, y=369)
pyautogui.write("arthur")   
pyautogui.press("tab")
pyautogui.write("arthur")
pyautogui.press("tab")
pyautogui.press("enter")

tabela=pandas.read_csv("c:/Users/Kids/Downloads/produtos (1).csv")
pyautogui.click(x=854, y=359)
pyautogui.click(x=745, y=256)
      
for linha in (tabela.index):
    pyautogui.click(x=745, y=256)
    codigo= tabela.loc[linha, "codigo"]
    pyautogui.write(codigo)
    pyautogui.press("tab")

    marca= tabela.loc[linha, "marca"]
    pyautogui.write(marca)
    pyautogui.press("tab")

    tipo= tabela.loc[linha, "tipo"]
    pyautogui.write(tipo)
    pyautogui.press("tab")

    categoria=str(tabela.loc[linha, "categoria"])
    pyautogui.write(categoria)
    pyautogui.press("tab")

    preco_unitario=str(tabela.loc[linha, "preco_unitario"])
    pyautogui.write(preco_unitario)
    pyautogui.press("tab")
        
    custo=str(tabela.loc[linha, "custo"])
    pyautogui.write(custo)
    pyautogui.press("tab")

    obs=str((tabela.loc[linha, "obs"]))
    pyautogui.write(obs)
    pyautogui.press("tab")
    pyautogui.press("enter")

    pyautogui.scroll(5000)  
    if linha == 4:
        break




        
    
    



