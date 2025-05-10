# Asistente IA de Redacción

Este proyecto consiste en una aplicación web que actúa como asistente para la redacción de textos utilizando Inteligencia Artificial. La aplicación consta de un componente frontend en React y una API backend en Python que se conecta a un servidor Ollama local para realizar tareas de procesamiento de texto usando el modelo Llama 3.3.

## Características

- **Mejora de textos**: Corrige errores gramaticales y mejora la claridad y fluidez.
- **Resumen de textos**: Condensa el contenido manteniendo los puntos clave.
- **Traducción**: Traduce el texto a varios idiomas.
- **Continuación de texto**: Genera contenido adicional manteniendo el estilo original.
- **Historial**: Guarda un registro de las interacciones previas.

## Requisitos previos

1. **Node.js y npm** - Para ejecutar la aplicación frontend.
2. **Python 3.7+** - Para la API backend.
3. **Ollama** - Instalado y configurado localmente.
4. **Modelo Llama 3.3** - Descargado en Ollama.

## Instalación

### 1. Configurar Ollama

Si aún no tienes Ollama instalado:

```bash
# Para Linux/MacOS
curl -fsSL https://ollama.com/install.sh | sh

# Para Windows
# Descargar el instalador desde https://ollama.com/download
```

Luego, descarga el modelo Llama 3.3:

```bash
ollama pull llama3.3
```

### 2. Configurar el Backend (API Python)

```bash
# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/MacOS:
source venv/bin/activate

# Instalar dependencias
pip install flask flask-cors requests

# Iniciar el servidor API
python app.py
```

### 3. Configurar el Frontend (React)

```bash
# Crear un nuevo proyecto React
npx create-react-app text-assistant

# Cambiar al directorio del proyecto
cd text-assistant

# Instalar las dependencias necesarias
npm install

# Copiar el componente TextAssistant.jsx a la carpeta src/components/
# Importar y usar el componente en App.js
```

## Estructura del proyecto

```
asistente-ia-redaccion/
│
├── backend/
│   ├── app.py              # API de Flask
│   └── requirements.txt    # Dependencias de Python
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   │   └── TextAssistant.jsx  # Componente principal
    │   ├── App.js
    │   └── ...
    ├── package.json
    └── ...
```

## Ejecución

1. **Iniciar Ollama**:
   ```bash
   ollama serve
   ```

2. **Iniciar el Backend**:
   ```bash
   cd backend
   python app.py
   ```
   El servidor API estará disponible en `http://localhost:5000`.

3. **Iniciar el Frontend**:
   ```bash
   cd frontend
   npm start
   ```
   La aplicación web estará disponible en `http://localhost:3000`.

## Personalización

### Ajuste de parámetros del modelo

Puedes modificar los parámetros del modelo en `app.py`:

```python
"options": {
    "temperature": 0.7,  # Controla la creatividad (valores más altos = más creatividad)
    "top_p": 0.9,        # Controla la diversidad de tokens
    "top_k": 40,         # Limita la selección a los k mejores tokens
    "max_tokens": 2000,  # Longitud máxima de la respuesta
}
```

### Agregar nuevos modos

Para agregar un nuevo modo de procesamiento de texto:

1. Actualiza la función `generate_prompt()` en `app.py`
2. Añade el nuevo modo a las opciones en el componente React

## Solución de problemas

### El backend no puede conectarse a Ollama

- Verifica que Ollama esté en ejecución: `ollama ps`
- Comprueba que el modelo está disponible: `ollama list`
- Asegúrate de que el URL de la API de Ollama es correcto en `app.py`

### Problemas de CORS

Si encuentras errores de CORS, asegúrate de que CORS esté correctamente configurado en el backend:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Esto debe estar presente en app.py
```

### Demoras en las respuestas

Las respuestas pueden tardar dependiendo de:
- El rendimiento de tu máquina
- La longitud del texto de entrada
- La configuración del modelo

Considera ajustar `max_tokens` o usar un modelo más pequeño si las respuestas son demasiado lentas.

## Notas adicionales

- Esta aplicación está diseñada para ejecutarse localmente y no incluye medidas de seguridad para un entorno de producción.
- El rendimiento dependerá significativamente del hardware donde se ejecute Ollama.