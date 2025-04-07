def validate_input(u, v, n, graph):
    """Validate whether the edge (u, v) is valid."""
    if u < 0 or u >= n or v < 0 or v >= n:
        return False, f"Intersection numbers must be between 0 and {n-1}!"
    if u == v:
        return False, "Self-loops are not allowed! An intersection cannot connect to itself."
    if v in graph[u]:
        return False, f"Road between intersection {u} and {v} already exists!"
    return True, ""

def get_vertex_count():
    """Get the number of intersections from the user."""
    while True:
        n = input("\nPlease enter the number of intersections in the city (enter 'q' to quit): ")
        if n.lower() == 'q':
            return None
        try:
            n = int(n)
            if n <= 0:
                print("The number of intersections must be a positive integer!")
                continue
            return n
        except ValueError:
            print("Invalid input! Please enter a positive integer.")

def get_edges(n):
    """Get road information from the user."""
    graph = [[] for _ in range(n)]
    edge_count = 0
    
    print(f"\nPlease enter road connections between intersections.")
    print("Format: enter two numbers u v, representing a road between intersections u and v.")
    print(f"Intersection numbers range from 0 to {n-1}")
    print("Enter -1 -1 to finish input.")
    
    while True:
        try:
            edge = input(f"Enter road #{edge_count+1} (or -1 -1 to finish): ")
            if edge.strip() == "":
                print("Input cannot be empty! Please enter two numbers or -1 -1.")
                continue
                
            u, v = map(int, edge.split())
            if u == -1 and v == -1:
                break
                
            is_valid, error_msg = validate_input(u, v, n, graph)
            if not is_valid:
                print(error_msg)
                continue
                
            graph[u].append(v)
            graph[v].append(u)  # Undirected graph: add edge in both directions
            edge_count += 1
            print(f"Added road: intersection {u} <--> intersection {v}")
            
        except ValueError:
            print("Invalid format! Please enter two integers separated by a space.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    return graph

def display_results(n, graph_info, cut_vertices, analysis):
    """Display the analysis results."""
    print("\n===== Analysis Results =====")
    print(f"The city has {n} intersections and {graph_info['edge_count']} roads.")
    
    if graph_info['isolated_vertices']:
        print(f"Found {len(graph_info['isolated_vertices'])} isolated intersections: ", 
              ", ".join(map(str, graph_info['isolated_vertices'])))
    
    if cut_vertices:
        print(f"\nFound {len(cut_vertices)} critical intersections:")
        print(" ".join(map(str, cut_vertices)))
        
        print("\nDetailed analysis:")
        for vertex in cut_vertices:
            components = analysis[vertex]
            print(f"Intersection {vertex}: If closed, the road network would split into {len(components)} disconnected regions.")
            for i, comp in enumerate(components):
                print(f"  Region {i+1}: contains intersections {', '.join(map(str, sorted(comp)))}")
    else:
        print("\nNo critical intersections found! The road network is robust.")

def find_critical_intersections(graph):
    """Use Tarjan's algorithm to find critical intersections (articulation points) in an undirected graph."""
    n = len(graph)
    visited = [False] * n
    disc = [-1] * n  # Discovery time
    low = [-1] * n   # Lowest discovery time reachable
    parent = [-1] * n
    is_cut_vertex = [False] * n
    time = [0]  # Wrapped in list for mutability in recursion
    
    def dfs(u):
        children = 0
        visited[u] = True
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        for v in graph[u]:
            if not visited[v]:
                children += 1
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                
                # Determine if u is a cut vertex
                if (parent[u] == -1 and children > 1) or (parent[u] != -1 and low[v] >= disc[u]):
                    is_cut_vertex[u] = True
                    
            elif v != parent[u]:  # Back edge
                low[u] = min(low[u], disc[v])
    
    # Run DFS on each connected component
    for i in range(n):
        if not visited[i]:
            dfs(i)
    
    return [i for i in range(n) if is_cut_vertex[i]]

def get_components_after_removal(graph, removed_vertex):
    """Get the connected components after removing a vertex."""
    n = len(graph)
    visited = [False] * n
    visited[removed_vertex] = True  # Treat removed vertex as already visited
    components = []
    
    def dfs(v, component):
        visited[v] = True
        component.append(v)
        for neighbor in graph[v]:
            if neighbor != removed_vertex and not visited[neighbor]:
                dfs(neighbor, component)
    
    for i in range(n):
        if not visited[i]:
            component = []
            dfs(i, component)
            if component:
                components.append(component)
    
    return components

def check_graph(graph):
    """Check the graph's connectivity and basic properties."""
    n = len(graph)
    edge_count = sum(len(adj) for adj in graph) // 2  # Each edge is counted twice
    visited = [False] * n
    isolated_vertices = []
    
    def dfs(v):
        visited[v] = True
        for neighbor in graph[v]:
            if not visited[neighbor]:
                dfs(neighbor)
    
    # Identify isolated vertices
    for i in range(n):
        if not graph[i]:
            isolated_vertices.append(i)
            visited[i] = True
    
    # Check connectivity of the remaining graph
    for i in range(n):
        if not visited[i]:
            dfs(i)
            break
    
    is_connected = all(visited)
    
    return {
        'edge_count': edge_count,
        'is_connected': is_connected,
        'isolated_vertices': isolated_vertices
    }

def analyze_critical_intersections(graph):
    """Analyze the critical intersections and their impact."""
    cut_vertices = find_critical_intersections(graph)
    
    analysis = {}
    for vertex in cut_vertices:
        components = get_components_after_removal(graph, vertex)
        analysis[vertex] = components
    
    return cut_vertices, analysis