from openai import OpenAI
from fpdf import FPDF
import os

client = OpenAI(api_key='sua_api_key')

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Resposta da Assistente Virtual", align="C", ln=True)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

dados = [
    {"role": "system", "content": "Você é uma assistente pessoal que responde diversas perguntas."}
]

def gerar_nome_arquivo(base='resposta', extensao='.pdf'):

    contador = 1
    nome_do_arquivo = f'{base}{extensao}'

    while os.path.exists(nome_do_arquivo):
        nome_do_arquivo = f"{base}_{contador}{extensao}"
        contador += 1

    return nome_do_arquivo

print('ASSISTENTE VIRTUAL \n DIGA -> sair <- PARA FINALIZAR A CONVERSA \n')

while True:

    pergunta = input('O que você quer saber? ')

    if pergunta.lower() in ['sair', 'finalizar']:
        print('Chat encerrado.')
        break

    dados.append({"role": "user", "content": pergunta})

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=dados
    )

    resposta = completion.choices[0].message.content

    dados.append({"role": "assistant", "content": resposta})

    print(f"Assistente: {resposta} \n")  

    pergunta_pdf = input('Deseja que eu gere um pdf com essa resposta? (Se sim, diga sim.) ')

    if pergunta_pdf == 'sim':
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=f'O usuário perguntou: {pergunta}. Eu respondi: {resposta}')
        nome_arquivo = gerar_nome_arquivo()
        pdf.output(nome_arquivo)
        print(f'pdf salvo como {nome_arquivo}! ')
