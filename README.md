# 城市关键路口查找工具

## 项目简介
本项目用于在城市道路网络中查找关键路口（割点）。关键路口是指在其被移除后，会导致道路网络分割成多个连通分量的路口。这些路口对交通网络的连通性和鲁棒性至关重要。

项目主要由两个模块组成：
- `main.py`：程序入口，负责启动流程。
- `tarjan_algorithm.py`：实现图的输入、关键路口查找算法（基于 Tarjan 算法）。

---

## 环境要求
- Python 3.6 及以上
- 无需额外第三方库，使用标准库即可

---

## 工作流程
1. **启动程序**：`main.py` 调用 `tarjan_algorithm.py`。
2. **获取图结构**：`get_graph()` 与用户交互，读取顶点数和边的信息，构建邻接表。
3. **查找割点**：`find_critical_intersections(graph)` 对每个连通分量运行深度优先搜索，标记所有割点。
4. **结果输出**：根据算法结果，打印关键路口列表或提示网络冗余性良好。

---

## 函数说明

### `main.py`
- **`main()`**：程序入口，调用 `tarjan_algorithm.py`。
- **`if __name__ == "__main__"`**：确保脚本被直接运行时才执行主流程。

### `tarjan_algorithm.py`

#### `get_graph()`
- **功能**：与用户交互，获取图的顶点数和边列表，返回邻接表。
- **输入验证**：
  - 顶点数量为正整数。
  - 边的格式为 `u v`，索引在 `[0, n-1]` 范围内。
  - 禁止自环与重复边。
  - 输入 `-1 -1` 结束边输入。
- **返回值**：
  - `graph`：长度为 `n` 的列表，每个元素为该顶点的邻接顶点列表。
  - 若用户输入 `q` 退出，则返回 `None`。

#### `find_critical_intersections(graph)`
- **功能**：使用 Tarjan 算法查找无向图中的割点（关键路口）。
- **参数**：
  - `graph`：邻接表表示的无向图，格式为 `List[List[int]]`。
- **返回值**：
  - `List[int]`：所有割点的顶点索引列表。
- **实现思路**：
  1. 初始化：
     - `visited`：标记顶点是否被访问。
     - `disc`：记录顶点的发现时间。
     - `low`：记录顶点或其子孙通过回边能够访问到的最早发现时间。
     - `is_cut`：记录顶点是否为割点。
     - `time`：全局时间戳。
  2. 对每个未访问顶点执行 DFS：
     - 记录 `disc[u]` 和 `low[u]`。
     - 对每个邻居 `v`：
       - 若 `v` 未访问，递归 DFS，更新 `low[u] = min(low[u], low[v])`。
       - 若 `low[v] >= disc[u]` 且 `u` 不是根节点，则 `u` 为割点。
       - 根节点特殊处理：若根节点有超过一个子节点，则为割点。
       - 若 `v` 已访问且不是父节点，则更新 `low[u] = min(low[u], disc[v])`。
  3. 收集所有 `is_cut[u] == True` 的顶点索引。
---

## 核心算法流程（Tarjan 割点查找）
1. **初始化**：
   - `time = 0`
   - 所有顶点 `visited=False`, `disc=-1`, `low=-1`, `is_cut=False`
2. **DFS 递归**：对每个顶点 `u`：
   - `visited[u] = True`
   - `disc[u] = low[u] = time`, `time += 1`
   - `child_count = 0`
   - 遍历 `v` in `graph[u]`：
     - 若 `v` 未访问：
       - `child_count += 1`
       - 递归 `dfs(v, u)`
       - `low[u] = min(low[u], low[v])`
       - 若 `parent != -1 and low[v] >= disc[u]`，则 `u` 是割点。
     - 若 `v` 已访问且 `v != parent`：
       - `low[u] = min(low[u], disc[v])`
   - 根节点判断：若 `parent == -1 and child_count > 1`，则 `u` 是割点。
3. **输出结果**：收集并返回所有割点。
---

