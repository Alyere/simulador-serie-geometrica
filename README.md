[readme_simulador_de_s_ries_geom_tricas.md](https://github.com/user-attachments/files/35464798/readme_simulador_de_s_ries_geom_tricas.md)
# Simulador de Séries Geométricas — Cálculo II (Grupo 6)

Aplicação web interativa desenvolvida para a disciplina de **Cálculo Diferencial e Integral II** (Centro Universitário UNIESP), com foco na modelagem matemática do **crescimento do armazenamento de dados** em servidores de backup por meio de séries geométricas.

---

## Sobre o Projeto

Em ambientes de infraestrutura e Ciência da Computação, rotinas de backup sucessivas podem estabilizar em um limite finito de espaço ou crescer de forma descontrolada até esgotar o disco. Este simulador permite analisar esse comportamento na prática, conectando a teoria de séries geométricas à análise de complexidade de algoritmos.

### Funcionalidades

- **Simulação interativa:** entrada personalizada para primeiro termo ($a_1$), razão ($r$), número de etapas ($n$) e unidade de medida (como GB, MB ou operações).
- **Dupla validação no Back-End:** cálculo pela **fórmula fechada** em tempo constante $O(1)$ comparado lado a lado com a **soma iterativa** (`math.fsum`) em $O(n)$, com tratamento para o caso especial $r = 1$ ($S_n = n \cdot a_1$).
- **Teste automático de convergência:** verifica o critério $|r| < 1$ e calcula o limite infinito $S_\infty = \frac{a_1}{1 - r}$ e a margem restante até o teto ($\Delta = S_\infty - S_n$).
- **Cenários pré-configurados:** alternância rápida entre convergência rápida, convergência lenta e explosão divergente.
- **Visualização gráfica:** gráfico interativo comparando volume por etapa ($a_k$), soma acumulada ($S_k$) e teto assintótico ($S_\infty$).
- **Exportação de dados:** geração de arquivo **CSV (Excel)** e cópia rápida do resumo numérico para relatórios.

---

## Cenário Oficial (Grupo 6)

Para a série de backups sucessivos:

$$S = 10 + 5 + 2{,}5 + 1{,}25 + \dots$$

Temos $a_1 = 10\text{ GB}$ e razão $r = \frac{5}{10} = 0{,}5$.

- **Soma dos 5 primeiros termos ($S_5$):**
  $$S_5 = \frac{10 \cdot (1 - 0{,}5^5)}{1 - 0{,}5} = 19{,}375\text{ GB}$$
- **Critério de convergência:** como $|r| = |0{,}5| < 1$, a série é **convergente**.
- **Soma infinita ($S_\infty$):**
  $$S_\infty = \frac{10}{1 - 0{,}5} = 20\text{ GB}$$
- **Interpretação:** mesmo realizando infinitas etapas de backup nessa taxa, o consumo total nunca ultrapassa $20\text{ GB}$. Em apenas 5 etapas, o sistema já atinge $96{,}88\%$ do teto (margem restante de $\Delta = 0{,}625\text{ GB}$).

### Cenários de Demonstração no Simulador

| Cenário | Parâmetros | Soma Parcial ($S_n$) | Teto Infinito ($S_\infty$) | Classificação |
| :--- | :--- | :--- | :--- | :--- |
| **1. Oficial Grupo 6 (Backups)** | $a_1 = 10$, $r = 0{,}5$, $n = 5$ | $19{,}3750\text{ GB}$ | $20{,}0000\text{ GB}$ | Convergente |
| **2. Convergência Lenta** | $a_1 = 10$, $r = 0{,}85$, $n = 15$ | $60{,}8431\text{ GB}$ | $66{,}6667\text{ GB}$ | Convergente |
| **3. Explosão / Divergente** | $a_1 = 10$, $r = 2{,}0$, $n = 6$ | $630{,}0000\text{ GB}$ | $\infty$ | Divergente |

---

## Relação com Análise de Algoritmos

- **$|r| < 1$ (Complexidade Linear $O(n)$):** em algoritmos de Divisão e Conquista como *Build-Heap* e *Quickselect*, o trabalho decresce geometricamente a cada nível ($n + \frac{n}{2} + \frac{n}{4} + \dots = 2n$), mantendo o custo limitado.
- **$|r| > 1$ (Explosão Exponencial $O(2^h)$):** em árvores de recursão sem otimização (como Fibonacci recursivo ingênuo), as chamadas dobram a cada nível ($1 + 2 + 4 + \dots + 2^h$), levando à divergência do custo computacional.
- **Alocação Dinâmica de Memória ($O(1)$ amortizado):** em estruturas que dobram de capacidade (`list` em Python e `ArrayList` em Java), o total de cópias até $n$ inserções segue $1 + 2 + 4 + \dots + n = 2n - 1$, garantindo custo médio constante por inserção.

---

## Tecnologias e Estrutura

- **Back-End:** Python 3 (somente biblioteca padrão — sem dependências externas)
- **Front-End:** HTML5, CSS3, JavaScript e Chart.js

```text
simulador-serie-geometrica/
├── simulador_serie_geometrica.py   # Servidor HTTP local e API JSON (/api/simular)
├── index.html                      # Interface web, gráficos interativos e exportação CSV
└── README.md                       # Documentação do projeto
```

---

## Como Executar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/Alyere/simulador-serie-geometrica.git
   cd simulador-serie-geometrica
   ```
2. Execute o servidor Python:
   ```bash
   python simulador_serie_geometrica.py
   ```
3. O simulador abrirá automaticamente no navegador em `http://localhost:8000`.

---

## Equipe — Grupo 6

- Maria Gabriele Gonçalves
- Alyere Targino
- Marcelo Filho
- Bruno de Araújo
- João Victor Camargo
- Victor Gadelha

---

## Referências

- STEWART, J. *Cálculo*, Vol. 2. Cengage Learning.
- ANTON, H.; BIVENS, I.; DAVIS, S. *Cálculo*, Vol. 2. Bookman.
- CORMEN, T. H. et al. *Algoritmos: Teoria e Prática*. Elsevier.
