import os
from typing import Tuple

import fitz
from gradio_client import Client
from services.default_json import padronizar_json


def analyze_pdf(
    pdf_path: str,
) -> Tuple[str, dict]:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"O arquivo PDF não foi encontrado: {pdf_path}")

    extracted_text = ""
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            extracted_text += page.get_text()
        doc.close()
    except Exception as e:
        raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")

    print(extracted_text)
    return extracted_text, {}


client = Client("wendellast/Quiz")

exemple_json = """
   
        {"texto": "string",
            "alternativas":
            [
                {"texto": "string",
                "correta": false
                },

                {"texto": "string",
                "correta": true
                }

                {"texto": "string",
                "correta": false
                }

                {"texto": "string",
                "correta": false
                }
        ]
        }
"""


async def bott(text, ask=exemple_json):
    prompt = f"""
    - Analise o texto abaixo e gere exatamente 9 perguntas sobre o conteúdo do texto.
    - Cada pergunta vai ter exatamente 4 alternativas e apenas uma delas será a correta.
    - a resposta correta deve ser marcada com o atributo "correta" como true.
    - As perguntas devem ser geradas no formato JSON.
    
    - Exemplo da resposta:
        {exemple_json}     
    - Texto:
        {text}
        
    - Retorne apenas o json com as perguntas e alternativas. 
    - Não inclua nada além do JSON com as perguntas e alternativas.
    - Não gere mais de 9 perguntas, e nem mais de 4 alternativas
"""

    result = client.predict(
        message=prompt,
        system_message="",
        max_tokens=712,
        temperature=0.7,
        top_p=0.95,
        api_name="/chat",
    )

    print(result)

    return result


async def generate_json_pdf(pdf_path):
    text, _ = analyze_pdf(pdf_path)
    result = await bott(text, ask=exemple_json)
    resul_perfect = padronizar_json(result)
    print(result)
    print("=-=" * 20)
    print(resul_perfect)
    return resul_perfect
