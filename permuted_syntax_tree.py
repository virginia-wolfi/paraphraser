from itertools import permutations

import nltk


class PermutedSyntaxTree:
    """
    A class to generate permutations of a syntax tree based on specific tagged nodes and conjunctions.

    The class traverses the syntax tree recursively from lower-level subtrees to higher-level subtrees to find all possible permutations.

    Attributes:
        CONJUNCTIONS (tuple): A tuple of conjunction labels to consider for permutations.
        TAGS (tuple): A tuple of subtree tags to consider for permutations.
        tree (nltk.Tree): The syntax tree represented as a nltk.Tree object.
        tagged_nodes_positions (dict): A dictionary storing positions of tagged subtrees that can be permuted.
        tagged_nodes_keys (list): A list of keys representing the positions of tagged subtrees.
        max_depth (int): The depth of nested tagged subtrees.
    """

    CONJUNCTIONS = (",", "CC")
    TAGS = ("NP", "NN", "N", "NNS", "VP", "UCP", "S")

    def __init__(self, syntax_tree: str) -> None:
        """
        Initializes the PermutedSyntaxTree with a syntax tree string.
        """

        self.tree = nltk.Tree.fromstring(syntax_tree)
        self.tagged_nodes_positions = dict()
        self.find_permutable_positions()
        self.tagged_nodes_keys = list(self.tagged_nodes_positions)
        self.max_depth = len(self.tagged_nodes_keys)
        self.all_permuted_trees = []

    def find_permutable_positions(self, conj_set=CONJUNCTIONS, tags=TAGS) -> None:
        """
        Finds and stores the positions of tagged subtrees that can be permuted.
        """

        tree = nltk.ParentedTree.convert(self.tree)
        subtrees = tree.subtrees(lambda t: t.label() in tags)
        for node in subtrees:
            # The right sibling must be a conjunction
            conj = node.right_sibling()
            while conj and conj.label() in conj_set:
                next_sibling = conj.right_sibling()
                if next_sibling and next_sibling.label() in tags:
                    pos = node.treeposition()[:-1]
                    permutable_positions = self.tagged_nodes_positions.setdefault(
                        pos, []
                    )
                    if node.treeposition() not in permutable_positions:
                        permutable_positions.extend(
                            [
                                node.treeposition(),
                                next_sibling.treeposition(),
                            ]
                        )
                    else:
                        permutable_positions.append(next_sibling.treeposition())
                conj = next_sibling  # move to the next conjunction if present

    def permute_subtrees_at_depth(self, tree: nltk.Tree, depth) -> list[nltk.Tree]:
        """
        Generates all permutations of the tagged subtrees at a specific depth.
        """

        permuted_trees = []
        current_node_key = self.tagged_nodes_keys[depth]
        node_positions = self.tagged_nodes_positions[current_node_key]
        subtrees_to_permute = [tree[pos] for pos in node_positions]
        tree_permutations = list(permutations(subtrees_to_permute))
        # Exclude the first permutation to avoid redundant processing of previously permuted subtrees
        # We do not exclude the first permutation at max nesting depth
        # to ensure all permutations are generated at the deepest level
        if depth < self.max_depth - 1:
            tree_permutations = tree_permutations[1:]
        for permutation in tree_permutations:
            new_tree = nltk.tree.Tree.convert(tree)
            for i, pos in enumerate(node_positions):
                new_tree[pos] = permutation[i]
            permuted_trees.append(new_tree)
        return permuted_trees

    def get_all_permutations(self) -> list[nltk.Tree]:
        """
        Recursively generates all possible permutations of the syntax tree.
        """

        def traverse_and_permute(tree: nltk.Tree, depth=self.max_depth - 1):
            if depth == -1:
                return
            else:
                permuted_trees = self.permute_subtrees_at_depth(tree, depth)
                self.all_permuted_trees.extend(permuted_trees)
                for permuted_tree in permuted_trees:
                    traverse_and_permute(permuted_tree, depth - 1)

        traverse_and_permute(self.tree)
        return self.all_permuted_trees

    def get_permutations_as_string(self) -> list[str]:
        permutations = self.all_permuted_trees
        if not permutations:
            permutations = self.get_all_permutations()
        return [" ".join(tree.leaves()) for tree in permutations]
