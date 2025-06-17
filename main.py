from compareFunc import find_tree_differences, find_tree_differences_no_id, search_node_by_id
from const import tree_a, tree_b, tree_a_no_id, tree_a_complex, tree_b_complex, tree_b_no_id

if __name__ == "__main__":
    solution_num = int(input("hey shay :), welcome: "))
    if solution_num == 1:
        result = find_tree_differences(tree_a, tree_b)

        print("Removed from A (only in A):")
        print(result['only_in_a'])

        print("\nAdded in B (only in B):")
        print(result['only_in_b'])
    elif solution_num == 2:

        result = find_tree_differences_no_id(tree_a_no_id, tree_b_no_id)

        print("Removed from A (only in A):")
        print(result['only_in_a'])

        print("\nAdded in B (only in B):")
        print(result['only_in_b'])
    elif solution_num == 3:

        result = find_tree_differences(tree_a_complex, tree_b_complex)

        print("Removed from A (only in A):")
        print(result['only_in_a'])

        print("\nAdded in B (only in B):")
        print(result['only_in_b'])

    elif solution_num == 4:
        node_id = input("give me: ")

        found = search_node_by_id(tree_a_complex, node_id)
        print(found if found else "Not found.")
