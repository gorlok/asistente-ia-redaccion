@echo off
echo Iniciando Asistente IA de Redaccion...

REM Verificar si Ollama está en ejecución
echo Verificando si Ollama esta en ejecucion...
curl -s http://localhost:11434/api/tags > nul
if %ERRORLEVEL% NEQ 0 (
    echo Ollama no esta en ejecucion. Intentando iniciar...
    start "" ollama serve
    echo Esperando a que Ollama se inicie...
    timeout /t 5
) else (
    echo Ollama ya esta en ejecucion.
)

REM Crear entorno virtual si no existe
if not exist venv\ (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Iniciar el servidor API
echo Iniciando el servidor API...
python run.py

pause