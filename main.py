import tarjan_algorithm as ta

def main():
    """
    主函数：
      1. 获取顶点数
      2. 构建图
      3. 寻找关键路口并输出
    """
    n = ta.get_vertex_count()
    if n is None:
        return
    
    graph = ta.get_edges(n)
    cut_vertices = ta.find_critical_intersections(graph)
    
    print("\n===== 分析结果 =====")
    if cut_vertices:
        print(f"关键路口（共{len(cut_vertices)}个）：{' '.join(map(str, cut_vertices))}")
    else:
        print("没有找到关键路口，网络非常健壮！")

if __name__ == "__main__":
    main()