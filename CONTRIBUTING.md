# PlanIt AI

# 🛠 Guia de Contribuição

Este documento descreve as regras e padrões para colaborar com este repositório. Siga essas orientações para garantir uma colaboração clara, eficiente e padronizada.

---

## 📌 Fluxo de Colaboração

1. **Abra uma issue antes de começar a trabalhar**
   - Descreva o problema ou funcionalidade.
   - Aguarde feedback ou aprovação para evitar retrabalho.
   - Use *labels* apropriadas: `bug`, `enhancement`, `discussion`, etc.

2. **Crie uma branch a partir da `developer`**
   - Nomeie a branch seguindo as convenções abaixo.
   - Faça *commits* pequenos e frequentes com mensagens claras.

3. **Abra um Pull Request (PR)**
   - Relacione a issue usando: `Closes #número-da-issue`
   - Descreva o que foi feito, por que e como testar.
   - Aguarde revisão antes de fazer *merge*.

---

## 🌱 Convenções de Nomes de Branches

Use o padrão: `tipo/id-curto-descritivo`

### Tipos de branch:
- `feature/` – nova funcionalidade
- `fix/` – correção de bug
- `chore/` – tarefas de manutenção
- `refactor/` – melhorias internas sem mudança de comportamento
- `docs/` – documentação

**Exemplos:**
- `feature/123-login-usuario`
- `fix/214-corrige-validacao-email`

---

## 📝 Padrão de Mensagens de Commit

Formato: `<tipo>: descrição breve e clara`

### Tipos válidos:
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` mudança em documentação
- `style:` formatação, sem mudança de lógica
- `refactor:` refatoração de código
- `test:` adição ou correção de testes
- `chore:` tarefas administrativas do projeto

**Exemplos:**
- `feat: adiciona autenticação via JWT`
- `fix: corrige bug no upload de arquivo`
- `refactor: melhora performance do modelo LLM`

---

## 🔍 Regras para Revisar Código

- Código precisa:
  - Ter testes cobrindo o comportamento principal, se aplicável
  - Ser claro, com nomes de variáveis e funções descritivos
  - Estar de acordo com os padrões de lint e formatação definidos

- O que revisar:
  - A funcionalidade proposta resolve o problema?
  - Está bem testado? Há casos não tratados?
  - Pode ser simplificado ou separado em partes menores?
  - Está seguindo as convenções de commit e branch?

---

## ✅ Requisitos para rodar o projeto com Vite

Antes de iniciar, certifique-se de que seu ambiente atende aos seguintes requisitos:

1. **Node.js**
   - Versão recomendada: `>= 18.0.0`
   - Verifique com: `node -v`

2. **Gerenciador de pacotes**
   - É necessário ter um dos seguintes instalados:
     - `npm` (vem com o Node.js) - recomendado
     - `yarn`
     - `pnpm`

## ⚙️ Configuração do Projeto Localmente

1. **Instalação**
   git clone https://github.com/CIN0136-2025-1-E8/planit-ai.git
   cd planit-ai\planit
   npm install

