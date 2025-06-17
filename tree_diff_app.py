import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components
from compareFunc import compare_trees_for_ui

st.set_page_config(page_title="Tree Diff Viewer", layout="wide")
st.title("🌳 Organizational Tree Diff Viewer")

display_mode = st.radio(
    "Choose how to display the comparison results:",
    ("Table View", "Tree View", "Visual Tree")
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Tree A (JSON)")
    tree_a_input = st.text_area("Paste JSON for Tree A", height=400)

with col2:
    st.subheader("📁 Tree B (JSON)")
    tree_b_input = st.text_area("Paste JSON for Tree B", height=400)


def merge_trees(a, b):
    """Recursively merge two trees by name."""
    if not isinstance(a, list): a = [a]
    if not isinstance(b, list): b = [b]

    def build_dict_by_name(tree):
        return {node["name"]: node for node in tree if "name" in node}

    dict_a = build_dict_by_name(a)
    dict_b = build_dict_by_name(b)

    merged = []

    for name in set(dict_a.keys()).union(dict_b.keys()):
        node = {"name": name}
        node_a = dict_a.get(name)
        node_b = dict_b.get(name)

        # Tag source
        if node_a and node_b:
            node["__source__"] = "both"
        elif node_a:
            node["__source__"] = "a"
        elif node_b:
            node["__source__"] = "b"

        # Merge metadata
        for k in set((node_a or {}).keys()).union((node_b or {}).keys()):
            if k not in ("name", "children"):
                node[k] = (node_a or {}).get(k) or (node_b or {}).get(k)

        # Merge children
        children_a = node_a.get("children", []) if node_a else []
        children_b = node_b.get("children", []) if node_b else []
        merged_children = merge_trees(children_a, children_b)
        if merged_children:
            node["children"] = merged_children

        merged.append(node)

    return merged


def render_tree(nodes, parent_label=""):
    if isinstance(nodes, pd.DataFrame):
        nodes = nodes.to_dict(orient="records")
    if isinstance(nodes, dict):
        nodes = [nodes]
    for node in nodes:
        label = node.get("name", str(node))
        with st.expander(f"{parent_label}{label}"):
            for k, v in node.items():
                if k != "children":
                    st.write(f"**{k}:** {v}")
            if "children" in node:
                render_tree(node["children"], parent_label="  ")

def extract_node_ids(nodes):
    """Flatten a tree into a set of unique IDs or names (depending on your structure)."""
    found = set()
    if isinstance(nodes, pd.DataFrame):
        nodes = nodes.to_dict(orient="records")
    if isinstance(nodes, dict):
        nodes = [nodes]
    for node in nodes:
        name = node.get("name", None)
        if name:
            found.add(name)
        if "children" in node:
            found.update(extract_node_ids(node["children"]))
    return found

def build_html_tree_highlighted(tree, highlight_set=None, color=None):
    if isinstance(tree, pd.DataFrame):
        tree = tree.to_dict(orient="records")
    if isinstance(tree, list):
        return ''.join([build_html_tree_highlighted(node, highlight_set, color) for node in tree])

    label = tree.get("name", "Unnamed")
    tooltip = "<br>".join(f"{k}: {v}" for k, v in tree.items() if k not in ("children", "__source__"))

    # Default values
    node_class = ""
    style_attr = ""

    if highlight_set is not None and color:
        # For Tree A / Tree B views
        if label in highlight_set:
            node_class = "highlight"
            style_attr = f' style="background-color:{color}; color:white; border-color:{color}; font-weight:bold;"'
    elif "__source__" in tree:
        # For combined tree view
        source = tree["__source__"]
        if source == "a":
            node_class = "highlight"
            style_attr = ' style="background-color:#e74c3c; color:white; border-color:#e74c3c; font-weight:bold;"'
        elif source == "b":
            node_class = "highlight"
            style_attr = ' style="background-color:#2ecc71; color:white; border-color:#2ecc71; font-weight:bold;"'
        # source == "both" → white, no class or style

    children = tree.get("children", [])
    children_html = ""
    if children:
        children_html = "<ul>"
        children_html += ''.join([build_html_tree_highlighted(child, highlight_set, color) for child in children])
        children_html += "</ul>"

    html = f'''
    <li>
        <div class="node {node_class}" title="{tooltip}" onclick="toggleCollapse(this)"{style_attr}>
            {label}
        </div>
        {children_html}
    </li>
    '''
    return html





def display_visual_tree_with_highlight(full_tree, highlight_nodes, color, layout="vertical"):
    html_body = build_html_tree_highlighted(full_tree, highlight_nodes, color)

    orientation_class = "tree-vertical" if layout == "vertical" else "tree-horizontal"

    html = f"""
    <div>
        <button onclick="downloadTree()">📸 Download Tree as PNG</button>
    </div>
    <div class="tree-container {orientation_class}" id="treeWrapper">
        <ul class="tree">{html_body}</ul>
    </div>

    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <script>
    function toggleCollapse(node) {{
        const li = node.parentElement;
        const children = li.querySelector("ul");
        if (children) {{
            children.style.display = children.style.display === "none" ? "block" : "none";
        }}
    }}

    function downloadTree() {{
        const element = document.getElementById("treeWrapper");
        html2canvas(element).then(canvas => {{
            const link = document.createElement('a');
            link.download = 'tree.png';
            link.href = canvas.toDataURL();
            link.click();
        }});
    }}
    </script>

    <style>
    .tree-container {{
        overflow: auto;
        padding: 20px;
        background: #fafafa;
        border: 1px solid #ddd;
        border-radius: 8px;
        max-height: 700px;
    }}

    .tree {{
        padding-left: 0;
        list-style-type: none;
        position: relative;
        font-family: monospace;
    }}

    .tree-vertical .tree ul::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 10px;
        border-left: 2px solid #ccc;
        height: 100%;
    }}

    .tree-vertical .tree li {{
        margin: 0;
        padding: 0 0 0 20px;
        position: relative;
    }}

    .tree-vertical .tree li::before {{
        content: '';
        position: absolute;
        top: 1em;
        left: 0;
        width: 20px;
        height: 0;
        border-top: 2px solid #ccc;
    }}

    .tree-horizontal .tree {{
        display: flex;
        flex-direction: row;
    }}

    .tree-horizontal .tree li {{
        list-style: none;
        padding: 0 20px;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    .tree-horizontal .tree li::before {{
        content: '';
        position: absolute;
        left: 50%;
        top: -20px;
        width: 0;
        height: 20px;
        border-left: 2px solid #ccc;
    }}

    .tree-horizontal .tree ul {{
        display: flex;
        justify-content: center;
        padding: 20px 0 0 0;
    }}

    .node {{
        cursor: pointer;
        display: inline-block;
        padding: 5px 10px;
        margin: 0.5em 0;
        background-color: #f0f0f0;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 14px;
        position: relative;
    }}

    .node:hover {{
        background-color: #ddd;
    }}

    .highlight {{
        background-color: {color};
        color: white;
        font-weight: bold;
        border-color: {color};
    }}
    </style>
    """
    components.html(html, height=750, scrolling=True)



if st.button("🔍 Compare Trees"):
    try:
        tree_a = json.loads(tree_a_input)
        tree_b = json.loads(tree_b_input)
        only_in_a, only_in_b = compare_trees_for_ui(tree_a, tree_b)

        # Extract unique node names
        unique_names_in_a = extract_node_ids(only_in_a)
        unique_names_in_b = extract_node_ids(only_in_b)

        tab1, tab2, tab3 = st.tabs(["🔴 Only in Tree A", "🟢 Only in Tree B", "⚪ Combined Tree"])

        with tab1:
            st.write(f"Found {len(unique_names_in_a)} unique node(s) in Tree A.")

            if display_mode == "Table View":
                st.dataframe(only_in_a)
            elif display_mode == "Tree View":
                render_tree(only_in_a)
            elif display_mode == "Visual Tree":
                display_visual_tree_with_highlight(tree_a, unique_names_in_a, "#e74c3c")  # red

        with tab2:
            st.write(f"Found {len(unique_names_in_b)} unique node(s) in Tree B.")

            if display_mode == "Table View":
                st.dataframe(only_in_b)
            elif display_mode == "Tree View":
                render_tree(only_in_b)
            elif display_mode == "Visual Tree":
                display_visual_tree_with_highlight(tree_b, unique_names_in_b, "#2ecc71")  # green

        with tab3:
            st.write("Combined Tree highlighting only-in-A (🔴), only-in-B (🟢), and both (⚪).")

            merged_tree = merge_trees(tree_a, tree_b)
            display_visual_tree_with_highlight(merged_tree, set(), "")  # No highlight set needed; handled per node

    except Exception as e:
        st.error(f"❌ Invalid JSON or comparison error: {e}")
