def part_1(tree):
    # Run node
    # Go through each child node
    # Sum metadata
    # Sum final metadata
    return run_node(tree, 0)


def run_node(tree, node_start):
    # Go through each child node
    child_node_quant = tree[node_start]
    metadata_quant = tree[node_start+1]
    child_nodes_done = 0
    index = node_start+2
    child_sums = 0
    while child_nodes_done < child_node_quant:
        child_add, index = run_node(tree, index)
        child_sums += child_add
        child_nodes_done += 1
    metadata_sum = sum(tree[index:(index+metadata_quant)])
    # Returns sum of metadata, and index of next node
    return child_sums + metadata_sum, index + metadata_quant


input_file = open('2018_8_input.txt', 'r').read().splitlines()
input_numeric = [int(i) for i in input_file[0].split(' ')]
print(part_1(input_numeric))


def part_2(tree):
    return run_node_2(tree, 0)


def run_node_2(tree, node_start):
    # Go through each child node
    child_node_quant = tree[node_start]
    metadata_quant = tree[node_start+1]
    child_nodes_done = 0
    index = node_start+2
    child_sums = []
    while child_nodes_done < child_node_quant:
        child_add, index = run_node_2(tree, index)
        child_sums.append(child_add)
        child_nodes_done += 1
    metadata = tree[index:(index+metadata_quant)]
    if child_node_quant == 0:
        return sum(metadata), index + metadata_quant
    else:
        metadata_sum = 0
        for i in metadata:
            if len(child_sums) + 1 > i > 0:
                metadata_sum += child_sums[i-1]
        return metadata_sum, index + metadata_quant


print(part_2(input_numeric))
