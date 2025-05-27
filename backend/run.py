#!/usr/bin/env python3
"""
Script para iniciar y configurar el asistente IA de redacción
Este script verifica la instalación de Ollama, comprueba la disponibilidad del modelo
y lanza la API de backend.
"""

import os
import sys
import subprocess
import time
import requests
import logging
from config import MODEL_NAME, OLLAMA_API_URL

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_ollama_installed():
    """Verifica si Ollama está instalado en el sistema"""
    try:
        result = subprocess.run(['ollama', '-v'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
        if result.returncode == 0:
            logger.info(f"Ollama instalado: {result.stdout.strip()}")
            return True
        else:
            logger.error("Ollama no está instalado o no está en el PATH")
            return False
    except FileNotFoundError:
        logger.error("Ollama no está instalado o no está en el PATH")
        return False

def check_ollama_running():
    """Verifica si el servidor Ollama está en ejecución"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            logger.info("Servidor Ollama en ejecución")
            return True
        else:
            logger.error(f"Error al conectar con Ollama: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error("No se puede conectar al servidor Ollama. Asegúrate de que esté en ejecución.")
        return False

def check_model_available():
    """Verifica si el modelo especificado está disponible en Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            for model in models:
                if model.get('name') == MODEL_NAME:
                    logger.info(f"Modelo {MODEL_NAME} encontrado")
                    return True
            logger.error(f"Modelo {MODEL_NAME} no encontrado en Ollama")
            return False
        else:
            logger.error(f"Error al obtener la lista de modelos: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        logger.error("No se puede conectar al servidor Ollama")
        return False

def start_ollama_server():
    """Intenta iniciar el servidor Ollama"""
    logger.info("Intentando iniciar el servidor Ollama...")
    try:
        # Iniciar Ollama en un proceso separado
        process = subprocess.Popen(['ollama', 'serve'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Esperar a que el servidor se inicie
        for _ in range(10):  # Intentar 10 veces
            time.sleep(1)
            try:
                response = requests.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    logger.info("Servidor Ollama iniciado correctamente")
                    return True
            except requests.exceptions.ConnectionError:
                continue
        
        logger.error("No se pudo iniciar el servidor Ollama después de varios intentos")
        return False
    except Exception as e:
        logger.error(f"Error al iniciar Ollama: {str(e)}")
        return False

def pull_model():
    """Descarga el modelo especificado si no está disponible"""
    logger.info(f"Descargando modelo {MODEL_NAME}...")
    try:
        result = subprocess.run(['ollama', 'pull', MODEL_NAME], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
        if result.returncode == 0:
            logger.info(f"Modelo {MODEL_NAME} descargado correctamente")
            return True
        else:
            logger.error(f"Error al descargar el modelo: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error al descargar el modelo: {str(e)}")
        return False

def start_api_server():
    """Inicia el servidor API de Flask"""
    try:
        from app import app
        
        # Determinar el puerto
        port = int(os.environ.get("PORT", 5000))
        
        logger.info(f"Iniciando API en el puerto {port}...")
        # Iniciar el servidor Flask
        app.run(host='0.0.0.0', port=port, debug=True)
        return True
    except Exception as e:
        logger.error(f"Error al iniciar el servidor API: {str(e)}")
        return False

def main():
    """Función principal"""
    logger.info("Iniciando el asistente IA de redacción...")
    
    # Verificar si Ollama está instalado
    if not check_ollama_installed():
        logger.error("Por favor, instala Ollama antes de continuar: https://ollama.com/download")
        sys.exit(1)
    
    # Verificar si el servidor Ollama está en ejecución
    if not check_ollama_running():
        logger.info("Intentando iniciar el servidor Ollama...")
        if not start_ollama_server():
            logger.error("No se pudo iniciar el servidor Ollama. Por favor, inicia Ollama manualmente.")
            sys.exit(1)
    
    # Verificar si el modelo está disponible
    if not check_model_available():
        logger.info(f"El modelo {MODEL_NAME} no está disponible. Intentando descargarlo...")
        if not pull_model():
            logger.error(f"No se pudo descargar el modelo {MODEL_NAME}. Por favor, descárgalo manualmente con 'ollama pull {MODEL_NAME}'")
            sys.exit(1)
    
    # Iniciar el servidor API
    logger.info("Todo está configurado correctamente. Iniciando el servidor API...")
    start_api_server()

if __name__ == "__main__":
    main()