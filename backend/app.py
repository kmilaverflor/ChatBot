# Importación de bibliotecas necesarias
from flask import Flask, request, jsonify, render_template  # Flask para servidor web, templates y manejo de JSON
from openai import OpenAI  # Cliente para comunicarse con OpenRouter compatible con API estilo OpenAI
from flask_cors import CORS  # Para permitir solicitudes de diferentes dominios (Cross-Origin)

# Inicializa la aplicación Flask
app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Habilita CORS (para permitir llamadas desde frontend alojado en otro dominio/puerto)
CORS(app)

# Configura el cliente de OpenAI apuntando a OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # Dirección base de la API de OpenRouter
    api_key="api-key",  # API Key de OpenRouter (
)

# Ruta raíz que carga la página principal del chatbot
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # Retorna el archivo HTML con el frontend del chatbot

# Ruta para manejar las interacciones del usuario con el chatbot
@app.route("/chat", methods=["POST"])
def chat():
    # Extrae el mensaje del usuario desde el cuerpo de la solicitud (JSON)
    data = request.get_json()
    user_input = data["message"]

    # Diccionario de preguntas frecuentes (FAQ)
    FAQS = {
        "¿qué servicios ofrece inge lean s.a.s.?": "INGE LEAN S.A.S. ofrece soluciones en software, hardware, automatización industrial, inteligencia artificial y mantenimiento especializado.",
        "¿dónde se encuentra ubicada la empresa?": "Nuestra sede principal está en Pereira, Risaralda, Colombia.",
        "¿hacen desarrollo de software a la medida?": "Sí, desarrollamos soluciones de software personalizadas según las necesidades del cliente.",
        "¿ofrecen mantenimiento preventivo y correctivo?": "Así es, brindamos ambos tipos de mantenimiento para equipos industriales y sistemas tecnológicos.",
        "¿trabajan con automatización industrial?": "Sí, somos especialistas en automatización de procesos industriales para mejorar la eficiencia.",
        "¿tienen experiencia en inteligencia artificial?": "Claro, aplicamos inteligencia artificial en soluciones como análisis predictivo, visión computacional, entre otros.",
        "¿cómo puedo solicitar una cotización?": "Puedes escribirnos a través del formulario web o nuestro canal de WhatsApp y te responderemos en breve.",
        "¿atienden clientes fuera del eje cafetero?": "Sí, aunque estamos en el Eje Cafetero, también atendemos proyectos en otras regiones de Colombia.",
        "¿qué tipo de clientes atienden?": "Trabajamos con empresas industriales, comerciales e instituciones que requieren soluciones tecnológicas avanzadas.",
        "¿tienen soporte técnico después de entregar el proyecto?": "Sí, ofrecemos soporte técnico postventa para asegurar el funcionamiento óptimo de nuestras soluciones."
    }

    # Contexto que se envía al modelo para definir su comportamiento
    business_context = """
    Eres el asistente virtual de INGE LEAN S.A.S., una empresa de ingeniería con sede en Pereira, Colombia, fundada en 2013.
    La empresa ofrece soluciones personalizadas en software, hardware, automatización industrial, inteligencia artificial y mantenimiento.
    Tu objetivo es guiar a los clientes a las mejores soluciones tecnológicas que mejoren la eficiencia y competitividad de sus procesos industriales o comerciales.
    Puedes responder en inglés o español, dependiendo del idioma del usuario. Sé siempre claro, profesional y útil.

    You are the virtual assistant of INGE LEAN S.A.S., an engineering company based in Pereira, Colombia, founded in 2013.
    The company provides custom solutions in software, hardware, industrial automation, artificial intelligence, and maintenance.
    Your goal is to guide clients toward the best technology to improve their efficiency and competitiveness.
    You can respond in English or Spanish depending on the user's language.
    """

    # Primero verificamos si el mensaje del usuario coincide exactamente con una pregunta del FAQ
    if user_input in FAQS:
        return jsonify({"reply": FAQS[user_input]})  # Retorna la respuesta directamente sin usar el modelo

    # Si no está en el FAQ, se envía el mensaje al modelo de lenguaje Qwen
    try:
        response = client.chat.completions.create(
            model="qwen/qwen3-coder:free",  # Modelo gratuito compatible con OpenRouter
            messages=[
                {"role": "system", "content": business_context},  # Rol del sistema que define el comportamiento del asistente
                {"role": "user", "content": user_input}  # Mensaje del usuario
            ],
            max_tokens=500,  # Cantidad máxima de tokens de salida
            temperature=0.7  # Creatividad de las respuestas (entre 0 y 1)
        )

        # Extrae y retorna la respuesta del modelo
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        # En caso de error, muestra el mensaje en consola y retorna un error JSON
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

# Ejecuta la aplicación en modo desarrollo (debug)
if __name__ == "__main__":
    app.run(debug=True)
