
# Site_Yanes -> App Desktop (Tkinter) com Firebase

Este projeto converte as telas `admin.html`, `cadastro_produto.html`, `cadastro_usuario.html` para um app desktop em Python/Tkinter e integra com Firebase (Firestore + Auth).

## Pré-requisitos

1. Python 3.10+ (recomendado).
2. Um projeto Firebase com Firestore e Authentication (Email/Password) ativados.
3. Web API Key (API_KEY) do Firebase:
   - Console Firebase > Project settings > Web API Key.
4. Service Account JSON:
   - Console Firebase > Project Settings > Service accounts > Generate new private key.
   - Baixe e salve como `serviceAccountKey.json` na raiz do projeto (ou ajuste `config.json`).

## Instalação

1. Clone seu repo localmente (ou crie pasta):
   ```bash
   git clone https://github.com/JaoCruz17/site_yanes.git
   cd site_yanes
