def get_graph():
    """
    简化的图输入函数:
    - 获取顶点数量和边信息
    - 构建邻接表表示的无向图
    """
    while True:
        try:
            n = input("\n请输入路口数量 (或输入'q'退出): ")
            if n.lower() == 'q':
                return None
            n = int(n)
            if n <= 0:
                print("路口数量必须是正整数！")
                continue
            break
        except ValueError:
            print("无效输入！请输入正整数。")
    
    # 初始化邻接表
    graph = [[] for _ in range(n)]
    
    print(f"\n请输入道路信息 (格式: u v，如 0 1)")
    print("输入 -1 -1 结束输入")
    
    edge_count = 0
    while True:
        try:
            raw = input(f"第{edge_count+1}条道路 (或 -1 -1 结束): ")
            if not raw.strip():
                print("输入不能为空！")
                continue
                
            u, v = map(int, raw.split())
            if u == -1 and v == -1:
                break
                
            # 验证输入
            if u < 0 or u >= n or v < 0 or v >= n:
                print(f"路口编号必须在 0 到 {n-1} 之间！")
                continue
            if u == v:
                print("不能添加自环！")
                continue
            if v in graph[u]:
                print(f"道路 {u} <--> {v} 已存在！")
                continue
                
            # 添加边 (无向图)
            graph[u].append(v)
            graph[v].append(u)
            edge_count += 1
            print(f"已添加: {u} <--> {v}")
        except ValueError:
            print("格式错误！请输入两个整数。")
    
    return graph

def find_critical_intersections(graph):
    """
    查找城市中的关键路口（割点）。
    输入: 邻接表表示的城市道路网络
    输出: 关键路口列表
    """
    n = len(graph)
    visited = [False] * n
    disc = [-1] * n     # 发现时间
    low = [-1] * n      # 最低可达时间
    is_cut = [False] * n
    time = [0]          # 使用列表实现可变时间计数器
    
    def dfs(u, parent=-1):
        # 访问当前顶点
        visited[u] = True
        disc[u] = low[u] = time[0]
        time[0] += 1
        child_count = 0
        
        # 探索所有邻接点
        for v in graph[u]:
            # 跳过父节点
            if v == parent:
                continue
                
            if not visited[v]:
                child_count += 1
                dfs(v, u)
                
                # 更新当前顶点的最低可达时间
                low[u] = min(low[u], low[v])
                
                # 判断是否为割点: 根节点有多个子节点 或 非根节点存在子节点v满足low[v] >= disc[u]
                if (parent == -1 and child_count > 1) or (parent != -1 and low[v] >= disc[u]):
                    is_cut[u] = True
            else:
                # 回边情况: 更新最低可达时间
                low[u] = min(low[u], disc[v])
    
    # 对每个连通分量运行DFS
    for i in range(n):
        if not visited[i]:
            dfs(i)
    
    # 返回所有割点
    return [i for i, flag in enumerate(is_cut) if flag]

def run_critical_intersections_finder():
    """运行关键路口查找程序"""
    print("城市关键路口查找工具")
    graph = get_graph()
    
    if graph is None:
        print("程序已退出。")
        return
        
    # 查找关键路口
    critical = find_critical_intersections(graph)
    
    # 输出结果
    if critical:
        print(f"\n找到 {len(critical)} 个关键路口:")
        print(", ".join(map(str, critical)))
        print("\n这些路口如果被阻断,将导致城市交通网络分割!")
    else:
        print("\n未找到关键路口,城市交通网络具有良好的冗余性。")