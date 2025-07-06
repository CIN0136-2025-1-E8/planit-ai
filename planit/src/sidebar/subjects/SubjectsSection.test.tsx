import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import SubjectsSection from "./SubjectsSection";
import '@testing-library/jest-dom';

// Mock do AddSubjectDialog para evitar testar o componente interno aqui
jest.mock("./AddSubjectDialog", () => (props: any) => (
  props.open ? (
    <div data-testid="add-subject-dialog">
      <button onClick={() => props.onSubmit && props.onSubmit("Test Subject", new File(["dummy"], "file.pdf", { type: "application/pdf" }))}>
        Mock Add
      </button>
      <button onClick={props.onClose}>Close</button>
    </div>
  ) : null
));

describe("SubjectsSection", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders loading and then subjects", async () => {
    // Mock fetchSubjects
    global.fetch = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => [
        { id: "1", title: "Matemática", color: "#fff", files: [] },
        { id: "2", title: "Física", color: "#fff", files: [] },
      ],
    }) as any;

    render(<SubjectsSection />);
    expect(screen.getByText(/Carregando/i)).toBeInTheDocument();
    await waitFor(() => {
      expect(screen.getByText("Matemática")).toBeInTheDocument();
      expect(screen.getByText("Física")).toBeInTheDocument();
    });
  });

  it("opens dialog and adds a subject", async () => {
    // Mock fetchSubjects (initial load)
    global.fetch = jest.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    }) as any;
    // Mock addSubject
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: "3", title: "Test Subject", color: "#fff", files: [] }),
    });

    render(<SubjectsSection />);
    // Open dialog
    fireEvent.click(screen.getByRole("button", { name: /Nova Matéria/i }));
    // Click mock add button in dialog
    fireEvent.click(screen.getByText("Mock Add"));
    await waitFor(() => {
      expect(screen.getByText("Test Subject")).toBeInTheDocument();
    });
  });
});
