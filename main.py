from tarjan_algorithm import get_graph, find_critical_intersections

def main():
    """
    主流程：
    1. 获取图数据
    2. 查找关键路口
    3. 显示结果
    """
    print("城市关键路口查找工具")
    graph = get_graph()
    if graph is None:
        print("程序已退出。")
        return

    critical = find_critical_intersections(graph)
    if critical:
        print(f"\n找到 {len(critical)} 个关键路口:")
        print(", ".join(map(str, critical)))
        print("\n这些路口如果被阻断,将导致城市交通网络分割!")
    else:
        print("\n未找到关键路口,城市交通网络具有良好的冗余性。")

if __name__ == "__main__":
    main()