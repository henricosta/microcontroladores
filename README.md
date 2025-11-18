# Como executar o projeto

## Passo a Passo

### 1. Extrair Python Portable
Execute o arquivo `Portable Python-3.10.5 x64.exe` para extrair o Python Portable.

### 2. Iniciar o Console Python
Após a extração, navegue até a pasta criada `Portable Python-3.10.5 x64` e execute o arquivo `Console-Launcher.exe`. Isso abrirá uma janela de terminal.

### 3. Executar o Projeto
No terminal aberto, digite o seguinte comando:

```cmd
..\run.bat
```

Para executar o projeto em modo de simulação de leituras, adicione a flag `-test`:

```cmd
..\run.bat -test
```

### O que o Script Faz
- O arquivo `run.bat` irá automaticamente:
  - Instalar todas as dependências necessárias do projeto
  - Configurar o ambiente Python
  - Executar a aplicação principal

### 5. Acesse o localhost para visualizar as leituras
http://localhost:8080