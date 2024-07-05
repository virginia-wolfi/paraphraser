from itertools import permutations

import nltk

class PermutedSyntaxTree:
    """
    A class to generate permutations of a syntax tree based on specific tagged nodes and conjunctions.

    This class traverses the syntax tree recursively from lower-level subtrees to higher-level subtrees
    to find all possible permutations. It considers specific tag groups to ensure permutations are meaningful
    and syntactically valid.

    Attributes:
        CONJUNCTIONS (tuple): A tuple of conjunction labels to consider for permutations.
        TAG_GROUPS (list of tuples): A list of tuples where each tuple contains tags to consider for permutations together.
        tree (nltk.Tree): The syntax tree represented as an nltk.Tree object.
        tagged_nodes_positions (dict): A dictionary storing positions of tagged subtrees that can be permuted.
        tagged_nodes_keys (list): A list of keys representing the positions of tagged subtrees.
        max_depth (int): The depth of nested tagged subtrees.
        all_permuted_trees (list): A list to store all permutations of the syntax tree.
    """

    CONJUNCTIONS = (",", "CC")
    TAG_GROUPS = [
        ("NN", "NNS", "N", "NNP"),             # Singular and plural nouns
        ("NP", "NPS"),                  # Noun phrases
        ("VB", "VBD", "VBG", "VBN", "VBP", "VBZ"),  # Verb forms
        ("VP",),                        # Verb phrases
        ("ADJP", "UCP"),                # Adjective phrases
        ("JJ", "JJR", "JJS"),           # Adjectives
        ("RB", "RBR", "RBS"),           # Adverbs
        ("S",),                         # Sentences                # Prepositional phrases
        ("DT", "PDT", "WDT"),           # Determiners
        ("PRP", "PRP$", "WP", "WP$"),   # Pronouns
        ("CD",),                        # Cardinals (numbers)
        ("CC",),                        # Coordinating conjunctions
        ("UH",),                        # Interjections
        ("MD",),                        # Modal verbs
        ("EX",),                        # Existential 'there'
        ("SYM",),                       # Symbols
        ("FW",)                         # Foreign words
    ]

    def __init__(self, syntax_tree: str) -> None:
        """
        Initializes the PermutedSyntaxTree with a syntax tree string.
        """

        self.tree = nltk.Tree.fromstring(syntax_tree)
        self.tagged_nodes_positions = dict()
        self.find_permutable_positions()
        self.tagged_nodes_keys = sorted(list(self.tagged_nodes_positions))
        self.max_depth = len(self.tagged_nodes_keys)
        self.all_permuted_trees = []

    def find_permutable_positions(self, conj_set: tuple[str] = CONJUNCTIONS, tag_groups: list[tuple] = TAG_GROUPS) -> None:
        """
        Finds and stores the positions of tagged subtrees that can be permuted.
        """

        tree = nltk.ParentedTree.convert(self.tree)
        for tags in tag_groups:
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

    def permute_subtrees_at_depth(self, tree: nltk.Tree, depth: int) -> list[nltk.Tree]:
        """
        Generates all permutations of the tagged subtrees at a specific depth.
        """

        permuted_trees = []
        current_node_key = self.tagged_nodes_keys[depth]
        node_positions = self.tagged_nodes_positions[current_node_key]
        subtrees_to_permute = [tree[pos] for pos in node_positions]

        tree_permutations = list(permutations(subtrees_to_permute))
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

        def traverse_and_permute(tree: nltk.Tree, depth: int = self.max_depth - 1):
            if depth == -1:
                self.all_permuted_trees.append(tree)
            else:
                permuted_trees = self.permute_subtrees_at_depth(tree, depth)
                for permuted_tree in permuted_trees:
                    traverse_and_permute(permuted_tree, depth - 1)

        traverse_and_permute(self.tree)
        return self.all_permuted_trees

    def get_permutations_as_string(self) -> list[str]:
        """
        Returns all permutations as strings, ensuring proper spacing and punctuation.

        Returns:
            list[str]: A list of strings representing all permuted syntax trees.
        """
        permutations = self.all_permuted_trees
        if not permutations:
            permutations = self.get_all_permutations()

        result = []
        punctuation_marks = [",", ".", "!", "?", ";", ":"]
        for tree in permutations:
            sentence = " ".join(tree.leaves())
            for mark in punctuation_marks:
                sentence = sentence.replace(f" {mark}", mark)
            result.append(sentence)

        return sorted(result)


