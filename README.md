# OEE Real-Time Analytics Challenge

Este projeto implementa uma solução de Machine Learning de ponta a ponta para monitorização de eficiência industrial (OEE) em tempo real. O sistema processa sinais de sensores (vibração, energia, temperatura) para classificar o estado da máquina e detetar a produção de peças.

## Arquitetura e Decisões de Design

### 1. Estratégia de "Unfolding" (Janelamento de Treino)
Como os dados históricos são fornecidos em **intervalos** e a predição é **pontual**, é implementada uma técnica de desdobramento:
- **Labels de Estado:** Propagados de forma constante para cada segundo do intervalo.
- **Contagem de Peças:** Em vez de uma distribuição uniforme, é utilizada uma heurística baseada no sinal de `power_draw`. O sistema identifica os picos de queda de energia dentro do intervalo para marcar os timestamps exatos onde um ciclo de produção provavelmente terminou.

### 2. Gestão de Estado em Streaming
Para manter a latência abaixo dos 15ms (requisito de performance), é utilizada um **In-Memory Cache Manager** baseado em `collections.deque`. 
- Cada `series_id` possui a sua própria fila circular.
- Isso permite que a API receba um único ponto e recupere instantaneamente a janela histórica (N=30s) necessária para o cálculo das features estatísticas.

### 3. Pipeline de ML Dual
É utilizada uma abordagem de classificação dupla com **Random Forest**:
- **Modelo A:** Classificador multi-classe para Estado (Producing, Idle, Downtime).
- **Modelo B:** Detetor binário de eventos de conclusão de peça.

## 🛠️ Como Executar

### Via Docker 
1. Build da imagem:
   ```bash
   docker build -t oee-analytics .
