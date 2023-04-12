from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
import requests
import json
import base64
import re
from csv import writer

#### RESOLVE CAPTCHA ####

url = "https://zeus.sii.cl/cvc_cgi/stc/CViewCaptcha.cgi"

payload = "oper=0"
headers = {
  'Content-Type': 'text/html'
}

response = requests.request("POST", url, headers=headers, data=payload)

aux = json.loads(response.text)

base64_message = aux["txtCaptcha"]
base64_bytes = base64_message.encode('ascii')
message_bytes = base64.b64decode(base64_bytes)
message = message_bytes.decode('ascii')
captchaNumber = message[36:40]

#### END RESOLVE CAPTCHA ####

#### WEBSCRAPPING ####

print(" ")
print(Fore.YELLOW+"########################################################################################################################")
print("################################### CONSULTA DE SITUACIÓN TRIBUTARIA DE TERCEROS #######################################")
print("########################################################################################################################"+Style.RESET_ALL)
print(" ")

while True:
  rut = input(Fore.GREEN+"Inserte RUT sin puntos y con guión:"+Style.RESET_ALL+" "+Fore.LIGHTRED_EX)
  if not re.match("^[0-9]+-[0-9kK]{1}$", rut):
        print ("RUT NO VÁLIDO")
  if len(rut) < 9:
        print("LARGO DE RUT INCORRECTO")
  else:
        print(" ")
        print(Fore.YELLOW+"########################################################################################################################")
        print("################################################ OBTENIENDO INFORMACIÓN ################################################")
        print("########################################################################################################################"+Style.RESET_ALL)
        print(" ")
        rut = rut.split("-")

        url2 = "https://zeus.sii.cl/cvc_cgi/stc/getstc"

        pl = "ACEPTAR=Efectuar Consulta&DV="+rut[1]+"&OPC=NOR&PRG=STC&RUT="+rut[0]+"&txt_code="+captchaNumber+"&txt_captcha="+aux["txtCaptcha"]
        h2 = {
          'Content-Type': 'text/html'
        }

        r2 = requests.request("POST", url2, headers=h2, data=pl)

        html_content = r2.text

        soup = BeautifulSoup(html_content, "lxml")
        name = soup.select("#contenedor > div:nth-child(4)")[0].string
        rut = soup.select("#contenedor > div:nth-child(7)")[0].string
        fechaConsulta = soup.select("#contenedor > span:nth-child(10)")[0].contents[1].strip()
        iniActividades = soup.select("#contenedor > span:nth-child(12)")[0].string
        fechaIniActividades = soup.select("#contenedor > span:nth-child(14)")[0].string
        if iniActividades == "Contribuyente presenta Inicio de Actividades: NO":
          monedaExtranjera = soup.select("#contenedor > span:nth-child(14)")[0].string.strip()
          empresaMenorTamano = soup.select("#contenedor > span:nth-child(16)")[0].contents[2]

        elif iniActividades == "Contribuyente presenta Inicio de Actividades: SI":
          monedaExtranjera = soup.select("#contenedor > span:nth-child(16)")[0].string.strip()
          empresaMenorTamano = soup.select("#contenedor > span:nth-child(18)")[0].contents[2]

        #### END WEBSCRAPPING ####

        #### PRINTING ####
        print(" ")
        print("FECHA DE REALIZACIÓN DE LA CONSULTA                                    --> "+Style.BRIGHT+Fore.BLUE+fechaConsulta.replace("Fecha de realización de la consulta: ","")+Style.RESET_ALL)
        print("NOMBRE                                                                 --> "+Style.BRIGHT+Fore.GREEN+name+Style.RESET_ALL)
        print("RUT                                                                    --> "+Style.BRIGHT+Fore.BLUE+rut+Style.RESET_ALL)
        print("PRESENTA INICIO DE ACTIVIDADES                                         --> "+Style.BRIGHT+Fore.BLUE+iniActividades.replace("Contribuyente presenta Inicio de Actividades: ","")+Style.RESET_ALL)
        if iniActividades == "Contribuyente presenta Inicio de Actividades: SI":
          print("FECHA DE INICIO DE ACTIVIDADES                                         --> "+Style.BRIGHT+Fore.BLUE+fechaIniActividades.replace("Fecha de Inicio de Actividades: ","")+Style.RESET_ALL)
        print("AUTORIZADO PARA DECLARAR Y PAGAR SUS IMPUESTOS EN MONEDA EXTRANJERA    --> "+Style.BRIGHT+Fore.BLUE+monedaExtranjera.replace("Contribuyente autorizado para declarar y pagar sus impuestos en moneda extranjera: ","")+Style.RESET_ALL)
        print("ES EMPRESA DE MENOR TAMAÑO                                             --> "+Style.BRIGHT+Fore.BLUE+empresaMenorTamano.replace(": ","")+Style.RESET_ALL)
        print(" ")
        print(Fore.YELLOW+"#########################################################################################################################")
        print("############################################## PROCESO TERMINADO ########################################################")
        print("#########################################################################################################################"+Style.RESET_ALL)
        print(" ")
        #### END PRINTING ####     
        break
