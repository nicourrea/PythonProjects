# Nicolas Urrea
# nu22c
# 05/29/2025
# The program in this file is the individual work of Nicolas Urrea

def line_input(line_str):
    try:
        return list(map(int, line_str.strip('[] \n').split(',')))
    except:
        print("Invalid input format. Please enter line as [x1,y1,x2,y2]")
        return None

def shape_edge(p1, p2):
    return tuple(sorted([tuple(p1), tuple(p2)])) # keep edge direction consistent

def main():
    try:
        n = int(input("Enter the number of lines: "))
    except ValueError:
        print("Invalid number of lines.")
        return

    print("Enter the lines:")
    
    edges = set()
    graph_point = {}

    for _ in range(n):
        line_str = input()
        line = line_input(line_str)
        if line is None or len(line) != 4:
            continue

        p1, p2 = (line[0], line[1]), (line[2], line[3])
        edge = shape_edge(p1, p2)
        edges.add(edge)

        #adjacnecy list
        for a, b in [(p1, p2), (p2, p1)]:
            if a not in graph_point:
                graph_point[a] = []
            graph_point[a].append(b)

    visited_edges = set()

    def dfs(current, start, path):
        if len(path) > 1 and current == start:
            return path # all edges connect forming a cycle

        for neighbor in graph_point.get(current, []):
            edge = shape_edge(current, neighbor)
            if edge not in visited_edges:
                visited_edges.add(edge)
                result = dfs(neighbor, start, path + [neighbor])
                if result:
                    return result
                visited_edges.remove(edge)

        return None

    for point in graph_point:
        path = dfs(point, point, [point])
        if path:
            print(f"The lines form a closed figure with {len(path) - 1} sides")
            return

    print("The lines do not form a closed figure.")

if __name__ == "__main__":
    main()