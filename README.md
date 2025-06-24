# pause-30min

Aplicativo simples que força pausas para movimentação a cada 30 minutos, bloqueando o uso do computador por 5 minutos. Ideal para quem passa muitas horas sentado e deseja cuidar da saúde enquanto trabalha ou estuda.

## 🧠 Por que usar?

Estudos científicos mostram que ficar mais de 30 minutos sem se movimentar pode aumentar o risco de doenças cardiovasculares, dores nas costas, e queda na produtividade. O **pause-30min** foi criado para ajudar você a manter uma rotina mais saudável com pausas obrigatórias ao longo do dia.

## 💡 Funcionalidades

- ⏰ **Pausas programadas:** A cada 30 minutos de uso, o aplicativo é acionado.
-  स्क्रीन **Bloqueio Restrito por 5 Minutos:** Uma tela preta em tela cheia cobre o monitor, exibindo um contador regressivo de 5 minutos. Durante este período, o uso do computador é efetivamente bloqueado para incentivar uma pausa real.
- ⚙️ **Configuração simples e leve:** Roda em segundo plano discretamente.
- 🚫 **Instância Única:** Impede que múltiplas cópias do aplicativo rodem ao mesmo tempo.
- 💻 **Desenvolvido para Windows:** Utiliza recursos do sistema para suas funcionalidades.

## 🚀 Como usar (Instalação Manual)

Este aplicativo foi pensado para ser simples e não requer um instalador complexo.

**Pré-requisitos:**
*   **Python para Windows:** Você precisará ter o Python instalado. Se não tiver, pode baixá-lo em [python.org](https://www.python.org/downloads/windows/). Durante a instalação do Python, marque a opção "Add Python to PATH". A biblioteca `tkinter` (usada para a tela de bloqueio) geralmente já vem inclusa nas instalações padrão do Python para Windows.

**Passos para usar:**

1.  **Baixe o arquivo:**
    *   Faça o download do arquivo `pause_30min.py` (ou `pause_30min.pyw`) deste repositório.

2.  **Prepare o arquivo (Recomendado para rodar em segundo plano sem janela de console):**
    *   Crie uma pasta no seu computador (ex: `C:\PauseApp`).
    *   Mova o arquivo baixado para dentro desta pasta.
    *   **Importante:** Renomeie o arquivo de `pause_30min.py` para `pause_30min.pyw` (o `w` no final é crucial para que ele execute sem abrir uma janela de console preta).

3.  **Crie um Atalho (para facilitar o início):**
    *   Clique com o botão direito no arquivo `pause_30min.pyw` dentro da pasta `C:\PauseApp` (ou onde você salvou).
    *   Selecione "Enviar para" > "Área de Trabalho (criar atalho)".
    *   Vá até a sua Área de Trabalho, encontre o atalho criado.
    *   **(Recomendado)** Clique com o botão direito no atalho, vá em "Propriedades".
        *   No campo "Destino", certifique-se de que o Python está sendo chamado com `pythonw.exe`. O caminho completo deve ser algo como:
            `"C:\Caminho\Completo\Para\Python\pythonw.exe" "C:\PauseApp\pause_30min.pyw"`
            (O caminho para `pythonw.exe` pode variar. Exemplos: `C:\Users\SeuNome\AppData\Local\Programs\Python\PythonXX\pythonw.exe` ou `C:\Program Files\PythonXX\pythonw.exe`. Se o caminho para `pythonw.exe` ou para o script contiver espaços, use aspas em volta de cada caminho, como mostrado).

4.  **Iniciando o Aplicativo:**
    *   Dê um duplo clique no atalho criado na sua Área de Trabalho (ou diretamente no arquivo `pause_30min.pyw`).
    *   O aplicativo começará a rodar em segundo plano. A cada 30 minutos, uma tela preta cobrirá seu monitor por 5 minutos, exibindo um contador. Após os 5 minutos, a tela desaparecerá e você poderá voltar a usar o computador.

5.  **Como Parar o Aplicativo:**
    *   Como ele roda em segundo plano e a tela de bloqueio impede interações, você precisará usar o Gerenciador de Tarefas para pará-lo se necessário (por exemplo, se precisar interromper o ciclo antes da hora):
        1.  Pressione `Ctrl + Shift + Esc` para abrir o Gerenciador de Tarefas. (Se a tela de bloqueio estiver ativa, você pode precisar usar `Ctrl + Alt + Del` e selecionar "Gerenciador de Tarefas").
        2.  Vá para a aba "Detalhes" (ou "Processos" em versões mais antigas do Windows).
        3.  Procure por um processo chamado `pythonw.exe` (ou `python.exe` se você executou o arquivo `.py`).
        4.  Selecione-o e clique em "Finalizar tarefa".

## 📝 Lembretes

*   Este aplicativo não possui uma interface gráfica para configurações. O intervalo de trabalho é fixo em 30 minutos, seguido por um bloqueio de 5 minutos.
*   **Para que ele inicie toda vez que você ligar o computador:** Você pode colocar o atalho criado (passo 3) na pasta de inicialização do Windows. Para abrir essa pasta, pressione `Win + R`, digite `shell:startup`, e pressione Enter. Cole o atalho lá.
*   **Importante:** O bloqueio de tela tenta ser restritivo, mas combinações de teclas do sistema como `Ctrl + Alt + Del` geralmente ainda permitirão acesso ao Gerenciador de Tarefas por questões de segurança do Windows. O objetivo é ser um forte lembrete e dificultar o retorno imediato ao trabalho.

## ⚙️ Código Fonte

O código é escrito em Python e utiliza as bibliotecas:
*   `time`: Para controlar os intervalos e contadores.
*   `ctypes`: Para interagir com funcionalidades do Windows (como ocultar console e criar mutex).
*   `threading`: Para rodar o timer principal e a interface de bloqueio em paralelo.
*   `sys`, `os`: Para funcionalidades de sistema.
*   `tkinter`: Para criar a interface gráfica da tela de bloqueio em tela cheia.