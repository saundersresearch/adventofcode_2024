import networkx as nx

with open("inputs/day5.txt") as f:
    input_string = f.read()


### Part 1
page_order_rules, pages_to_produce = input_string.split("\n\n")
page_order_rules = page_order_rules.splitlines()

# Are they sorted?
middle_sum = 0
for page_str in pages_to_produce.splitlines():
    page_array = page_str.split(",")

    # Create graph using page_order_rules
    edge_list = [rule.split("|") for rule in page_order_rules]
    edge_list = [
        edge for edge in edge_list if edge[0] in page_array and edge[1] in page_array
    ]
    graph = nx.from_edgelist(edge_list, create_using=nx.DiGraph)

    # Is it a tournament?
    assert nx.is_tournament(graph), "Graph is not a tournament."

    # Find Hamiltonian path
    sorted_pages = nx.tournament.hamiltonian_path(graph)

    if page_array == sorted(page_array, key=lambda x: sorted_pages.index(x)):
        middle_index = len(page_array) // 2
        middle_sum += int(page_array[middle_index])

print(f"{middle_sum=}")

### Part 2
middle_sum = 0
for page_str in pages_to_produce.splitlines():
    page_array = page_str.split(",")

    # Create graph using page_order_rules
    edge_list = [rule.split("|") for rule in page_order_rules]
    edge_list = [
        edge for edge in edge_list if edge[0] in page_array and edge[1] in page_array
    ]
    graph = nx.from_edgelist(edge_list, create_using=nx.DiGraph)

    # Is it a tournament?
    assert nx.is_tournament(graph), "Graph is not a tournament."

    # Find Hamiltonian path
    sorted_pages = nx.tournament.hamiltonian_path(graph)
    sorted_page_array = sorted(page_array, key=lambda x: sorted_pages.index(x))
    if page_array != sorted_page_array:
        middle_index = len(page_array) // 2
        middle_sum += int(sorted_page_array[middle_index])

print(f"{middle_sum=}")