const ScheduleStyles = () => (
  <style>{`
    /* Estilos Globais e Fundo */
    .schedule-background {
      display: flex;
      justify-content: center;
      align-items: flex-start; /* Alinhado ao topo para o header */
      min-height: 100vh;
      padding: 20px;
      background-color: #0c0c1e;
      background-image: radial-gradient(white, rgba(255, 255, 255, 0.2) 2px, transparent 40px),
        radial-gradient(white, rgba(255, 255, 255, 0.15) 1px, transparent 30px);
      background-size: 550px 550px, 350px 350px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      box-sizing: border-box;
    }
    
    .schedule-wrapper {
      width: 100%;
      max-width: 1400px;
      color: white;
    }

    /* Cabeçalho de Navegação */
    .schedule-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding: 10px;
      background-color: rgba(26, 26, 51, 0.5);
      border-radius: 12px;
      backdrop-filter: blur(5px);
    }
    .schedule-header h2 {
      margin: 0;
      font-size: 1.5rem;
      font-weight: 500;
    }
    .nav-buttons button {
      background: #2a2a6b;
      border: none;
      color: white;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 1rem;
      margin-left: 10px;
      transition: background-color 0.2s;
    }
    .nav-buttons button:hover {
      background: #3c3ca0;
    }

    /* Container Principal do Calendário (Desktop) */
    .schedule-container {
      display: grid;
      grid-template-columns: 60px repeat(5, 1fr); 
      grid-template-rows: auto repeat(18, 30px); /* Linha para dias da semana + 18 para horas */
      gap: 0 10px;
    }

    /* Dias da Semana (Desktop) */
    .day-label {
      text-align: center;
      padding-bottom: 10px;
      font-weight: 500;
      color: #a7a7d1;
      border-bottom: 1px solid #2a2a6b;
      margin-bottom: 5px;
    }

    /* Marcadores de Tempo */
    .time-label {
      grid-column: 1;
      color: #a7a7d1;
      font-size: 14px;
      text-align: right;
      padding-right: 10px;
      transform: translateY(-50%);
    }

    /* Linhas da Grelha */
    .grid-line {
      grid-column: 2 / -1;
      border-bottom: 1px solid #2a2a6b;
      transform: translateY(-1px);
    }
    
    /* Blocos de Evento */
    .event-item {
      display: flex;
      flex-direction: column; /* Alterado para empilhar conteúdo */
      padding: 12px;
      border-radius: 12px;
      color: #1a1a1a;
      font-weight: 500;
      overflow: hidden;
      margin: 1px;
      z-index: 10;
      transition: box-shadow 0.2s;
    }
    .event-item:hover {
      box-shadow: 0 0 15px rgba(255, 255, 255, 0.3);
    }
    .event-header {
      display: flex;
      align-items: center;
      margin-bottom: 8px; /* Espaço entre header e detalhes */
    }
    .event-details {
      font-size: 13px;
      font-weight: 400;
      line-height: 1.4;
      background: rgba(255, 255, 255, 0.3);
      padding: 8px;
      border-radius: 6px;
      margin-top: auto; /* Empurra para o fundo */
    }
    .event-item button {
        margin-top: 10px;
        padding: 6px 10px;
        border: none;
        background-color: rgba(0,0,0,0.2);
        color: white;
        border-radius: 5px;
        cursor: pointer;
    }
    .event-item button:hover {
        background-color: rgba(0,0,0,0.4);
    }

    /* Layout Responsivo para Mobile */
    @media (max-width: 768px) {
      .schedule-background {
        padding: 10px;
      }
      .schedule-header h2 {
        font-size: 1.1rem;
      }
      .schedule-container {
        display: block; /* Remove a grelha */
      }
      .day-label, .time-label, .grid-line {
        display: none; /* Esconde elementos da grelha desktop */
      }
      .mobile-day-group {
        margin-bottom: 20px;
      }
      .mobile-day-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #a7a7d1;
        padding-bottom: 8px;
        border-bottom: 2px solid #2a2a6b;
        margin-bottom: 12px;
      }
      .event-item {
        flex-direction: row; /* Lado a lado em mobile */
        align-items: center;
        margin-bottom: 10px;
        padding: 15px;
      }
      .event-header {
        margin-bottom: 0;
        flex-grow: 1;
      }
      .event-details, .event-item button {
        display: none; /* Opcional: esconder detalhes/botões na vista mobile inicial */
      }
    }
  `}</style>
);

export default ScheduleStyles;
