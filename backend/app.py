from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import logging
# Importar la configuración desde config.py
from config import OLLAMA_API_URL, MODEL_NAME, MODEL_PARAMS

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("api.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

def generate_prompt(text, mode, target_language=None):
    """
    Genera el prompt adecuado según el modo seleccionado
    """
    if mode == "mejorar":
        return f"""Mejora el siguiente texto, corrigiendo errores gramaticales, 
        mejorando la claridad, fluidez y coherencia, sin cambiar su significado original:
        
        {text}
        
        Texto mejorado:"""
        
    elif mode == "resumir":
        return f"""Resume el siguiente texto, manteniendo los puntos clave y 
        la información más importante:
        
        {text}
        
        Resumen:"""
        
    elif mode == "traducir":
        return f"""Traduce el siguiente texto al {target_language}, 
        manteniendo el tono y estilo original:
        
        {text}
        
        Traducción:"""
        
    elif mode == "continuar":
        return f"""Continúa el siguiente texto de manera coherente y natural, 
        manteniendo el mismo estilo y tono:
        
        {text}
        
        Continuación:"""
    
    return text  # Si no se especifica un modo válido, devolver el texto original

@app.route('/api/generate', methods=['POST'])
def generate_text():
    try:
        data = request.json
        text = data.get('text', '')
        mode = data.get('mode', 'mejorar')
        target_language = data.get('targetLanguage')
        
        if not text:
            return jsonify({"error": "No se proporcionó texto"}), 400
        
        # Generar el prompt adecuado según el modo
        prompt = generate_prompt(text, mode, target_language)
        
        # Obtener los parámetros del modelo para el modo actual
        model_params = MODEL_PARAMS.get(mode, MODEL_PARAMS["default"])
        
        # Configurar la solicitud a Ollama
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,  # No queremos streaming para esta aplicación
            "options": model_params
        }
        
        logger.info(f"Procesando solicitud en modo '{mode}' con {len(text)} caracteres")
        
        # Enviar solicitud a Ollama
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # Lanzar excepción si hay error HTTP
        
        result = response.json()
        generated_text = result.get('response', '')
        
        # Limpiar el texto generado (eliminar las instrucciones del prompt si están incluidas)
        # Esto puede necesitar ajustes según cómo responda el modelo
        if mode == "mejorar" and "Texto mejorado:" in generated_text:
            generated_text = generated_text.split("Texto mejorado:", 1)[1].strip()
        elif mode == "resumir" and "Resumen:" in generated_text:
            generated_text = generated_text.split("Resumen:", 1)[1].strip()
        elif mode == "traducir" and "Traducción:" in generated_text:
            generated_text = generated_text.split("Traducción:", 1)[1].strip()
        elif mode == "continuar" and "Continuación:" in generated_text:
            generated_text = generated_text.split("Continuación:", 1)[1].strip()
            
        logger.info(f"Texto generado correctamente con {len(generated_text)} caracteres")
        return jsonify({
            "generatedText": generated_text,
            "stats": {
                "inputLength": len(text),
                "outputLength": len(generated_text),
                "mode": mode
            }
        })
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al conectar con Ollama: {str(e)}")
        return jsonify({"error": f"Error al conectar con Ollama: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint simple para verificar si la API está funcionando
    """
    return jsonify({"status": "ok", "model": MODEL_NAME})

if __name__ == '__main__':
    # Determinar el puerto. Usar 5000 por defecto o el especificado por variable de entorno
    port = int(os.environ.get("PORT", 5000))
    
    # Iniciar el servidor en modo de desarrollo
    app.run(host='0.0.0.0', port=port, debug=True)