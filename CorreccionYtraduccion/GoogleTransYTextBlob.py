import time

from textblob import TextBlob
from googletrans import Translator

num = 1

for i in range(220):
        with open(f"textosEspanol/texto ({i+num}).txt", "r") as f:
            text = f.read()
            textBlb = TextBlob(text)
            trasnlator = Translator()
            textING = trasnlator.translate(str(textBlb))
            print(f"Empezo espera de 20s del archivo {i + num}")
            time.sleep(20)
            print(f"Terminaron 20 segundos del archivo {i + num}")
            textBlb2 = TextBlob(str(textING.text))
            textCorrected = textBlb2.correct()
            del text
            del textING

        with open(f"textosIngles/texto ({i+num}).txt", "w", encoding="utf-8") as g:
            g.write(str(textCorrected))
            del textCorrected
            f.close()
            g.close()




