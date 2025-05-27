# Projeto Fiap 3
##### Nathan Novais - 360103
##### William Brandão - 360387
### Descrição do Projeto
Desenvolvemos um modelo de previsão de resultados de futebol focado no Manchester United. Utilizamos Vite no frontend e Flask no backend, ambos hospedados na Google Cloud Platform (GCP).

Para alimentar o sistema com dados reais, criamos uma base no BigQuery da GCP, utilizando um job automatizado que fazia requisições à API da api-sports.io. A partir disso, coletamos informações sobre partidas, estatísticas e elencos.

Com os dados armazenados e tratados, construímos um modelo de Random Forest com o objetivo de prever, a partir de informações prévias da rodada, a probabilidade de vitória, empate ou derrota do Manchester United.

### Links Úteis
- **Frontend:https://storage.googleapis.com/soccer-scout-fiap-3/index.html**
- **Backend: https://flask-service-494036280576.us-central1.run.app**

### Diagrama do Projeto

![fiap-3 drawio (1)](https://github.com/user-attachments/assets/249ce2a0-59ac-4018-b876-504ddcff1ad8)


#### Como iniciar a aplicação:

- **Backend:**

1. Vá para a pasta backend:
   ```
   bash
   cd backend
   ```
2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # (Linux/Mac) or .\venv\Scripts\activate (Windows)
   ```
4. Instale os requisitos:
   ```
   pip install -r requirements.txt
   ```
6. inicie o arquivo 'main.py' pelo Python:
   ```
   python main.py
   ```

- **Frontend:**
  
1. Vá para a pasta 'frontend'
     ```
     bash
     cd ../frontend
     ```
2. Realize a instalação e a execução do yarn
     ```
     yarn install
     yarn run dev
     ```

     
