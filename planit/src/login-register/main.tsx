import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App'; // importa o componente App
import './index.css';    // importa os estilos globais (opcional)

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
