#!/bin/bash

echo "Iniciando Asistente IA de Redacción..."

# Verificar si Ollama está en ejecución
echo "Verificando si Ollama está en ejecución..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "Ollama no está en ejecución. Intentando iniciar..."
    ollama serve &
    echo "Esperando a que Ollama se inicie..."
    sleep 5
else
    echo "Ollama ya está en ejecución."
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r backend/requirements.txt

# Iniciar el servidor API
echo "Iniciando el servidor API..."
python backend/run.py