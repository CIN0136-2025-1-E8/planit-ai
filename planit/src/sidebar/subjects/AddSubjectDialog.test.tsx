import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import AddSubjectDialog from "./AddSubjectDialog";

// Helper para criar um arquivo mock
function createFile(name = "file.pdf", type = "application/pdf") {
  return new File(["dummy content"], name, { type });
}

describe("AddSubjectDialog", () => {
  it("renders dialog and submits with valid input", () => {
    const handleSubmit = jest.fn();
    render(
      <AddSubjectDialog open={true} onClose={() => {}} onSubmit={handleSubmit} />
    );

    // Fill in the text field
    fireEvent.change(screen.getByLabelText(/Nome\/Descrição da Matéria/i), {
      target: { value: "Matemática" },
    });

    // Simulate file input
    const file = createFile();
    const fileInput = screen.getByLabelText(/Escolher arquivo PDF/i);
    fireEvent.change(fileInput, { target: { files: [file] } });

    // Click the Adicionar button
    const addButton = screen.getByRole("button", { name: /Adicionar/i });
    fireEvent.click(addButton);

    // Assert that handleSubmit was called with correct arguments
    expect(handleSubmit).toHaveBeenCalledWith("Matemática", file);
  });

  it("does not submit if fields are empty", () => {
    const handleSubmit = jest.fn();
    render(
      <AddSubjectDialog open={true} onClose={() => {}} onSubmit={handleSubmit} />
    );
    const addButton = screen.getByRole("button", { name: /Adicionar/i });
    fireEvent.click(addButton);
    expect(handleSubmit).not.toHaveBeenCalled();
  });
});