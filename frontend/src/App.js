import React from 'react';
import './App.css';
import TextAssistant from './components/TextAssistant';

function App() {
  return (
    <div className="App">
      <header className="App-header" style={{ padding: '1rem 0', backgroundColor: '#f0f4f8', borderBottom: '1px solid #ddd' }}>
        <h1 style={{ margin: 0, fontSize: '1.5rem', color: '#2a4365' }}>Asistente IA de Redacción</h1>
      </header>
      <main style={{ backgroundColor: '#f9fafb', minHeight: 'calc(100vh - 60px)' }}>
        <TextAssistant />
      </main>
      <footer style={{ padding: '1rem', textAlign: 'center', fontSize: '0.875rem', color: '#4a5568', backgroundColor: '#f0f4f8', borderTop: '1px solid #ddd' }}>
        &copy; {new Date().getFullYear()} - Asistente IA de Redacción con Llama 3.2
      </footer>
    </div>
  );
}

export default App;