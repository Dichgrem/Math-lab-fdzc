import tarjan_algorithm as ta

def main():
    """Main function: Interactive critical intersection finder"""
    print("Welcome to the Critical Intersection Finder!")
    print("This program helps you identify critical intersections in a road network.")
    
    while True:
        # Get the number of intersections
        n = ta.get_vertex_count()
        if n is None:
            print("Bye")
            break
        
        # Get the road connections
        graph = ta.get_edges(n)
        
        # Analyze basic properties of the graph
        graph_info = ta.check_graph(graph)
        
        # If the graph is not fully connected, warn the user
        if not graph_info['is_connected'] and graph_info['edge_count'] > 0:
            print("\nWarning: The input road network is not fully connected!")
            proceed = input("Do you still want to find critical intersections? (y/n): ")
            if proceed.lower() != 'y':
                continue
        
        # Find critical intersections
        print("\nFinding critical intersections...")
        cut_vertices, analysis = ta.analyze_critical_intersections(graph)
        
        # Display the result
        ta.display_results(n, graph_info, cut_vertices, analysis)
        
        # Ask if the user wants to analyze another network
        if input("\nWould you like to analyze another road network? (y/n): ").lower() != 'y':
            print("Bye")
            break

if __name__ == "__main__":
    main()