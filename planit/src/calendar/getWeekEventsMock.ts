// src/calendar/__mocks__/getWeekEventsMock.ts

export function getWeekEventsMock() {
  return Promise.resolve({
    events: [
      {
        id: 1,
        title: "Math Lecture",
        description: "Algebra and calculus topics.",
        start_time: "2025-07-21T09:00:00",
        end_time: "2025-07-21T10:30:00",
        location: "Room 101",
        type: "lecture"
      },
      {
        id: 2,
        title: "Project Meeting",
        description: "Weekly project sync.",
        start_time: "2025-07-22T14:00:00",
        end_time: "2025-07-22T15:00:00",
        location: "Zoom",
        type: "meeting"
      },
      {
        id: 3,
        title: "Exam Review",
        description: "Review for upcoming exam.",
        start_time: "2025-07-23T11:00:00",
        end_time: "2025-07-23T12:00:00",
        location: "Room 202",
        type: "review"
      }
    ]
  });
}