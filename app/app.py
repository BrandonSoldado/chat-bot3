from config import *


register_llm_provider("groq", ChatGroq)
chat = ChatGroq(temperature=1, groq_api_key="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", model_name="llama3-70b-8192")


prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente virtual que responde a preguntas sobre hongos"),
    ("human", "{text}")
])
#chain = prompt | chat
chain = chat
def chatbot(mensaje):
    global historial
    historial.append({"role": "user", "content": mensaje})
    #response = chain.invoke({"text": mensaje})
    response = chain.invoke(historial)
    return response.content




app = Flask(__name__)
@app.route("/webhook", methods=["POST"])
def webhook():
    message_body = request.form.get("Body")
    from_number = request.form.get("From")
    nombre = obtener_nombre_usuario(from_number)
    if message_body.lower() == "confirm":
        respuesta = mensaje_presentacion(nombre) 
    else:
        id_usuario = obtener_id_usuario(from_number)
        cargar_historial(nombre)
        agregar_preguntas_respuestas_al_historial(id_usuario)     
        respuesta = chatbot(message_body)  
        insertar_conversacion(message_body,respuesta,obtener_fecha_actual(),obtener_hora_actual(),id_usuario) 
    resp = MessagingResponse()
    resp.message(respuesta)
    print(message_body)
    print(respuesta)
    return str(resp)




if __name__ == "__main__":
    app.run(debug=True, port=5000)