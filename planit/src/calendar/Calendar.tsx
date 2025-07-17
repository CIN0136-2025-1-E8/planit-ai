import React, { useState, useEffect } from 'react';
import { format, addDays, subDays, startOfWeek, endOfWeek, getDay } from 'date-fns';
import { ptBR } from 'date-fns/locale';

// --- ESTILOS CSS EMBUTIDOS ---
// Adicionei media queries para a responsividade
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

// --- COMPONENTES AUXILIARES ---
const ClockIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '8px', minWidth: '14px' }} >
    <circle cx="12" cy="12" r="10"></circle>
    <polyline points="12 6 12 12 16 14"></polyline>
  </svg>
);

// --- DADOS E LÓGICA DO CALENDÁRIO ---
// Dados iniciais dos eventos. Agora usam objetos Date.
const getInitialEvents = (weekStartDate) => [
    { id: 1, name: 'CAD', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 0)), end: new Date(new Date(weekStartDate).setHours(12,0,0)), color: '#E69C5C', details: null, isLoading: false },
    { id: 2, name: 'IP', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 2)), end: new Date(new Date(weekStartDate).setHours(12,0,0)), color: '#D9D9D9', details: null, isLoading: false },
    { id: 3, name: 'Mat. Discreta', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 4)), end: new Date(new Date(weekStartDate).setHours(12,0,0)), color: '#8CB9E6', details: null, isLoading: false },
    { id: 4, name: 'Sistemas Digitais', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 1)), end: new Date(new Date(weekStartDate).setHours(15,0,0)), color: '#9DE68C', details: null, isLoading: false },
    { id: 5, name: 'Mat. Discreta', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 2)), end: new Date(new Date(weekStartDate).setHours(15,0,0)), color: '#8CB9E6', details: null, isLoading: false },
    { id: 6, name: 'Des. de Software', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 3)), end: new Date(new Date(weekStartDate).setHours(15,0,0)), color: '#E68C8C', details: null, isLoading: false },
];

// Horários para exibir na lateral
const timeLabels = ['8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm'];
const weekDays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta'];

// --- COMPONENTE PRINCIPAL ---
const Schedule = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [events, setEvents] = useState(getInitialEvents(startOfWeek(currentDate, { weekStartsOn: 1 })));

  // Atualiza os eventos quando a semana muda
  useEffect(() => {
    const weekStart = startOfWeek(currentDate, { weekStartsOn: 1 });
    // Numa aplicação real, aqui faria uma chamada à API para buscar eventos desta semana.
    // Por agora, vamos apenas recriar os eventos de exemplo para a semana certa.
    // Esta lógica de exemplo é simplificada.
  }, [currentDate]);

  const handlePrevWeek = () => setCurrentDate(subDays(currentDate, 7));
  const handleNextWeek = () => setCurrentDate(addDays(currentDate, 7));

  // Função para simular a chamada à LLM
  const handleLoadSummary = (eventId) => {
    // 1. Ativa o estado de loading
    setEvents(prevEvents =>
      prevEvents.map(e => (e.id === eventId ? { ...e, isLoading: true } : e))
    );

    // 2. Simula uma chamada de API com 2 segundos de atraso
    setTimeout(() => {
      const summaryText = "Este é um resumo gerado pela LLM. O projeto CAD envolve a criação de modelos 3D para engenharia mecânica, utilizando técnicas avançadas de modelagem e simulação para otimizar o design de peças.";
      
      // 3. Atualiza o evento com o texto e desativa o loading
      setEvents(prevEvents =>
        prevEvents.map(e =>
          e.id === eventId ? { ...e, details: summaryText, isLoading: false } : e
        )
      );
    }, 2000);
  };

  // Converte a data/hora de um evento para uma linha da grelha
  const dateToGridRow = (date) => {
    const startHour = 8;
    const eventHour = date.getHours();
    const eventMinutes = date.getMinutes();
    const totalMinutesFromStart = (eventHour - startHour) * 60 + eventMinutes;
    // Cada linha representa 30 minutos. +1 porque a grelha começa na linha 2.
    return (totalMinutesFromStart / 30) + 2;
  };
  
  const weekStart = startOfWeek(currentDate, { weekStartsOn: 1 });
  const weekEnd = endOfWeek(currentDate, { weekStartsOn: 1 });
  const weekEventsByDay = weekDays.map((_, dayIndex) => 
    events.filter(event => getDay(event.start) === (dayIndex + 1) % 7)
  );

  return (
    <>
      <ScheduleStyles />
      <div className="schedule-wrapper">
        <header className="schedule-header">
          <h2>{`${format(weekStart, 'd MMM', { locale: ptBR })} - ${format(weekEnd, 'd MMM yyyy', { locale: ptBR })}`}</h2>
          <div className="nav-buttons">
            <button onClick={handlePrevWeek}>Anterior</button>
            <button onClick={handleNextWeek}>Próxima</button>
          </div>
        </header>

        {/* Vista Desktop */}
        <div className="schedule-container d-none d-md-grid">
          {weekDays.map((day, index) => (
            <div key={day} className="day-label" style={{ gridColumn: index + 2 }}>{day}</div>
          ))}
          
          {timeLabels.map((time, index) => (
            <React.Fragment key={time}>
              <div className="time-label" style={{ gridRow: index * 2 + 2 }}>{time}</div>
              {index < timeLabels.length && <div className="grid-line" style={{ gridRow: index * 2 + 3 }}></div>}
            </React.Fragment>
          ))}
          
          {events.map(event => {
            const dayOfWeek = getDay(event.start); // Domingo = 0, Segunda = 1 ...
            if (dayOfWeek === 0 || dayOfWeek === 6) return null; // Não mostrar no fim de semana
            
            return (
              <div
                key={event.id}
                className="event-item"
                style={{
                  gridColumn: dayOfWeek,
                  gridRow: `${dateToGridRow(event.start)} / ${dateToGridRow(event.end)}`,
                  backgroundColor: event.color,
                }}
              >
                <div className="event-header">
                  <ClockIcon />
                  <span>{event.name}</span>
                </div>
                {event.isLoading && <div className="event-details">A carregar resumo...</div>}
                {event.details && <div className="event-details">{event.details}</div>}
                {!event.details && !event.isLoading && (
                  <button onClick={() => handleLoadSummary(event.id)}>Carregar Resumo</button>
                )}
              </div>
            );
          })}
        </div>
        
        {/* Vista Mobile */}
        <div className="d-md-none">
          {weekDays.map((day, index) => (
            <div key={day} className="mobile-day-group">
              <h3 className="mobile-day-header">{day}</h3>
              {weekEventsByDay[index].length > 0 ? (
                weekEventsByDay[index].map(event => (
                  <div key={event.id} className="event-item" style={{ backgroundColor: event.color }}>
                     <div className="event-header">
                        <ClockIcon />
                        <span>{event.name} ({format(event.start, 'HH:mm')})</span>
                     </div>
                  </div>
                ))
              ) : (
                <p style={{color: '#6c757d', paddingLeft: '10px'}}>Sem eventos.</p>
              )}
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default Schedule;