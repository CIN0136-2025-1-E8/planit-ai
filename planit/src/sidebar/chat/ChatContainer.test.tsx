// import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ChatContainer from "./ChatContainer";

// Mock do ChatSection para focar só na lógica do ChatContainer
jest.mock("./ChatSection", () => (props: any) => (
  <div>
    <div data-testid="messages">
      {props.messages.map((msg: any) => (
        <div key={msg.id} data-testid={msg.role}>{msg.content}</div>
      ))}
    </div>
    <form onSubmit={props.handleSubmit}>
      <input
        value={props.input}
        onChange={e => props.setInput(e.target.value)}
        data-testid="chat-input"
      />
      <button type="submit" data-testid="send-btn">Enviar</button>
    </form>
    {props.isLoading && <div data-testid="loading">Carregando...</div>}
  </div>
));

describe("ChatContainer", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("busca e exibe o histórico do chat ao montar", async () => {
    const mockHistory = [
      { role: "user", text: "Oi" },
      { role: "model", text: "Olá!" },
    ];
    jest.spyOn(require("./api"), "fetchChatHistory").mockResolvedValueOnce(mockHistory);
    render(<ChatContainer />);
    await waitFor(() => {
      expect(screen.getByText("Oi")).toBeInTheDocument();
      expect(screen.getByText("Olá!")).toBeInTheDocument();
    });
  });

  it("mostra mensagem padrão se falhar ao buscar histórico", async () => {
    jest.spyOn(require("./api"), "fetchChatHistory").mockRejectedValueOnce(new Error("fail"));
    render(<ChatContainer />);
    await waitFor(() => {
      expect(screen.getByText(/Planit AI/)).toBeInTheDocument();
    });
  });

  it("envia uma mensagem e exibe a resposta do assistente", async () => {
    jest.spyOn(require("./api"), "fetchChatHistory").mockResolvedValueOnce([]);
    jest.spyOn(require("./api"), "sendMessageToBackend").mockResolvedValueOnce("Resposta da IA");
    render(<ChatContainer />);
    // Digita e envia mensagem
    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "Oi" } });
    fireEvent.click(screen.getByTestId("send-btn"));
    // Estado de carregando
    expect(screen.getByTestId("loading")).toBeInTheDocument();
    // Depois de enviar, a mensagem do usuário deve aparecer
    await waitFor(() => {
      expect(screen.getByText("Oi")).toBeInTheDocument();
    });
    // Depois da resposta do assistente, ambas devem estar presentes
    await waitFor(() => {
      expect(screen.getByText("Resposta da IA")).toBeInTheDocument();
    });
  });

  it("mostra mensagem de erro se o backend falhar", async () => {
    jest.spyOn(require("./api"), "fetchChatHistory").mockResolvedValueOnce([]);
    jest.spyOn(require("./api"), "sendMessageToBackend").mockRejectedValueOnce(new Error("fail"));
    render(<ChatContainer />);
    fireEvent.change(screen.getByTestId("chat-input"), { target: { value: "Oi" } });
    fireEvent.click(screen.getByTestId("send-btn"));
    await waitFor(() => {
      expect(screen.getByText(/problema ao processar/)).toBeInTheDocument();
    });
  });
});
