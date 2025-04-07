def validate_input(u, v, n, graph):
    """
    校验边 (u, v) 合法性：
      - 路口编号 0 ≤ u,v < n
      - 不允许自环（u == v）
      - 不允许重复边（graph[u] 已包含 v）
    返回 (bool, error_msg)
    """
    # 检查顶点编号是否在有效范围内（0到n-1之间）
    if u < 0 or u >= n or v < 0 or v >= n:
        # 如果任一顶点编号越界，返回错误信息
        return False, f"路口编号必须在 0 到 {n-1} 之间！"
    # 检查是否为自环（起点和终点相同）
    if u == v:
        # 如果是自环，返回错误信息
        return False, "不能添加自环！"
    # 检查是否已存在这条边（防止重复添加）
    if v in graph[u]:
        # 如果边已存在，返回错误信息
        return False, f"道路 {u} <--> {v} 已存在！"
    # 验证通过，返回成功标志和空错误信息
    return True, ""

def get_vertex_count():
    """
    获取用户输入的顶点数量：
      - 输入正整数，或输入 'q' 退出
      - 重复提示直到获得合法值或退出
    """
    # 无限循环，直到获得有效输入或用户选择退出
    while True:
        # 提示用户输入路口数量，并获取输入
        n = input("\n请输入城市中路口的数量 (输入'q'退出): ")
        # 检查用户是否输入了退出命令
        if n.lower() == 'q':
            # 如果用户输入q或Q，返回None表示用户选择退出
            return None
        try:
            # 尝试将输入转换为整数
            n = int(n)
            # 检查输入的数是否为正整数
            if n <= 0:
                # 如果不是正整数，显示错误提示
                print("路口数量必须是正整数！")
                # 继续下一次循环，重新获取输入
                continue
            # 输入有效，返回路口数量
            return n
        except ValueError:
            # 如果输入无法转换为整数，显示错误提示
            print("无效输入！请输入一个正整数。")

def get_edges(n):
    """
    构造无向图的邻接表：
      - 初始化 graph = [[] for _ in range(n)]
      - 用户输入 u v 表示添加一条无向边
      - 输入 -1 -1 结束
      - 每次添加前调用 validate_input()
    返回 graph
    """
    # 初始化邻接表表示的图，每个顶点对应一个空列表
    graph = [[] for _ in range(n)]
    # 初始化边计数器为0
    edge_count = 0
    # 打印输入提示信息
    print(f"\n请输入连接路口的道路信息。")
    print("格式：u v （如 0 1），输入 -1 -1 结束。")
    
    # 无限循环，直到用户输入-1 -1结束
    while True:
        try:
            # 提示用户输入一条道路（一条边）
            raw = input(f"请输入第{edge_count+1}条道路 (或 -1 -1 结束): ")
            # 检查输入是否为空
            if raw.strip() == "":
                # 如果输入为空，显示错误提示
                print("输入不能为空！")
                # 继续下一次循环，重新获取输入
                continue
            # 将输入分割并转换为两个整数u和v
            u, v = map(int, raw.split())
            # 检查是否为结束标志
            if u == -1 and v == -1:
                # 如果是结束标志，跳出循环
                break
            # 验证输入的边是否合法
            valid, msg = validate_input(u, v, n, graph)
            # 如果验证不通过
            if not valid:
                # 打印错误信息
                print(msg)
                # 继续下一次循环，重新获取输入
                continue
            # 在邻接表中添加边u->v
            graph[u].append(v)
            # 在邻接表中添加边v->u（因为是无向图）
            graph[v].append(u)
            # 边计数器增加1
            edge_count += 1
            # 打印成功添加边的信息
            print(f"已添加道路：{u} <--> {v}")
        except ValueError:
            # 如果输入格式错误无法转换为整数，显示错误提示
            print("格式错误！请输入两个整数。")
    # 返回构建好的图（邻接表）
    return graph

def check_graph(graph):
    """
    检查图的基本属性：
      - 边数 = sum(len(adj))/2
      - 孤立顶点列表
      - 是否连通（除孤立顶点外是否全被 DFS 访问）
    返回 dict：{ edge_count, is_connected, isolated_vertices }
    """
    # 获取图中顶点的数量
    n = len(graph)
    # 计算图中边的数量（每条边在邻接表中出现两次，所以除以2）
    edge_count = sum(len(adj) for adj in graph)//2
    # 初始化访问标记数组，标记所有顶点为未访问
    visited = [False]*n
    # 初始化孤立顶点列表
    isolated = []
    
    # 定义深度优先搜索函数
    def dfs(u):
        # 标记当前顶点为已访问
        visited[u] = True
        # 遍历当前顶点的所有邻居
        for w in graph[u]:
            # 如果邻居未被访问，则递归访问它
            if not visited[w]:
                dfs(w)
    
    # 标记孤立点（没有与其他顶点相连的顶点）
    for i, adj in enumerate(graph):
        # 如果顶点的邻接列表为空，则它是孤立的
        if not adj:
            # 将顶点添加到孤立顶点列表
            isolated.append(i)
            # 标记为已访问（因为孤立点不需要通过DFS访问）
            visited[i] = True
    
    # 从第一个非孤立点开始DFS
    for i in range(n):
        # 如果找到未访问的顶点，从它开始DFS
        if not visited[i]:
            dfs(i)
            break
    
    # 返回图的属性字典
    return {
        'edge_count': edge_count,  # 边的数量
        'is_connected': all(visited),  # 是否所有顶点都可达（图是否连通）
        'isolated_vertices': isolated  # 孤立顶点列表
    }

def find_critical_intersections(graph):
    """
    Tarjan 割点算法核心：
      - 使用 DFS 记录发现时间 disc[] 和 low[]
      - 根节点 child_count > 1 → 割点
      - 非根节点若存在子 v 满足 low[v] >= disc[u] → 割点
    返回割点列表
    """
    # 获取图中顶点的数量
    n = len(graph)
    # 初始化顶点访问标记数组
    visited = [False]*n
    # 初始化顶点的发现时间数组，-1表示未发现
    disc = [-1]*n
    # 初始化顶点的最低可达时间数组，-1表示未计算
    low = [-1]*n
    # 初始化顶点的父节点数组，-1表示无父节点（根节点）
    parent = [-1]*n
    # 初始化割点标记数组，False表示不是割点
    is_cut = [False]*n
    # 使用列表存储时间计数器（方便在递归中修改）
    time = [0]
    
    # 定义Tarjan算法的深度优先搜索函数
    def dfs(u):
        # 标记当前顶点为已访问
        visited[u] = True
        # 设置顶点的发现时间和初始最低可达时间为当前时间，然后时间增加1
        disc[u] = low[u] = time[0]
        time[0] += 1
        # 初始化子节点计数器
        child = 0
        
        # 遍历当前顶点的所有邻居
        for v in graph[u]:
            # 如果邻居未被访问
            if not visited[v]:
                # 设置邻居的父节点为当前顶点，子节点计数增加1
                parent[v] = u
                child += 1
                # 递归访问邻居
                dfs(v)
                # 更新当前顶点的最低可达时间
                low[u] = min(low[u], low[v])
                
                # 判断当前顶点是否为割点：
                # 1) 如果是根节点(parent[u] == -1)且有多个子节点(child > 1)
                # 2) 如果不是根节点且存在子节点v，其low[v]>=disc[u]
                if (parent[u] == -1 and child > 1) or \
                   (parent[u] != -1 and low[v] >= disc[u]):
                    # 标记当前顶点为割点
                    is_cut[u] = True
            # 如果邻居已被访问，且不是当前顶点的父节点（是回边）
            elif v != parent[u]:
                # 更新当前顶点的最低可达时间
                low[u] = min(low[u], disc[v])
    
    # 对图中每个顶点进行处理
    for i in range(n):
        # 如果顶点未被访问，从它开始DFS
        if not visited[i]:
            dfs(i)
    
    # 返回所有被标记为割点的顶点列表
    return [i for i, flag in enumerate(is_cut) if flag]