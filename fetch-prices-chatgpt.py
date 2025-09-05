import os
import json
import requests
from datetime import datetime
from openai import OpenAI

# Sua API Key
OPENAI_API_KEY = "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"

def buscar_precos():
      client = OpenAI(api_key=OPENAI_API_KEY)

    # URLs para buscar
      urls = {
          'arabica': 'https://www.noticiasagricolas.com.br/cotacoes/cafe/indicador-cepea-esalq-cafe-arabica',
          'conillon': 'https://www.noticiasagricolas.com.br/cotacoes/cafe/indicador-cepea-esalq-cafe-conillon'
      }

    precos = {}

    for tipo, url in urls.items():
              try:
                            response = requests.get(url)
                            content = response.text[:5000]  # Limitar conteúdo

            prompt = f"Extraia APENAS o preço atual do café {tipo} em R$/saca desta página. Responda só o número: {content}"

            chat_response = client.chat.completions.create(
                              model="gpt-3.5-turbo",
                              messages=[{"role": "user", "content": prompt}],
                              max_tokens=20
            )

            preco_texto = chat_response.choices[0].message.content.strip()
            preco = float(preco_texto.replace(',', '.'))
            precos[tipo] = preco

        except:
            precos[tipo] = 2200.0 if tipo == 'arabica' else 1400.0

              # Criar JSON
              data = {
                  "last_update": datetime.now().isoformat(),
                        "cafe_arabica": precos.get('arabica', 2200.0),
                        "cafe_conillon": precos.get('conillon', 1400.0),
                        "cacau_bahia": 500.0
              }

    with open('prices.json', 'w') as f:
              json.dump(data, f, indent=2)

    print("Preços atualizados!")

if __name__ == "__main__":
      buscar_precos()
