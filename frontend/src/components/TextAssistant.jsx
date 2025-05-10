import { useState, useEffect } from 'react';

const TextAssistant = () => {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [mode, setMode] = useState('mejorar'); // Modos: mejorar, resumir, traducir, continuar
  const [history, setHistory] = useState([]);
  const [targetLanguage, setTargetLanguage] = useState('inglés');

  const languages = ['inglés', 'español', 'francés', 'alemán', 'italiano', 'portugués'];

  const handleSubmit = async () => {
    if (!inputText.trim()) {
      setErrorMessage('Por favor ingresa texto para procesar');
      return;
    }
    
    setIsLoading(true);
    setErrorMessage('');
    
    try {
      // En una implementación real, esto se conectaría a tu API de Python
      const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: inputText,
          mode: mode,
          targetLanguage: mode === 'traducir' ? targetLanguage : null
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      const result = await response.json();
      setOutputText(result.generatedText);
      
      // Guardar en historial
      const newHistoryItem = {
        id: Date.now(),
        input: inputText,
        output: result.generatedText,
        mode: mode,
        timestamp: new Date().toLocaleString()
      };
      
      setHistory(prev => [newHistoryItem, ...prev]);
      
    } catch (err) {
      setErrorMessage(`Error al procesar el texto: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
      .then(() => {
        // Podría mostrar un toast de confirmación en una implementación más completa
      })
      .catch(err => {
        setErrorMessage(`Error al copiar: ${err.message}`);
      });
  };

  // Muestra la entrada con estilo para diferenciar entre contenidos
  const renderHistoryItem = (item) => {
    return (
      <div key={item.id} className="mb-6 p-4 border rounded-lg bg-gray-50">
        <div className="flex justify-between mb-2">
          <span className="font-semibold text-gray-700">
            {item.mode === 'mejorar' && 'Texto mejorado'}
            {item.mode === 'resumir' && 'Resumen'}
            {item.mode === 'traducir' && `Traducción al ${targetLanguage}`}
            {item.mode === 'continuar' && 'Continuación'}
          </span>
          <span className="text-sm text-gray-500">{item.timestamp}</span>
        </div>
        
        <div className="mb-3 p-3 bg-white border rounded-md">
          <p className="text-sm text-gray-800">{item.input}</p>
        </div>
        
        <div className="p-3 bg-white border rounded-md">
          <p className="text-sm">{item.output}</p>
        </div>
        
        <div className="flex gap-2 mt-2 justify-end">
          <button 
            onClick={() => setInputText(item.output)}
            className="text-sm px-3 py-1 bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
          >
            Editar
          </button>
          <button 
            onClick={() => copyToClipboard(item.output)}
            className="text-sm px-3 py-1 bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
          >
            Copiar
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">
        Asistente IA de Redacción
      </h1>

      <div className="mb-8">
        <div className="mb-4">
          <label htmlFor="mode" className="block mb-2 font-medium text-gray-700">
            Modo:
          </label>
          <div className="flex flex-wrap gap-2">
            {['mejorar', 'resumir', 'traducir', 'continuar'].map((option) => (
              <button
                key={option}
                type="button"
                onClick={() => setMode(option)}
                className={`px-4 py-2 rounded-md text-sm font-medium ${
                  mode === option
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                }`}
              >
                {option.charAt(0).toUpperCase() + option.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {mode === 'traducir' && (
          <div className="mb-4">
            <label htmlFor="language" className="block mb-2 font-medium text-gray-700">
              Traducir a:
            </label>
            <select
              id="language"
              value={targetLanguage}
              onChange={(e) => setTargetLanguage(e.target.value)}
              className="w-full p-2 border rounded-md bg-white"
            >
              {languages.map((lang) => (
                <option key={lang} value={lang}>
                  {lang.charAt(0).toUpperCase() + lang.slice(1)}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="mb-4">
          <label htmlFor="inputText" className="block mb-2 font-medium text-gray-700">
            Texto:
          </label>
          <textarea
            id="inputText"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Escribe o pega tu texto aquí..."
            className="w-full p-3 border rounded-md h-40"
          />
        </div>

        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-500">
            {inputText.length} caracteres
          </span>
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className={`px-6 py-2 rounded-md text-white font-medium ${
              isLoading
                ? 'bg-blue-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            {isLoading ? 'Procesando...' : 'Procesar texto'}
          </button>
        </div>
      </div>

      {errorMessage && (
        <div className="mb-6 p-3 bg-red-100 text-red-700 rounded-md">
          {errorMessage}
        </div>
      )}

      {outputText && (
        <div className="mb-8 p-6 border rounded-lg bg-white shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Resultado</h2>
            <button
              onClick={() => copyToClipboard(outputText)}
              className="px-3 py-1 bg-gray-100 text-gray-700 rounded hover:bg-gray-200 text-sm"
            >
              Copiar al portapapeles
            </button>
          </div>
          <p className="whitespace-pre-wrap">{outputText}</p>
        </div>
      )}

      {history.length > 0 && (
        <div className="mt-8">
          <h2 className="text-xl font-semibold mb-4">Historial</h2>
          <div>
            {history.map(renderHistoryItem)}
          </div>
        </div>
      )}
    </div>
  );
};

export default TextAssistant;