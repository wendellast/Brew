import json
import re


def padronizar_json(json_entrada):
    if isinstance(json_entrada, (dict, list)):
        if isinstance(json_entrada, list):
            return [processar_questao(q) for q in json_entrada[:9]]
        else:
            return processar_questao(json_entrada)

    if isinstance(json_entrada, str):
        padrao = (
            r'\{\s*"texto"\s*:.*?"alternativas"\s*:\s*\[\s*(\{.*?\}\s*,?\s*)+\s*\]\s*\}'
        )
        matches = re.finditer(padrao, json_entrada, re.DOTALL)

        questoes = []
        for match in matches:
            json_str = match.group(0)
            try:
                questao = json.loads(json_str)
                questao_processada = processar_questao(questao)
                if questao_processada["texto"] and questao_processada["alternativas"]:
                    questoes.append(questao_processada)
                    if len(questoes) >= 9:
                        break
            except json.JSONDecodeError:
                continue

        if questoes:
            return questoes

    return {"texto": "", "alternativas": []}


def processar_questao(questao):
    questao_padrao = {"texto": "", "alternativas": []}

    if not isinstance(questao, dict):
        return questao_padrao

    if (
        "texto" in questao
        and isinstance(questao["texto"], str)
        and questao["texto"].strip()
    ):
        questao_padrao["texto"] = questao["texto"].strip()
    else:
        return questao_padrao

    alternativas_validas = []
    contagem_corretas = 0

    if "alternativas" in questao and isinstance(questao["alternativas"], list):
        for alternativa in questao["alternativas"]:
            if len(alternativas_validas) >= 4:
                break

            if not isinstance(alternativa, dict):
                continue

            alt_padrao = {}

            if (
                "texto" in alternativa
                and isinstance(alternativa["texto"], str)
                and alternativa["texto"].strip()
            ):
                alt_padrao["texto"] = alternativa["texto"].strip()
            else:
                continue

            if "correta" in alternativa:
                if isinstance(alternativa["correta"], bool):
                    eh_correta = alternativa["correta"]
                elif isinstance(alternativa["correta"], str):
                    eh_correta = alternativa["correta"].lower() in (
                        "true",
                        "yes",
                        "sim",
                        "1",
                    )
                elif isinstance(alternativa["correta"], (int, float)):
                    eh_correta = bool(alternativa["correta"])
                else:
                    continue

                alt_padrao["correta"] = eh_correta
                if eh_correta:
                    contagem_corretas += 1
            else:
                continue

            alternativas_validas.append(alt_padrao)

    if contagem_corretas > 1:
        return {"texto": "", "alternativas": []}

    questao_padrao["alternativas"] = alternativas_validas

    if not questao_padrao["alternativas"]:
        return {"texto": "", "alternativas": []}

    return questao_padrao
