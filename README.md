# OportuniData

Busca vagas de tecnologia via Google Jobs (SerpAPI) com filtros avançados de área, linguagem, senioridade, modalidade e localização.

## Pré-requisitos

- Python 3.7+
- Conta gratuita na SerpAPI (até 100 buscas grátis/mês)

## Configuração

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd OportuniData
   ```
2. **Configure as variáveis de ambiente:**
   - Copie o arquivo de exemplo:
     ```bash
     cp .env.example .env
     ```
   - Abra o arquivo `.env` criado e insira sua chave da SerpAPI:
     ```env
     SERPAPI_KEY=sua_chave_aqui
     ```
   - Você pode obter sua chave gratuita em: https://serpapi.com/
   - **Nunca compartilhe sua chave em repositórios públicos.**
3. **Instale as dependências do projeto:**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Execute o aplicativo com:

```bash
streamlit run app.py
```

- Selecione os filtros desejados (área, linguagem, senioridade, modalidade, localização, palavra-chave).
- Clique em **Buscar Vagas**.
- Veja as vagas listadas e baixe o CSV, se desejar.

## Funcionalidades

- Busca vagas de tecnologia no Google Jobs via SerpAPI.
- Filtros por área de atuação, linguagem de programação, senioridade, modalidade de contratação, estado/cidade e palavra-chave.
- Sinônimos centralizados nos arquivos JSON para maior abrangência.
- Query booleana otimizada para resultados amplos.
- Paginação automática (até 3 páginas por busca).
- Interface moderna e responsiva com Streamlit.

## Variáveis de Ambiente (.env)

O arquivo `.env` armazena configurações sensíveis e **não deve ser versionado**. Para rodar o sistema, você precisa criar um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
SERPAPI_KEY=sua_chave_aqui
```

- Substitua `sua_chave_aqui` pela sua chave pessoal da SerpAPI.
- Nunca compartilhe sua chave em repositórios públicos.
- Use o arquivo `.env.example` como modelo.

## Licença

MIT
