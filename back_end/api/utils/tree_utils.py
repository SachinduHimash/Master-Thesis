import uuid
from threading import Lock
from collections import defaultdict

# Global dictionary to store trees
trees = defaultdict(lambda: None)
lock = Lock()

class TreeNode:
    def __init__(self, name, value=0.0, alpha_cut=0.0, prompt=""):
        self.name = name  # Name of the node
        self.value = value  # Value of the node
        self.alpha_cut = alpha_cut  # Alpha cut value for second-level nodes
        self.prompt = prompt  # Prompt for leaf nodes
        self.children = []  # Children nodes

    def add_child(self, child_node):
        """Add a child node to the current node."""
        self.children.append(child_node)

    def update_value(self, new_value):
        """Update the value of the current node."""
        self.value = new_value
    
    def update_alpha_cut(self, new_alpha_cut):
        """Update the value of the current node."""
        self.alpha_cut = new_alpha_cut

    def __str__(self):
        children_str = ", ".join(child.name for child in self.children)
        return f"Node(name={self.name}, value={self.value}, alpha_cut={self.alpha_cut}, prompt={self.prompt}),children=[{children_str}])"
    
    def to_dict(self):
        """Convert the TreeNode object to a JSON-serializable dictionary."""
        return {
            "name": self.name,
            "value": self.value,
            "alpha_cut": self.alpha_cut,
            "prompt": self.prompt,
            "children": [child.to_dict() for child in self.children]  # Recursively convert children
        }


class TreeManager:
 
    @staticmethod
    
    def build_tree():
          with lock:
            tree_id = str(uuid.uuid4())
            
            # Root node
            humanity = TreeNode(name="Humanity")
            alpha_cut = 40
            # First level nodes
            focus_on_life = TreeNode(name="Focus on Life and Well-being",alpha_cut=alpha_cut)
            targeting_vulnerable_populations = TreeNode(name="Targeting Vulnerable Populations",alpha_cut=alpha_cut)
            comprehensive_care = TreeNode(name="Comprehensive Care",alpha_cut=alpha_cut)
            preserving_dignity = TreeNode(name="Preserving Dignity",alpha_cut=alpha_cut)


            # Adding first level TreeNodes as children to the root node
            humanity.add_child(focus_on_life)
            humanity.add_child(targeting_vulnerable_populations)
            humanity.add_child(comprehensive_care)
            humanity.add_child(preserving_dignity)

            trees[tree_id] = humanity
            
            return tree_id

    @staticmethod
    def get_tree(tree_id):
        """
        Retrieve the tree for the given ID.
        """
        return trees.get(tree_id).to_dict()
    
    @staticmethod
    def get_node(tree_id,node_name):
        root = trees.get(tree_id)
        if not root:
            raise ValueError(f"Tree with ID {tree_id} does not exist.")
        
        def find_node_by_name(node, name):
            if node.name == name:
                return node
            for child in node.children:
                found = find_node_by_name(child, name)
                if found:
                    return found
            return None

        node = find_node_by_name(root, node_name)
        
        return node
    
    @staticmethod
    def add_child_node(tree_id, parent_name, child_name, child_value=None, child_prompt="", child_alpha_cut=0.0):
        root = trees.get(tree_id)
        if not root:
            raise ValueError(f"Tree with ID {tree_id} does not exist.")

        # Helper function to find a node by its name
        def find_node_by_name(node, name):
            if node.name == name:
                return node
            for child in node.children:
                found = find_node_by_name(child, name)
                if found:
                    return found
            return None

        # Locate the parent node
        parent_node = find_node_by_name(root, parent_name)
        if not parent_node:
            raise ValueError(f"Parent node with name {parent_name} not found in tree {tree_id}.")

        # Create the new child node
        child_node = TreeNode(
            name=child_name,
            value=child_value if child_value is not None else 0.0,  # Default to 0.0 if no value is provided
            prompt=child_prompt,
            alpha_cut=child_alpha_cut,
        )

        # Add the child node to the parent's children list
        parent_node.add_child(child_node)

        
    @staticmethod
    def add_or_update_node(tree_id,parent_name=None, node_name="", value=0.0,prompt="",alpha_cut=0.0):
        """
        Adds a new node if it does not exist or updates it if it does.

        Parameters:
            tree_id (str): The ID of the tree.
            node_name (str): Name of the node.
            value (float): Value of the node (default=0.0).
            alpha_cut (float): Alpha cut value (default=0.0).
            prompt (str): Prompt for the node (default="").
            parent_name (str, optional): Name of the parent node. If None, the node is added under the root.
        """

        root = trees.get(tree_id)
        if not root:
            raise ValueError(f"Tree with ID {tree_id} does not exist.")

        # Recursive function to find a node by name
        def find_node(node, name):
            if node.name == name:
                return node
            for child in node.children:
                found = find_node(child, name)
                if found:
                    return found
            return None

        # Check if the node exists
        existing_node = find_node(root, node_name)
        if existing_node:
            # Update existing node
            existing_node.update_value(value)
            existing_node.update_alpha_cut(alpha_cut)
        else:
        # If the node doesn't exist, add it as a child under the specified parent or root
            parent_node = root if parent_name is None else find_node(root, parent_name)
            if not parent_node:
                raise ValueError(f"Parent node with name '{parent_name}' not found.")

            # Create and add the new node
            new_node = TreeNode(name=node_name, value=value, alpha_cut=alpha_cut, prompt=prompt)
            parent_node.add_child(new_node)
    
    @staticmethod
    # Function to find a node by name and update its value
    def update_node_value_by_name(tree_id, target_name, new_value):
        """Recursively find a node by name and update its value."""
        root = trees[tree_id]
        if root is None:
            print(f"Tree with ID {tree_id} not found.")
            return False

        # Recursive function to search and update the node
        def find_and_update(node):
            if node.name == target_name:
                
                node.update_value(new_value)
                return True  # Node found and updated

            for child in node.children:
                if find_and_update(child):
                    return True  # Node found and updated in a child

            return False  # Node not found in this branch

        # Start the search and update from the root node
        return find_and_update(root)
    
    @staticmethod
    # Function to find a node by name and update its value
    def update_node_alpha_cut_by_name(tree_id, target_name, new_alpha_cut):
        """Recursively find a node by name and update its value."""
        root = trees[tree_id]
        if root is None:
            print(f"Tree with ID {tree_id} not found.")
            return False

        # Recursive function to search and update the node
        def find_and_update_alpha_cut(node):
            if node.name == target_name:
                
                node.update_alpha_cut(new_alpha_cut)
                return True  # Node found and updated

            for child in node.children:
                if find_and_update_alpha_cut(child):
                    return True  # Node found and updated in a child

            return False  # Node not found in this branch

        # Start the search and update from the root node
        return find_and_update_alpha_cut(root)


    
    @staticmethod
    def find_node_with_max_diff_and_least_leaf_value(tree_id):
        root = trees[tree_id]
        max_diff_node = None
        max_diff = -1

        # Find the first-level node with the maximum difference between value and alpha_cut
        for first_level_node in root.children:
            print("max_diff",max_diff)
            if(first_level_node.value != 0.0 and first_level_node.value < first_level_node.alpha_cut):
                diff = abs(first_level_node.value - first_level_node.alpha_cut)
                if diff > max_diff:
                    max_diff = diff
                    max_diff_node = first_level_node

        

        # Once the node with the max difference is found, find its child node with the maximum difference
        if max_diff_node:
            print("max_diff_node:",max_diff_node.name)
            # Initialize variables for the child node with the maximum difference
            max_diff_child = None
            child_max_diff = -1
            for child in max_diff_node.children:
                print("value:",child.value,"alpha_cut:",child.alpha_cut)
                if(child.value < child.alpha_cut):
                    child_diff = abs(child.value - child.alpha_cut)
                    
                    print("child_diff:",child_diff,"child_max_diff:",child_max_diff)
                    if child_diff > child_max_diff:
                        child_max_diff = child_diff
                        max_diff_child = child

            # Find the leaf node with the least value under max_diff_node
            least_value_leaf = None
            min_value = float('inf')

            def traverse_leaf(node):
                nonlocal least_value_leaf, min_value
                if not node.children:  # It's a leaf node
                    if node.value < min_value:
                        min_value = node.value
                        least_value_leaf = node
                else:
                    for child in node.children:
                        traverse_leaf(child)

            traverse_leaf(max_diff_node)

            # Return both the child node with the max difference and the leaf node with the least value
            return {
                "max_diff_child": (max_diff_child) if max_diff_child else None,
                "least_value_leaf": (least_value_leaf) if least_value_leaf else None
            }

        return None  # If no such nodes are found


    @staticmethod
    def delete_tree(tree_id):
        """
        Delete the tree associated with the given ID.
        """
        with lock:
            if tree_id in trees:
                del trees[tree_id]
                
    @staticmethod
    def print_tree(tree_id):
        root = trees.get(tree_id)
        if not root:
            raise ValueError(f"Tree with ID {tree_id} does not exist.")
        
        # Recursive function to print the node and its children
        def print_node(node, indent=0):
            print(f"{' ' * indent}Node(name={node.name}, value={node.value}, alpha_cut={node.alpha_cut}, prompt={node.prompt})")
            for child in node.children:
                print_node(child, indent + 4)  # Increase indentation for child nodes
        
        # Start printing from the root node
        print_node(root)