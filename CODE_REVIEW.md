# Processo de Revisão de Código (Code Review)

Este documento define as diretrizes e o processo para a revisão de código no projeto PlanIt AI. O objetivo é garantir a qualidade, a manutenibilidade e a colaboração eficiente entre a equipe.

## Quem revisa?

Todo Pull Request (PR) ou Merge Request (MR) deve ser revisado por, no mínimo, **uma pessoa** da equipe. Para funcionalidades críticas ou alterações de grande impacto, recomenda-se a revisão por **duas pessoas**.

## Como escolher o revisor?

A escolha do revisor deve seguir uma abordagem mista:

1.  **Voluntariado e Especialidade**: Qualquer membro da equipe pode se voluntariar para revisar um PR. É incentivado que revisores com mais conhecimento na área do código (backend, frontend, etc.) se apresentem.
2.  **Rodízio e Delegação**: O autor do PR pode solicitar diretamente a revisão de um ou mais membros específicos. Para garantir que todos participem e compartilhem conhecimento, a equipe pode adotar um sistema de rodízio informal.
3.  **Revisão Cruzada**: É uma boa prática que um desenvolvedor de backend revise o trabalho de outro de backend, e o mesmo para o frontend, garantindo a especialidade na revisão.

## Quais critérios precisam ser verificados?

O revisor deve focar nos seguintes critérios, alinhados com o arquivo `CONTRIBUTING.md` e com os processos de automação:

-   **Funcionalidade**: A implementação resolve o problema ou a funcionalidade descrita na *issue* relacionada?
-   **Legibilidade e Clareza**: O código é fácil de entender? Nomes de variáveis, funções e classes são descritivos e claros?
-   **Testes**:
    -   O código novo está coberto por testes? (unitários, de integração, etc.).
    -   Os testes existentes continuam passando? O fluxo de CI/CD (`cicd.yml`) deve estar passando.
-   **Boas Práticas e Padrões**:
    -   O código segue os padrões de estilo e formatação do projeto (linting)?
    -   Foram utilizadas as melhores práticas para as tecnologias do projeto (Python/FastAPI e React/TypeScript)?
-   **Segurança**: A implementação introduz alguma vulnerabilidade de segurança (ex: injeção de SQL, XSS, senhas expostas)?
-   **Documentação**: O código está devidamente comentado, especialmente em partes complexas? A documentação externa (como o `README.md`) precisa ser atualizada?

## Que padrão de comentários usar?

Para manter um ambiente colaborativo e produtivo, siga estas diretrizes ao deixar comentários:

-   **Seja Respeitoso e Construtivo**: A crítica deve ser direcionada ao código, não ao autor. Use uma linguagem amigável e profissional.
-   **Seja Claro e Específico**: Em vez de dizer "isso está errado", explique *por que* está errado e, se possível, sugira uma alternativa melhor.
-   **Use Prefixo para Sugestões**: Para facilitar a identificação, use prefixos como `Sugestão:` ou `Dúvida:`.
-   **Equilibre Críticas com Elogios**: Se encontrar uma solução elegante ou um bom trabalho, elogie! Isso ajuda a manter a moral da equipe.
-   **Exemplo de um bom comentário**:
    > "Sugestão: percebi que esta função está fazendo duas coisas: buscando os dados e formatando-os. Que tal separá-la em duas funções menores para melhorar a clareza e facilitar os testes? Algo como `fetchUserData()` e `formatUserData()`."

## Quando um Pull Request (PR) / Merge Request (MR) pode ser aprovado?

Um PR/MR está pronto para ser mesclado na branch `developer` ou `main` quando os seguintes requisitos forem atendidos:

1.  **CI/CD Aprovado**: Todos os checks automatizados (testes, linting, build) devem passar com sucesso, conforme definido no arquivo `.github/workflows/cicd.yml`.
2.  **Revisão Aprovada**: O PR deve receber a aprovação de, no mínimo, **um revisor**.
3.  **Resolução de Comentários**: Todos os comentários e discussões levantados durante a revisão devem ser resolvidos. Se uma sugestão não for aplicada, o autor deve justificar o motivo.
4.  **Sem Conflitos de Merge**: O PR não deve ter conflitos com a branch de destino.
