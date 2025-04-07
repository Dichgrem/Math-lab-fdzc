def get_graph():
    """
    交互式获取图结构函数:
    - 从用户输入获取顶点数量
    - 从用户输入获取边的信息
    - 构建并返回邻接表表示的无向图
    
    返回:
        邻接表表示的图，或者当用户选择退出时返回None
    """
    # 循环直到获得有效的顶点数量或用户选择退出
    while True:
        try:
            # 提示用户输入顶点数量
            n = input("\n请输入路口数量 (或输入'q'退出): ")
            # 检查用户是否选择退出
            if n.lower() == 'q':
                return None
            # 将输入转换为整数
            n = int(n)
            # 验证顶点数量必须为正整数
            if n <= 0:
                print("路口数量必须是正整数！")
                continue
            # 若验证通过，跳出循环
            break
        except ValueError:
            # 输入无法转换为整数时的错误处理
            print("无效输入！请输入正整数。")
    
    # 初始化邻接表，为每个顶点创建一个空列表
    graph = [[] for _ in range(n)]
    
    # 打印输入提示信息
    print(f"\n请输入道路信息 (格式: u v，如 0 1)")
    print("输入 -1 -1 结束输入")
    
    # 记录已添加的边数
    edge_count = 0
    # 循环获取边的信息，直到用户输入结束标志
    while True:
        try:
            # 提示用户输入一条边
            raw = input(f"第{edge_count+1}条道路 (或 -1 -1 结束): ")
            # 检查输入是否为空
            if not raw.strip():
                print("输入不能为空！")
                continue
            
            # 将输入分割并转换为两个整数（顶点索引）
            u, v = map(int, raw.split())
            # 检查是否为结束标志
            if u == -1 and v == -1:
                break
            
            # 验证顶点索引是否在有效范围内
            if u < 0 or u >= n or v < 0 or v >= n:
                print(f"路口编号必须在 0 到 {n-1} 之间！")
                continue
            # 验证是否为自环（同一顶点）
            if u == v:
                print("不能添加自环！")
                continue
            # 验证边是否已存在
            if v in graph[u]:
                print(f"道路 {u} <--> {v} 已存在！")
                continue
            
            # 在邻接表中添加边（无向图需要添加两次）
            graph[u].append(v)
            graph[v].append(u)
            # 更新边计数器
            edge_count += 1
            # 打印成功添加的信息
            print(f"已添加: {u} <--> {v}")
        except ValueError:
            # 输入格式错误时的处理
            print("格式错误！请输入两个整数。")
    
    # 返回构建好的图
    return graph

def find_critical_intersections(graph):
    """
    查找城市中的关键路口（割点）。
    实现基于Tarjan算法寻找无向图中的割点。
    
    参数:
        graph: 邻接表表示的城市道路网络，格式为 [[], [], ...]，
               其中graph[i]包含与顶点i相连的所有顶点列表
               
    返回:
        关键路口（割点）的列表
    """
    # 获取图中顶点的总数
    n = len(graph)
    # 初始化访问标记数组，False表示未访问
    visited = [False] * n
    # 初始化发现时间数组，-1表示未发现
    disc = [-1] * n     
    # 初始化最低可达时间数组，用于追踪回边
    low = [-1] * n      
    # 初始化割点标记数组，False表示不是割点
    is_cut = [False] * n
    # 使用列表实现可变时间计数器（在递归函数中需要修改）
    time = [0]          
    
    def dfs(u, parent=-1):
        """
        深度优先搜索函数，用于发现割点
        
        参数:
            u: 当前正在访问的顶点
            parent: 当前顶点的父节点，默认为-1（表示根节点）
        """
        # 标记当前顶点为已访问
        visited[u] = True
        # 设置顶点的发现时间和初始最低可达时间
        disc[u] = low[u] = time[0]
        # 时间计数器增加
        time[0] += 1
        # 记录当前顶点的直接子节点数量
        child_count = 0
        
        # 遍历当前顶点的所有邻接点
        for v in graph[u]:
            # 如果是父节点，跳过（避免重复访问）
            if v == parent:
                continue
                
            # 如果邻接点未访问，则进行DFS探索
            if not visited[v]:
                # 子节点计数增加
                child_count += 1
                # 递归访问子节点
                dfs(v, u)
                
                # 更新当前顶点的最低可达时间
                # low[u]表示从u出发能够到达的最早被发现的顶点
                low[u] = min(low[u], low[v])
                
                # 判断当前顶点是否为割点:
                # 条件1: 如果是根节点(parent=-1)且有多个子节点(child_count>1)
                # 条件2: 如果不是根节点，且存在子节点v，其low[v]>=disc[u]，
                #        说明v及其子孙无法通过回边到达u的祖先
                if (parent == -1 and child_count > 1) or (parent != -1 and low[v] >= disc[u]):
                    is_cut[u] = True
            else:
                # 如果邻接点已访问（发现回边），更新最低可达时间
                # 这是处理"回边"的情况，即连接到已访问节点的边
                low[u] = min(low[u], disc[v])
    
    # 对每个连通分量运行DFS
    # 因为图可能不是完全连通的，需要确保所有顶点都被处理
    for i in range(n):
        if not visited[i]:
            dfs(i)
    
    # 返回所有被标记为割点的顶点索引列表
    return [i for i, flag in enumerate(is_cut) if flag]

def run_critical_intersections_finder():
    """
    运行关键路口查找程序的主要流程:
    1. 获取图数据
    2. 运行查找算法
    3. 显示结果
    """
    # 显示程序标题
    print("城市关键路口查找工具")
    # 获取图结构
    graph = get_graph()
    
    # 如果用户选择退出，则结束程序
    if graph is None:
        print("程序已退出。")
        return
    
    # 调用Tarjan算法查找关键路口（割点）
    critical = find_critical_intersections(graph)
    
    # 根据结果输出相应信息
    if critical:
        # 找到关键路口时，显示数量和列表
        print(f"\n找到 {len(critical)} 个关键路口:")
        print(", ".join(map(str, critical)))
        print("\n这些路口如果被阻断,将导致城市交通网络分割!")
    else:
        # 未找到关键路口时，显示网络的冗余性良好
        print("\n未找到关键路口,城市交通网络具有良好的冗余性。")