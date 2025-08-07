## 📌 Descrição do Projeto
**Planit AI** é uma aplicação web inteligente focada na organização da rotina acadêmica. Através do envio de mensagens e documentos como ementas e horários de disciplinas, o sistema analisa automaticamente as informações e gera cronogramas personalizados para estudantes.

Combinando praticidade e inteligência artificial, o Planit AI ajuda alunos a planejarem seus estudos de forma **eficiente**, otimizando o tempo e melhorando a **produtividade** ao longo do semestre.

## ▶️ Executando o Projeto com Docker

### ⬇️ Clonando o Repositório

Primeiro, clone o repositório para a sua máquina local usando o seguinte comando:

    git clone https://github.com/CIN0136-2025-1-E8/planit-ai.git
    cd planit-ai

### ✅ Pré-requisitos

- Docker e Docker Compose, ou Podman e Podman Compose instalados. O comando `docker-compose` pode ser substituído por 
`podman-compose`.

### ⚙️ Configuração Inicial

Antes de iniciar os serviços, é crucial configurar as variáveis de ambiente.

1. **Crie o arquivo de ambiente:**

    Navegue até o diretório `server/` e faça uma cópia do arquivo `.env.example`:

        cp server/.env.example server/.env

2. **Defina a Chave da API do Google:**

    Abra o arquivo `server/.env` que você acabou de criar e insira sua chave da API do Google no campo `GOOGLE_API_KEY`.

        # server/.env
        DEBUG=True
        GOOGLE_API_KEY="SUA_CHAVE_DE_API_VAI_AQUI"
        DATABASE_URL=postgresql://testuser:testpassword@db/testdb
        #DATABASE_URL=postgresql://testuser:testpassword@localhost:5432/testdb
        POSTGRES_USER=testuser
        POSTGRES_PASSWORD=testpassword
        POSTGRES_DB=testdb

    ⚠️ **Importante:** O arquivo `.env` contém informações sensíveis e **NUNCA** deve ser enviado para o controle de 
    versão (ex: Git). Ele já está incluído no `.dockerignore` e no `.gitignore` para prevenir commits acidentais.

### 🚀 Executando os Serviços

Com a configuração concluída, você pode iniciar todos os contêineres (backend, frontend e banco de dados) de uma vez.

#### Iniciar todos os serviços

Para construir as imagens e iniciar os contêineres, execute o seguinte comando na raiz do projeto:

    docker-compose up --build

#### Executar em modo "daemon"

Para que os contêineres rodem em segundo plano (modo _daemon_), adicione a flag `-d`:

    docker-compose up --build -d

#### Visualizando os logs

Se os serviços estiverem rodando em modo _daemon_, você pode visualizar os logs em tempo real para depuração. Para ver 
os logs de todos os serviços, use:

    docker-compose logs -f

Para ver o log de um serviço específico (por exemplo, `backend`):

    docker-compose logs -f backend

#### Desligar os serviços

Para parar e remover os contêineres e redes criados, execute:

    docker-compose down

Para parar os serviços e **remover também os volumes** (como os dados do banco de dados), use a flag `-v`:

    docker-compose down -v

### ✨ Recarregamento Automático (Hot Reload)

Tanto o backend quanto o frontend estão configurados para recarregamento automático, agilizando o desenvolvimento 
através do espelhamento dos diretórios locais para dentro dos contêineres.

- **Backend:** O diretório local `./server/app` é montado dentro do contêiner. O servidor Uvicorn, configurado com a 
flag `--reload`, monitora este diretório e reinicia automaticamente a cada alteração no código.

- **Frontend:** De forma similar, o diretório local `./planit` é montado dentro do contêiner do frontend. O servidor de 
desenvolvimento do Vite monitora este diretório e, quando um arquivo é salvo, as mudanças são refletidas 
instantaneamente no navegador, sem a necessidade de recarregar a página manualmente.

### 🐞 Depurando o Backend Fora do Contêiner

Para uma depuração mais aprofundada do backend (usando breakpoints com um IDE, por exemplo), pode ser mais fácil 
executá-lo diretamente na sua máquina local, fora do contêiner.

Nesse cenário, o banco de dados e o frontend ainda rodarão via Docker. Siga estes passos:

1. **Altere a URL do Banco de Dados:**

    No arquivo `server/.env`, comente a linha `DATABASE_URL` que aponta para `db` e descomente a linha que aponta para 
    `localhost`. Isso fará com que sua aplicação local se conecte ao banco de dados que está rodando no contêiner.

        # server/.env
        
        # Comente esta linha:
        # DATABASE_URL=postgresql://testuser:testpassword@db/testdb
        
        # E descomente esta:
        DATABASE_URL=postgresql://testuser:testpassword@localhost:5432/testdb
        
2. **Inicie os outros serviços via Docker:**
    
   Execute o `docker-compose` para iniciar apenas o banco de dados (`db`) e o frontend.
    
        docker-compose up -d --build db frontend

3. **Configure o ambiente virtual e execute o backend localmente:**

    Navegue até a pasta do servidor, crie um ambiente virtual, ative-o e instale as dependências.

        # Navegue até a pasta do servidor
        cd server
        
        # Crie o ambiente virtual
        python -m venv .venv
        
        # Ative o ambiente virtual (Linux/macOS)
        source .venv/bin/activate
        
        # Ative o ambiente virtual (Windows)
        # .\.venv\Scripts\activate
        
        # Instale as dependências
        pip install -r requirements-dev.txt

Agora, você pode iniciar o servidor backend a partir do seu ambiente de desenvolvimento local (por exemplo, com o 
comando `uvicorn app.main:app`) e ele se conectará ao banco de dados no contêiner. Lembre-se de remover a flag 
`--reload` se estiver usando as ferramentas de depuração do seu IDE.

[Python 3.11](https://www.python.org/downloads/) é a versão mínima para este projeto.

## 👨‍💻 Equipe do Projeto
[Isabella Mendes](https://github.com/isabellamdsr)  
[Wilhyã Pedro](https://github.com/Wilhy-p)  
[Luan Romero](https://github.com/luanromerolcc)  
[Guimel Filipe](https://github.com/filipeguimel)  
[Leandro Junior](https://github.com/LeandroJrMarques)  
[Maia Ferreira](https://github.com/maia-cin)  
[Thiago Alves](https://github.com/ThAlvesM)  
[Denilson França](https://github.com/altinctrl)  
[Luiz Veloso](https://github.com/lm-veloso)  
