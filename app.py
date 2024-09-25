from flask import Flask, request, jsonify, render_template
import pdfplumber
import os
from groq import Groq
import json

app = Flask(__name__)

# Inicializando o cliente da API Groq
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Função para converter o PDF em texto
def pdf_to_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Rota para servir a página HTML
@app.route("/")
def index():
    return render_template("index.html")

# Rota para processar o PDF
@app.route("/process_pdf", methods=["POST"])
def process_pdf():
    if "pdf" not in request.files:
        return jsonify({"error": "Nenhum PDF foi enviado."}), 400
    
    pdf_file = request.files["pdf"]
    
    # Converter o PDF para texto
    transcription = pdf_to_text(pdf_file)
    
    # Definir o prompt com a transcrição extraída
    messages = [
        {
            "role": "system",
            "content": """
              Você é um avaliador de cold calls. Você receberá uma transcrição de uma cold call realizada com um cliente e
              deverá retornar um feedback da conversa. Sua resposta deverá conter uma nota de 1 a 10, pontos positivos, pontos negativos
              e sugestões de melhoria. Nas sugestões de melhoria, forneça aspectos de vendas que o vendedor tenha que melhorar e inclua
              também conteúdos (artigos, vídeos, livros, etc.) sobre os tópicos que o vendedor deve melhorar.

              Leve em consideração aspectos de sucesso como o fechamento da venda ou agendamento de uma próxima reunião.

              Formate sua resposta como um dicionário Python. Não inclua mais nada além do dicionário:

              {
                "nota": "valor",
                "positivos": "ponto positivo",
                "negativos": "ponto negativo",
                "melhorias": "melhorias"
              }
              """
        },
        {
            "role": "user",
            "content": transcription
        }
    ]

    # Usar a API da Groq para gerar a análise
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
        max_tokens=1024
    )
    
    # Extraindo a resposta
    generated_text = chat_completion.choices[0].message.content
    print(generated_text)
    generated_text = json.loads(generated_text)
    
    return jsonify(generated_text)

if __name__ == "__main__":
    app.run(debug=True)
