import pandas as pd
from typing import Dict, Any, List

def flatten_tree(tree: Dict[str, Any], path=()) -> List[Dict[str, Any]]:
    """
    Flatten tree to a list of nodes, including the full path to each node.
    """
    node = {
        'id': tree['id'],
        'name': tree.get('name'),
        'type': tree.get('type'),
        'path': ' > '.join(path + (tree.get('name', ''),))
    }
    nodes = [node]
    for child in tree.get('children', []):
        nodes.extend(flatten_tree(child, path + (tree.get('name', ''),)))
    return nodes

def find_tree_differences(tree_a: Dict[str, Any], tree_b: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Compares two trees and returns:
    - nodes only in A (removed)
    - nodes only in B (added)
    """
    df_a = pd.DataFrame(flatten_tree(tree_a)).set_index('id')
    df_b = pd.DataFrame(flatten_tree(tree_b)).set_index('id')

    # Compare index (IDs)
    only_in_a = df_a[~df_a.index.isin(df_b.index)]
    only_in_b = df_b[~df_b.index.isin(df_a.index)]

    return {
        'only_in_a': only_in_a.reset_index(),
        'only_in_b': only_in_b.reset_index()
    }


import pandas as pd
from typing import Dict, Any, List

def flatten_tree_no_id(tree: Dict[str, Any], path=()) -> List[Dict[str, Any]]:
    """
    Flatten the tree into a list of nodes based on path + name (no id).
    """
    current_path = path + (tree.get('name', ''),)
    node = {
        'name': tree.get('name'),
        'type': tree.get('type'),
        'path': ' > '.join(current_path)
    }
    nodes = [node]
    for child in tree.get('children', []):
        nodes.extend(flatten_tree_no_id(child, current_path))
    return nodes

def find_tree_differences_no_id(tree_a: Dict[str, Any], tree_b: Dict[str, Any]) -> Dict[str, pd.DataFrame]:
    """
    Compares two trees by full path. Returns nodes only in A and only in B.
    """
    df_a = pd.DataFrame(flatten_tree_no_id(tree_a)).set_index('path')
    df_b = pd.DataFrame(flatten_tree_no_id(tree_b)).set_index('path')

    only_in_a = df_a[~df_a.index.isin(df_b.index)].reset_index()
    only_in_b = df_b[~df_b.index.isin(df_a.index)].reset_index()

    return {
        'only_in_a': only_in_a,
        'only_in_b': only_in_b
    }


def search_node_by_id(tree: Dict[str, Any], target_id: str) -> Dict[str, Any] or None:
    """
    Recursively search a tree for a node by its ID.
    Returns the node dict if found, or None.
    """
    if tree.get('id') == target_id:
        return tree
    for child in tree.get('children', []):
        result = search_node_by_id(child, target_id)
        if result is not None:
            return result
    return None

def compare_trees_for_ui(tree_a, tree_b):
    df_a = pd.DataFrame(flatten_tree(tree_a)).set_index('id')
    df_b = pd.DataFrame(flatten_tree(tree_b)).set_index('id')
    only_in_a = df_a[~df_a.index.isin(df_b.index)].reset_index()
    only_in_b = df_b[~df_b.index.isin(df_a.index)].reset_index()
    return only_in_a, only_in_b