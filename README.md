# 关键路口查找器 使用说明（README）

本项目提供了一个交互式工具，用于在无向路网中识别关键路口（割点），基于 Tarjan 算法。当移除某个路口后，网络的连通分量数增加时，该路口即为关键路口，反映出该路口对网络连通性的影响。

---

## 目录

1. [概述](#概述)
2. [环境要求](#环境要求)
3. [文件结构](#文件结构)
4. [函数说明](#函数说明)
   - [`validate_input`](#validate_input)
   - [`get_vertex_count`](#get_vertex_count)
   - [`get_edges`](#get_edges)
   - [`display_results`](#display_results)
   - [`find_critical_intersections`](#find_critical_intersections)
   - [`get_components_after_removal`](#get_components_after_removal)
   - [`check_graph`](#check_graph)
   - [`analyze_critical_intersections`](#analyze_critical_intersections)
5. [整体工作流程](#整体工作流程)
6. [离散数学知识](#离散数学知识)
7. [使用方法](#使用方法)

---

## 概述

关键路口查找器用于识别无向路网中的关键路口（割点），即移除该路口后会使网络分割成更多不连通的区域，揭示网络的脆弱性。核心算法采用 Tarjan 算法，时间复杂度为 O(V+E)，V 为顶点数，E 为边数。

## 环境要求

- Python 3.6 及以上
- 无需额外第三方库，仅使用内置数据结构和递归

## 文件结构

```
project/
├── main.py              # 程序入口，负责用户交互和流程控制
└── tarjan_algorithm.py  # 核心算法及辅助函数实现
```
## 整体工作流程

1. **启动**：`main.py` 欢迎用户。
2. **输入**：调用 `get_vertex_count` 获取路口数。
3. **建图**：调用 `get_edges` 构建邻接表。
4. **预检查**：调用 `check_graph` 分析基本属性。
5. **警告**：若图不连通，提示用户是否继续。
6. **分析**：调用 `analyze_critical_intersections` 查找并分析割点。
7. **输出**：调用 `display_results` 展示结果。
8. **循环或退出**：询问用户是否继续分析新网络。

---

## 离散数学知识

- **图论**：将路口和道路抽象为无向图。
- **割点（Articulation Point）**：移除后会增加连通分量数的顶点。
- **深度优先搜索（DFS）**：用于遍历图并计算 `disc` 和 `low` 值。
- **连通性**：判断图是否完全连通及识别孤立顶点。
- **递归与归纳**：DFS 的正确性依赖递归结构。

---

## 使用方法

1. 克隆仓库。
2. 安装 Python 3.6 及以上。
3. 在项目根目录运行：
   ```bash
   python main.py
   ```
4. 按提示输入路网信息并查看结果。

---

## 函数说明

### `validate_input(u, v, n, graph)`

- **作用**：校验边 `(u, v)` 是否有效。
- **参数**：
  - `u, v`：候选边的两个端点。
  - `n`：顶点总数。
  - `graph`：当前邻接表。
- **返回**：`(is_valid: bool, error_msg: str)`。

验证内容：
1. 顶点编号需在 `[0, n-1]` 范围内。
2. 禁止自环 (`u != v`)。
3. 禁止重复边。

---

### `get_vertex_count()`

- **作用**：提示用户输入路口数量。
- **流程**：
  1. 循环提示，直到输入正整数或输入 `'q'` 退出。
  2. 输入 `'q'` 返回 `None`，否则返回整数。

---

### `get_edges(n)`

- **作用**：提示用户输入道路连接，并构建邻接表。
- **参数**：
  - `n`：顶点总数。
- **流程**：
  1. 初始化 `graph = [[] for _ in range(n)]`。
  2. 循环读取 `(u, v)`，直到输入 `-1 -1`。
  3. 使用 `validate_input` 校验边。
  4. 对有效边，分别加入 `graph[u]` 和 `graph[v]`。
  5. 返回构建完成的 `graph`。

---

### `display_results(n, graph_info, cut_vertices, analysis)`

- **作用**：以可读格式输出分析结果。
- **参数**：
  - `n`：顶点数量。
  - `graph_info`：图的基本属性字典，包含：
    - `edge_count`：道路总数。
    - `is_connected`：是否连通。
    - `isolated_vertices`：孤立路口列表。
  - `cut_vertices`：关键路口列表。
  - `analysis`：每个关键路口移除后分量列表的映射。

---

### `find_critical_intersections(graph)`

- **作用**：使用 Tarjan 算法查找无向图中的割点。
- **参数**：
  - `graph`：邻接表。
- **返回**：关键路口列表。

**主要步骤**：
1. 初始化 `visited`, `disc`（发现时间）, `low`（可回溯最早发现时间）, `parent`, `is_cut_vertex` 数组。
2. 对每个未访问顶点执行 DFS：
   - 设置发现时间和 low 值。
   - 对每个邻居递归 DFS，更新 `low[u]`。
   - 根节点有 ≥2 个子节点时为割点；非根节点若 `low[v] >= disc[u]` 则为割点。
3. 收集所有标记为割点的顶点。

---

### `get_components_after_removal(graph, removed_vertex)`

- **作用**：计算移除指定顶点后图的连通分量。
- **参数**：
  - `graph`：原始邻接表。
  - `removed_vertex`：待移除顶点。
- **流程**：
  1. 将 `removed_vertex` 标记为已访问。
  2. 对每个未访问顶点执行 DFS，收集组件。
  3. 返回所有组件列表。

---

### `check_graph(graph)`

- **作用**：检查图的连通性和基本属性。
- **参数**：
  - `graph`：邻接表。
- **返回**：包含：
  - `edge_count`：边数。
  - `is_connected`：是否连通。
  - `isolated_vertices`：孤立顶点列表。

**步骤**：
1. 统计边数（度数和除以 2）。
2. 识别孤立顶点。
3. 对非孤立顶点执行 DFS，检测连通性。

---

### `analyze_critical_intersections(graph)`

- **作用**：高层封装，查找关键路口并分析其移除影响。
- **参数**：
  - `graph`：邻接表。
- **返回**：
  - `cut_vertices`：关键路口列表。
  - `analysis`：每个关键路口对应的分量列表。

---

