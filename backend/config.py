# config.py
# Archivo de configuración para el Asistente IA de Redacción

# Configuración de Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"  # Asegúrate de que este modelo esté disponible en tu instancia de Ollama

# Parámetros del modelo para diferentes modos
MODEL_PARAMS = {
    "default": {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 2000,
    },
    "mejorar": {
        "temperature": 0.6,  # Menor temperatura para mayor precisión
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 2000,
    },
    "resumir": {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 1500,  # Respuestas más cortas para resúmenes
    },
    "traducir": {
        "temperature": 0.5,  # Temperatura baja para mayor precisión en traducciones
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 2000,
    },
    "continuar": {
        "temperature": 0.8,  # Mayor temperatura para más creatividad
        "top_p": 0.95,
        "top_k": 50,
        "max_tokens": 2500,  # Más tokens para generar continuaciones más largas
    }
}