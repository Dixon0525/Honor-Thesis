import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import matplotlib.animation as animation
import matplotlib.cm as mpl_cm
from math import gcd


def generate_cayley_graph(m, n, X):
    G = nx.Graph()
    vertices = [(i, j) for i in range(m) for j in range(n)]
    G.add_nodes_from(vertices)
    for x, y in vertices:
        for dx, dy in X:
            neighbor = ((x + dx) % m, (y + dy) % n)
            G.add_edge((x, y), neighbor)
    return G


def expand_W_g(W, g, j):
    # O(j)*O(|W|)=O(j*N) bounded by O(N^2)
    W_hat = W[1:-1]
    W_hat_inv = [(-x[0] % m, -x[1] % n) for x in reversed(W_hat)]
    sequence = []
    for i in range(j - 1 if j % 2 == 1 else j - 2):
        sequence.append(g)
        if i % 2 == 0:
            sequence.extend(W_hat_inv)
        else:
            sequence.extend(W_hat)

    return sequence


def compute_T(S, Q, g, j, m, n):
    S_bar = S[:-1]
    W = S_bar + Q
    Q_bar = Q[:-1] if len(Q) > 1 else []
    W_bar = W[:-1] if len(W) > 2 else []
    W_hat_inv = [(-x[0] % m, -x[1] % n) for x in reversed(W_bar)]
    g_inv = (-g[0] % m, -g[1] % n)
    expanded_W_g = expand_W_g(W, g, j)
    if j % 2 == 1:
        T = Q_bar + expanded_W_g + [W[-1]] + [g_inv] * (j - 1)
    else:
        T = Q_bar + expanded_W_g + [g] + W_hat_inv + [g_inv] * (j - 1)
    return T


def generate_hamiltonian_circuit(ST):
    circuit = [ST[0]]
    generator_sequence = []
    for move in ST[1:]:
        next_position = ((circuit[-1][0] + move[0]) % m, (circuit[-1][1] + move[1]) % n)
        circuit.append(next_position)
        generator_sequence.append(move)
    return circuit, generator_sequence


def animate_hamiltonian_circuit(G, circuit, generator_sequence, generator_list, title="Hamiltonian Circuit Animation"):
    pos = {(i, j): (i, -j) for i, j in G.nodes()}
    fig, ax = plt.subplots(figsize=(20, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightgray', edge_color='gray', node_size=500)
    colors = ['red', 'blue', 'black', 'purple', 'orange', 'cyan', 'magenta',
              'yellow', 'brown', 'pink', 'lime', 'teal', 'lavender', 'gold', 'navy']
    color_map = {}
    for i, g in enumerate(generator_list):
        inv_g = ((-g[0]) % m, (-g[1]) % n)
        color = colors[i % len(colors)]
        color_map[g] = color
        color_map[inv_g] = color

    visited_nodes = {}
    visited_edges = []
    edge_colors = []

    for num in range(len(generator_sequence)):
        ax.clear()
        nx.draw(G, pos, with_labels=False, node_color='black', edge_color='white', node_size=1)

        g_used = generator_sequence[num]
        color = color_map.get(g_used, 'black')

        visited_nodes[circuit[num]] = color
        edge = (circuit[num], circuit[num + 1])
        if edge not in visited_edges and (edge[1], edge[0]) not in visited_edges:
            visited_edges.append(edge)
        edge_colors.append(color)

        nx.draw_networkx_nodes(G, pos, nodelist=list(visited_nodes.keys()), node_color="black", node_size=1)
        nx.draw_networkx_edges(G, pos, edgelist=visited_edges, edge_color=edge_colors)
        ax.set_title(f"{title} Step {num + 1}/{len(generator_sequence)+1}")
        plt.pause(0.001)

    final_edge = (circuit[-1], circuit[0])
    if final_edge not in visited_edges and (final_edge[1], final_edge[0]) not in visited_edges:
        visited_edges.append(final_edge)
        edge_colors.append(colors[0])
        nx.draw_networkx_edges(G, pos, edgelist=visited_edges, edge_color=edge_colors)
        ax.set_title(f"{title} Step {len(generator_sequence)+1}/{len(generator_sequence)+1}")
        plt.pause(0.001)

    plt.show()


if __name__ == "__main__":
    m = int(input("Input m for Z_m: "))
    n = int(input("Input n for Z_n: "))
    M = eval(input("Input generating set M (format: [(dx1, dy1), (dx2, dy2)]): "))
    M = [g for g in M if g != (0, 0)]
    G = generate_cayley_graph(m, n, M)


    def generate_order(gens):
        visited = set()
        frontier = [(0, 0)]
        while frontier:
            current = frontier.pop()
            if current in visited:
                continue
            visited.add(current)
            for dx, dy in gens:
                neighbor = ((current[0] + dx) % m, (current[1] + dy) % n)
                if neighbor not in visited:
                    frontier.append(neighbor)
        return visited

    minimal_M = []
    for i in range(len(M)):
        trial = minimal_M + [M[i]]
        generated = generate_order(trial)
        if len(generated) == m * n:
            minimal_M = trial
            break
        minimal_M = trial
    # check if redundant
    print(f"minimal generating set: {minimal_M}")

    g1 = minimal_M[0]
    s = 1
    current = g1
    while current != (0, 0):
        s += 1
        current = ((current[0] + g1[0]) % m, (current[1] + g1[1]) % n)
    S = [g1] * s

    for i in range(1, len(minimal_M)):
        g = minimal_M[i]
        Q = [S[-1]]
        j = 1

        generated_H = set()
        basis = minimal_M[:i]
        frontier = [(0, 0)]
        while frontier:
            current = frontier.pop()
            if current in generated_H:
                continue
            generated_H.add(current)
            for dx, dy in basis:
                neighbor = ((current[0] + dx) % m, (current[1] + dy) % n)
                if neighbor not in generated_H:
                    frontier.append(neighbor)

        current = g
        while current not in generated_H:
            j += 1
            current = ((current[0] + g[0]) % m, (current[1] + g[1]) % n)

        T = compute_T(S, Q, g, j, m, n)
        S = S[:-1] + T

    circuit, generator_sequence = generate_hamiltonian_circuit(S)
    animate_hamiltonian_circuit(G, circuit, generator_sequence, M, title="Animating Hamiltonian Circuit in G")

# [(1, 0), (0, 1)]
# [(1, 1), (2, 4), (3, 4)]
# [(2, 4), (1, 1), (3, 4)]
# [(1, 1), (3, 4)]
# [(1, 1), (2, 4)]
