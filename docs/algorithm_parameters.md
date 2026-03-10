# Parâmetros dos Algoritmos de Planejamento de Caminho

Este documento descreve os parâmetros importantes dos algoritmos de planejamento de caminho implementados neste projeto. Inclui os algoritmos testados na bateria de testes: **A\***, **Hybrid A\***, **Dijkstra**, **Lazy Theta\***, **D\* Lite**, **RRT**, **APF** (Artificial Potential Field) e **DWA** (Dynamic Window Approach).

---

## Índice

1. [A* (A-Star)](#1-a-a-star)
2. [Hybrid A*](#2-hybrid-a)
3. [Dijkstra](#3-dijkstra)
4. [Lazy Theta*](#4-lazy-theta)
5. [D* Lite](#5-d-lite)
6. [APF (Artificial Potential Field)](#6-apf-artificial-potential-field)
7. [DWA (Dynamic Window Approach)](#7-dwa-dynamic-window-approach)
8. [RRT (Rapidly-exploring Random Tree)](#8-rrt-rapidly-exploring-random-tree)
9. [Parâmetros Gerais do Sistema](#9-parâmetros-gerais-do-sistema)

---

## 1. A* (A-Star)

### Descrição
O algoritmo A* é um algoritmo de busca em grafo que encontra o caminho mais curto entre dois pontos usando uma função heurística. Nesta implementação, o A* não possui parâmetros específicos configuráveis, mas utiliza parâmetros gerais do sistema.

### Localização do Código
- **Implementação**: `src/core/path_planner/path_planner/src/graph_planner/astar_planner.cpp`
- **Cabeçalho**: `src/core/path_planner/path_planner/include/path_planner/graph_planner/astar_planner.h`

### Parâmetros Utilizados

O A* utiliza apenas os parâmetros gerais do path planner:

| Parâmetro | Localização | Valor Padrão | Descrição |
|-----------|-------------|--------------|-----------|
| `obstacle_inflation_factor` | `system_config.pb.txt` | `0.5` | Fator de inflação de obstáculos usado para verificação de colisão |

### Observações
- O A* usa movimentos em 8 direções (4 cardinais + 4 diagonais)
- A heurística utilizada é a distância euclidiana
- Pode ser configurado para funcionar como Dijkstra (`dijkstra=true`) ou GBFS (`gbfs=true`)

---

## 2. Hybrid A*

### Descrição
O Hybrid A* é uma extensão do A* que considera restrições de movimento do veículo (como raio mínimo de giro), gerando trajetórias suaves usando modelos de movimento Dubins ou Reeds-Shepp.

### Localização dos Parâmetros
- **Arquivo de Configuração**: `src/core/system_config/system_config/system_config.pb.txt` (linhas 12-30)
- **Definição Protobuf**: `src/core/system_config/system_config/path_planner_protos/graph_planner/hybrid_astar_planner.proto`
- **Implementação**: `src/core/path_planner/path_planner/src/graph_planner/hybrid_astar_planner/hybrid_astar_planner.cpp`

### Parâmetros

| Parâmetro | Tipo | Valor Padrão | Unidade | Descrição |
|-----------|------|--------------|---------|-----------|
| `motion_model` | `enum` | `DUBINS_UNSPECIFIED` | - | Modelo de movimento: `DUBINS_UNSPECIFIED` (0) ou `REEDS_SHEPP` (1) |
| `goal_tolerance` | `double` | `0.125` | metros | Tolerância de distância ao objetivo |
| `dim_3_size` | `int64` | `64` | - | Dimensões auxiliares para busca (discretização angular) |
| `max_iterations` | `int64` | `1000000` | - | Número máximo de iterações durante a expansão da busca |
| `max_approach_iterations` | `int64` | `1000` | - | Número máximo de iterações durante a busca próxima ao objetivo |
| `traverse_unknown` | `bool` | `false` | - | Permitir busca em espaço desconhecido (útil para navegação durante mapeamento) |
| `curve_sample_ratio` | `double` | `0.15` | - | Razão de amostragem para geração de curvas |
| `minimum_turning_radius` | `double` | `0.4` | metros | Raio mínimo de giro do veículo |
| `non_straight_penalty` | `double` | `1.20` | - | Penalidade para movimentos não retilíneos (deve ser ≥ 1) |
| `change_penalty` | `double` | `0.0` | - | Penalidade para mudança de direção (deve ser ≥ 0) |
| `reverse_penalty` | `double` | `2.1` | - | Penalidade para movimento reverso (deve ser ≥ 1) |
| `retrospective_penalty` | `double` | `0.025` | - | Penalidade para preferir manobras posteriores antes de anteriores ao longo do caminho |
| `lookup_table_dim` | `int64` | `20` | - | Tamanho da janela de distância Dubins/Reeds-Shepp para cache [m] |
| `analytic_expansion_ratio` | `double` | `3.5` | - | Razão para tentar expansões analíticas durante a busca para abordagem final |
| `analytic_expansion_max_length` | `double` | `3.0` | metros | Comprimento máximo da expansão analítica a ser considerada válida |
| `lamda_h` | `double` | `2.5` | - | Peso da heurística (lambda) |
| `default_graph_size` | `int64` | `100000` | - | Tamanho padrão do grafo |

### Exemplo de Configuração

```protobuf
graph_planner {
    hybrid_astar_planner {
        motion_model: DUBINS_UNSPECIFIED
        goal_tolerance: 0.125
        dim_3_size: 64
        max_iterations: 1000000
        max_approach_iterations: 1000
        traverse_unknown: false
        curve_sample_ratio: 0.15
        minimum_turning_radius: 0.4
        non_straight_penalty: 1.20
        change_penalty: 0.0
        reverse_penalty: 2.1
        retrospective_penalty: 0.025
        lookup_table_dim: 20
        analytic_expansion_ratio: 3.5
        analytic_expansion_max_length: 3.0
        lamda_h: 2.5
        default_graph_size: 100000
    }
}
```

### Dicas de Ajuste
- **`minimum_turning_radius`**: Deve corresponder às características físicas do robô
- **`reverse_penalty`**: Valores maiores desencorajam movimento reverso
- **`max_iterations`**: Aumentar pode melhorar a qualidade do caminho, mas aumenta o tempo de cálculo
- **`dim_3_size`**: Controla a discretização angular. Valores maiores = mais precisão, mas mais custo computacional

---

## 3. Dijkstra

### Descrição
O algoritmo Dijkstra é uma variante do A* que não utiliza heurística (h=0), garantindo encontrar o caminho de menor custo, mas geralmente explorando mais nós.

### Localização do Código
- **Implementação**: Usa a mesma classe `AStarPathPlanner` com flag `dijkstra=true`
- **Código**: `src/core/path_planner/path_planner/src/graph_planner/astar_planner.cpp`

### Parâmetros Utilizados

O Dijkstra utiliza apenas os parâmetros gerais do path planner (mesmos do A*):

| Parâmetro | Localização | Valor Padrão | Descrição |
|-----------|-------------|--------------|-----------|
| `obstacle_inflation_factor` | `system_config.pb.txt` | `0.5` | Fator de inflação de obstáculos usado para verificação de colisão |

### Observações
- O Dijkstra é implementado como uma variante do A* (mesma classe, flag diferente)
- Não utiliza heurística, então sempre encontra o caminho ótimo, mas pode ser mais lento
- Usa movimentos em 8 direções (4 cardinais + 4 diagonais)

---

## 4. Lazy Theta*

### Descrição
O Lazy Theta* é uma variante do Theta* que verifica colisões de forma "preguiçosa" (lazy), melhorando a eficiência computacional.

### Localização do Código
- **Implementação**: `src/core/path_planner/path_planner/src/graph_planner/lazy_theta_star_planner.cpp`
- **Cabeçalho**: `src/core/path_planner/path_planner/include/path_planner/graph_planner/lazy_theta_star_planner.h`

### Parâmetros Utilizados

O Lazy Theta* utiliza apenas os parâmetros gerais do path planner:

| Parâmetro | Localização | Valor Padrão | Descrição |
|-----------|-------------|--------------|-----------|
| `obstacle_inflation_factor` | `system_config.pb.txt` | `0.5` | Fator de inflação de obstáculos usado para verificação de colisão |

### Observações
- Herda de `ThetaStarPathPlanner`
- Não possui parâmetros específicos configuráveis
- Verifica colisões de forma lazy (apenas quando necessário), melhorando performance

---

## 5. D* Lite

### Descrição
O D* Lite é um algoritmo de planejamento incremental que pode replanejar eficientemente quando o ambiente muda, sendo útil para navegação em ambientes dinâmicos.

### Localização do Código
- **Implementação**: `src/core/path_planner/path_planner/src/graph_planner/dstar_lite_planner.cpp`
- **Cabeçalho**: `src/core/path_planner/path_planner/include/path_planner/graph_planner/dstar_lite_planner.h`

### Parâmetros Utilizados

O D* Lite utiliza apenas os parâmetros gerais do path planner:

| Parâmetro | Localização | Valor Padrão | Descrição |
|-----------|-------------|--------------|-----------|
| `obstacle_inflation_factor` | `system_config.pb.txt` | `0.5` | Fator de inflação de obstáculos usado para verificação de colisão |

### Observações
- Não possui parâmetros específicos configuráveis
- Mantém uma janela local do costmap (tamanho fixo: 70 células = 3.5m / 0.05m resolução)
- Eficiente para replanejamento quando o ambiente muda

---

## 6. APF (Artificial Potential Field)

### Descrição
O algoritmo APF utiliza campos de potencial artificial para guiar o robô em direção ao objetivo (força atrativa) e afastá-lo de obstáculos (força repulsiva).

### Localização dos Parâmetros
- **Arquivo de Configuração**: `src/core/system_config/system_config/system_config.pb.txt` (linhas 150-157)
- **Definição Protobuf**: `src/core/system_config/system_config/controller_protos/apf_controller.proto`

### Parâmetros

| Parâmetro | Tipo | Valor Padrão | Unidade | Descrição |
|-----------|------|--------------|---------|-----------|
| `lookahead_time` | `double` | `1.0` | segundos | Tempo de lookahead para previsão da trajetória |
| `min_lookahead_dist` | `double` | `0.3` | metros | Distância mínima de lookahead |
| `max_lookahead_dist` | `double` | `0.9` | metros | Distância máxima de lookahead |
| `smooth_window` | `int64` | `5` | - | Janela de tempo para suavização da trajetória |
| `weight_attractive_force` | `double` | `1.0` | - | Fator de escala da força atrativa (atração ao objetivo) |
| `weight_repulsive_force` | `double` | `3.0` | - | **Repulsion Gain (krep)**: Fator de escala global da força repulsiva (repulsão de obstáculos) |

### Repulsion Gain (krep) Based on Distance

O **Repulsion Gain (krep)** no APF é calculado de forma **dinâmica baseada na distância** ao obstáculo, e depois multiplicado pelo ganho global `weight_repulsive_force`.

**Fórmula do krep baseado em distância:**
```cpp
k = (1.0 - 1.0 / dist) / (dist * dist)
```

Onde:
- `dist`: Distância normalizada ao obstáculo (0 = no obstáculo, 1 = longe do obstáculo)
- `k`: Ganho repulsivo calculado dinamicamente

**Força repulsiva final:**
```cpp
rep_force = k * grad_dist
net_force = weight_attractive_force * attr_force + 
            weight_repulsive_force * rep_force
```

**Características:**
- O ganho `k` é **inversamente proporcional ao quadrado da distância**
- Quando próximo ao obstáculo (`dist → 0`), `k → ∞` (força repulsiva muito alta)
- Quando longe do obstáculo (`dist → 1`), `k → 0` (força repulsiva baixa)
- O parâmetro `weight_repulsive_force` (padrão: **3.0**) multiplica toda a força repulsiva

**Recomendações:**
- **`weight_repulsive_force` baixo (1.0-2.0)**: Robô menos cauteloso, pode passar muito perto de obstáculos
- **`weight_repulsive_force` médio (3.0-5.0)**: Balance entre segurança e eficiência
- **`weight_repulsive_force` alto (>5.0)**: Robô muito cauteloso, pode ter dificuldade em passar por corredores estreitos

### Exemplo de Configuração

```protobuf
apf_controller {
    lookahead_time: 1.0
    min_lookahead_dist: 0.3
    max_lookahead_dist: 0.9
    smooth_window: 5
    weight_attractive_force: 1.0
    weight_repulsive_force: 3.0
}
```

### Dicas de Ajuste
- **`weight_repulsive_force`**: Aumentar este valor torna o robô mais cauteloso com obstáculos, mas pode causar oscilações
- **`weight_attractive_force`**: Controla a força de atração ao objetivo
- **`smooth_window`**: Valores maiores resultam em trajetórias mais suaves, mas podem aumentar a latência

---

## 7. DWA (Dynamic Window Approach)

### Descrição
O DWA é um algoritmo de planejamento local que seleciona velocidades seguras dentro de uma janela dinâmica, considerando as limitações de aceleração do robô.

### Localização dos Parâmetros
- **Arquivo de Configuração**: `src/core/controller/dwa_controller/cfg/DWAController.cfg`
- **Implementação**: `src/core/controller/dwa_controller/src/dwa.cpp`

### Parâmetros Específicos do DWA

| Parâmetro | Tipo | Valor Padrão | Unidade | Descrição |
|-----------|------|--------------|---------|-----------|
| `sim_time` | `double` | `1.7` | segundos | Tempo de simulação para rolar trajetórias |
| `sim_granularity` | `double` | `0.025` | metros | Granularidade para verificação de colisões ao longo da trajetória |
| `angular_sim_granularity` | `double` | `0.1` | radianos | Granularidade para verificação de colisões em rotações |
| `path_distance_bias` | `double` | `0.6` | - | Peso para a distância do caminho na função de custo |
| `goal_distance_bias` | `double` | `0.8` | - | Peso para a distância ao objetivo na função de custo |
| `occdist_scale` | `double` | `0.01` | - | Peso para a distância de obstáculos na função de custo |
| `twirling_scale` | `double` | `0.0` | - | Peso para penalizar mudanças no heading do robô |
| `stop_time_buffer` | `double` | `0.2` | segundos | Tempo que o robô deve parar antes de uma colisão para considerar a trajetória válida |
| `oscillation_reset_dist` | `double` | `0.05` | metros | Distância que o robô deve percorrer antes de resetar flags de oscilação |
| `oscillation_reset_angle` | `double` | `0.2` | radianos | Ângulo que o robô deve girar antes de resetar flags de oscilação |
| `forward_point_distance` | `double` | `0.325` | metros | Distância do centro do robô para colocar um ponto adicional de pontuação |
| `scaling_speed` | `double` | `0.25` | m/s | Valor absoluto da velocidade para começar a escalar o footprint do robô |
| `max_scaling_factor` | `double` | `0.2` | - | Fator máximo para escalar o footprint do robô |
| `vx_samples` | `int` | `3` | - | Número de amostras para explorar o espaço de velocidade x |
| `vy_samples` | `int` | `10` | - | Número de amostras para explorar o espaço de velocidade y |
| `vth_samples` | `int` | `20` | - | Número de amostras para explorar o espaço de velocidade angular (theta) |
| `use_dwa` | `bool` | `True` | - | Usar abordagem de janela dinâmica para restringir velocidades de amostragem |

### Parâmetros Genéricos do Local Planner

O DWA também utiliza parâmetros genéricos do local planner (definidos via `add_generic_localplanner_params`):

- `max_vel_trans`, `min_vel_trans`: Velocidades translacionais máxima e mínima
- `max_vel_x`, `min_vel_x`: Velocidades em x máxima e mínima
- `max_vel_y`, `min_vel_y`: Velocidades em y máxima e mínima
- `max_vel_theta`, `min_vel_theta`: Velocidades angulares máxima e mínima
- `acc_lim_x`, `acc_lim_y`, `acc_lim_theta`, `acc_lim_trans`: Limites de aceleração
- `xy_goal_tolerance`, `yaw_goal_tolerance`: Tolerâncias para alcançar o objetivo
- `prune_plan`: Se deve podar o plano
- `trans_stopped_vel`, `theta_stopped_vel`: Velocidades consideradas como paradas

### Dicas de Ajuste
- **`sim_time`**: Aumentar permite prever mais à frente, mas aumenta o tempo de cálculo
- **`path_distance_bias` vs `goal_distance_bias`**: Balancear entre seguir o caminho global e ir direto ao objetivo
- **`occdist_scale`**: Valores maiores tornam o robô mais cauteloso com obstáculos
- **`vx_samples`, `vth_samples`**: Mais amostras melhoram a qualidade, mas aumentam o tempo de cálculo

---

## 8. RRT (Rapidly-exploring Random Tree)

### Descrição
O RRT é um algoritmo de planejamento probabilístico que constrói uma árvore de exploração aleatória no espaço de configuração.

### Localização dos Parâmetros
- **Arquivo de Configuração**: `src/core/system_config/system_config/system_config.pb.txt` (linhas 33-38)
- **Definição Protobuf**: `src/core/system_config/system_config/path_planner_protos/sample_planner/sample_planner.proto`
- **Implementação**: `src/core/path_planner/path_planner/src/sample_planner/rrt_planner.cpp`

### Parâmetros

| Parâmetro | Tipo | Valor Padrão | Unidade | Descrição |
|-----------|------|--------------|---------|-----------|
| `sample_points` | `int64` | `1500` | - | Número de pontos aleatórios a serem amostrados |
| `sample_max_distance` | `double` | `30.0` | metros | Distância máxima entre pontos de amostra |
| `optimization_radius` | `double` | `20.0` | metros | Raio de otimização para melhorar o caminho |
| `optimization_sampe_probability` | `double` | `0.05` | - | **Goal Bias**: Probabilidade de amostrar diretamente o objetivo (0.0-1.0) |

### Goal Bias

O **Goal Bias** no RRT é controlado pelo parâmetro `optimization_sampe_probability` com valor padrão de **0.05 (5%)**.

**Como funciona:**
- A cada iteração, o algoritmo gera um número aleatório entre 0 e 1
- Se o número for **≤ 0.05** (5% das vezes), o algoritmo amostra diretamente o objetivo
- Caso contrário (95% das vezes), amostra um ponto aleatório no espaço de configuração

**Fórmula no código:**
```cpp
if (p(eng) > config_.sample_planner().optimization_sampe_probability()) {
    // Amostra ponto aleatório
} else {
    // Amostra o objetivo diretamente
}
```

**Recomendações:**
- **Valores baixos (0.01-0.05)**: Exploração mais ampla, pode demorar mais para convergir
- **Valores médios (0.1-0.2)**: Balance entre exploração e convergência
- **Valores altos (>0.3)**: Convergência mais rápida, mas pode ficar preso em mínimos locais

### Exemplo de Configuração

```protobuf
sample_planner {
    sample_points: 1500
    sample_max_distance: 30.0
    optimization_radius: 20.0
    optimization_sampe_probability: 0.05
}
```

### Parâmetros Adicionais Utilizados

O RRT também utiliza parâmetros gerais do path planner:

| Parâmetro | Valor Padrão | Descrição |
|-----------|--------------|-----------|
| `obstacle_inflation_factor` | `0.5` | Fator de inflação de obstáculos para verificação de colisão |

### Dicas de Ajuste
- **`sample_points`**: Aumentar melhora a probabilidade de encontrar um caminho, mas aumenta o tempo de cálculo
- **`sample_max_distance`**: Controla o tamanho dos passos da árvore. Valores menores resultam em exploração mais detalhada
- **`optimization_sampe_probability`**: Probabilidade de amostrar diretamente o objetivo. Valores maiores (0.1-0.2) podem acelerar a convergência
- **`optimization_radius`**: Usado por variantes do RRT (RRT*, Informed RRT) para otimização do caminho

---

## 9. Parâmetros Gerais do Sistema

### Parâmetros do Path Planner

Localizados em `src/core/system_config/system_config/system_config.pb.txt`:

| Parâmetro | Valor Padrão | Descrição |
|-----------|--------------|-----------|
| `obstacle_inflation_factor` | `0.5` | Fator de inflação de obstáculos (usado por todos os planners) |
| `convert_offset` | `0.0` | Offset de conversão |
| `default_tolerance` | `0.0` | Tolerância padrão |
| `expand_zone` | `true` | Expandir zona |
| `show_safety_corridor` | `false` | Mostrar corredor de segurança |
| `enable_resample` | `false` | Habilitar reamostragem |
| `resample_ratio` | `0.5` | Razão de reamostragem |
| `is_outline_map` | `true` | Se é mapa de contorno |

### Parâmetros do Controller Geral

Localizados em `src/core/system_config/system_config/system_config.pb.txt` (linhas 78-90):

| Parâmetro | Valor Padrão | Unidade | Descrição |
|-----------|--------------|---------|-----------|
| `control_frequency` | `10.0` | Hz | Frequência de controle |
| `goal_dist_tolerance` | `0.3` | metros | Tolerância de distância ao objetivo |
| `rotate_tolerance` | `0.5` | radianos | Tolerância de rotação |
| `max_linear_velocity` | `0.5` | m/s | Velocidade linear máxima |
| `min_linear_velocity` | `0.0` | m/s | Velocidade linear mínima |
| `max_linear_velocity_increment` | `0.5` | m/s | Incremento máximo de velocidade linear |
| `max_angular_velocity` | `1.5` | rad/s | Velocidade angular máxima |
| `min_angular_velocity` | `0.0` | rad/s | Velocidade angular mínima |
| `max_angular_velocity_increment` | `1.5` | rad/s | Incremento máximo de velocidade angular |

---

## Como Modificar os Parâmetros

### Para APF, RRT e Hybrid A*:
1. Edite o arquivo: `src/core/system_config/system_config/system_config.pb.txt`
2. Localize a seção correspondente:
   - `apf_controller` para APF
   - `sample_planner` para RRT
   - `graph_planner.hybrid_astar_planner` para Hybrid A*
3. Modifique os valores desejados
4. Recompile o projeto

### Para DWA:
1. Edite o arquivo: `src/core/controller/dwa_controller/cfg/DWAController.cfg`
2. Modifique os valores padrão nas linhas `gen.add(...)`
3. Recompile o projeto
4. **Alternativamente**: Use `dynamic_reconfigure` durante a execução:
   ```bash
   rosrun rqt_reconfigure rqt_reconfigure
   ```

### Para A*:
O A* não possui parâmetros específicos, mas você pode modificar:
- `obstacle_inflation_factor` em `system_config.pb.txt` para ajustar a sensibilidade a obstáculos

---

## Referências

- **A***: Implementação baseada em busca heurística
- **APF**: Campos de potencial artificial para navegação
- **DWA**: Dynamic Window Approach para planejamento local
- **RRT**: Rapidly-exploring Random Tree para planejamento probabilístico

---

## Notas Finais

- Todos os valores padrão são baseados na configuração atual do projeto
- Parâmetros podem variar dependendo do tipo de robô e ambiente
- Recomenda-se testar diferentes configurações para otimizar o desempenho
- Use ferramentas de visualização (RViz) para observar o efeito das mudanças

---

**Última atualização**: Baseado na análise do código-fonte do projeto

