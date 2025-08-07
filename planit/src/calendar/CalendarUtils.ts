import { getDay } from 'date-fns';

export const getInitialEvents = (weekStartDate: Date) => [
  { id: 1, name: 'CAD', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 0)), end: new Date(new Date(weekStartDate).setHours(12, 0, 0)), color: '#E69C5C', details: null, isLoading: false },
  { id: 2, name: 'IP', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 2)), end: new Date(new Date(weekStartDate).setHours(12, 0, 0)), color: '#D9D9D9', details: null, isLoading: false },
  { id: 3, name: 'Mat. Discreta', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 4)), end: new Date(new Date(weekStartDate).setHours(12, 0, 0)), color: '#8CB9E6', details: null, isLoading: false },
  { id: 4, name: 'Sistemas Digitais', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 1)), end: new Date(new Date(weekStartDate).setHours(15, 0, 0)), color: '#9DE68C', details: null, isLoading: false },
  { id: 5, name: 'Mat. Discreta', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 2)), end: new Date(new Date(weekStartDate).setHours(15, 0, 0)), color: '#8CB9E6', details: null, isLoading: false },
  { id: 6, name: 'Des. de Software', start: new Date(new Date(weekStartDate).setDate(weekStartDate.getDate() + 3)), end: new Date(new Date(weekStartDate).setHours(15, 0, 0)), color: '#E68C8C', details: null, isLoading: false },
];

export const dateToGridRow = (date: Date) => {
  const startHour = 8;
  const eventHour = date.getHours();
  const eventMinutes = date.getMinutes();
  const totalMinutesFromStart = (eventHour - startHour) * 60 + eventMinutes;
  return (totalMinutesFromStart / 30) + 2;
};

export const filterEventsByDay = (events: any[], dayIndex: number) => 
  events.filter(event => getDay(event.start) === (dayIndex + 1) % 7);