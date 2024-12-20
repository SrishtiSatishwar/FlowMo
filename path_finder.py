from data import cameraGraph

"""I applied the concept of graph traversal to traverse from a source node to a destination node, traversing the path recursively."""
"""This function has been written by me for the most part. I used GPT assistance for a few lines of conceptual clarification."""
def findPaths(graph, start, end, max_paths=2):
    paths = []
    visited = set()
    def dfs(current_path):
        nonlocal paths
        # If destination reached, add path to results and return paths. It will trigger the entire
        # recursion for the next neighbour
        current_camera = current_path[-1]
        if current_camera == end:
            paths.append(current_path[:])
            return
        
        # Traverse neighbors one at a time. 
        # For every neighbour it will recursively call dfs and traverse
        for neighbor in graph[current_camera]:
            if neighbor not in visited:
                visited.add(neighbor)
                current_path.append(neighbor)
                dfs(current_path)
                # start unwinding here when a path is found.
                # after complete removal of current_path and visited, we will go back to next neighbour and find
                # path from that neighbour 
                # For example RC1C1 -> RC1C2 (first neibhour of RC1C1) -> RC1C3... to destination.
                # then        RC1C1 -> RC2C1 (second beighbour of RC1C1) -> RC2C2.... to destination.
                current_path.pop()
                visited.remove(neighbor)

    # Mark "start" point as visited and immediately start traversal
    visited.add(start)
    # Start graph traversal from the "start" point, mark it as visited
    dfs([start])
    # I'm limiting to two paths only, as I want to show ETA for two comparable paths.
    return paths[:max_paths]


"""Test Cases produced by GPT, helped test the findPaths() function which was imported into the main file."""
def run_test_case(start, end):
    # Run a single test case.
    print(f"Test Case: Start = {start}, End = {end}")
    paths = findPaths(camera_graph, start, end)
    if paths:
        for i, path in enumerate(paths):
            print(f"  Path {i + 1}: {path}")
    else:
        print("  No paths found.")
    print("-" * 40)

def main():
    # Run test cases for path_finder.
    # Define test cases
    test_cases = [
        ("RC1C1", "RC2C5"),  # Valid paths between two connected cameras
        ("RC1C2", "RC1C5"),  # Valid paths with a more roundabout route
        ("RC1C2", "RC2C3"),  # Multiple valid paths possible
        ("RC1C1", "RC1C1"),  # Same start and end (should return one empty path)
        ("RC1C1", "RC1C4"),  # Invalid path (non-existent end point)
    ]

    # Run each test case
    for start, end in test_cases:
        run_test_case(start, end)

if __name__ == "__main__":
    main()