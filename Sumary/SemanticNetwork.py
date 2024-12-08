from Node import Node

class SemanticNetwork:

    def __init__(self):
        """_summary_
        Initializes an empty semantic network.
        """
        self.nodes = []

    def add_concept(self, concept):
        """_summary_
        Adds a new concept node to the network if it doesn't already exist.

        Arguments:
            concept (str): The name of the concept to add.

        Returns:
            Node: The node corresponding to the concept.
        """
        for node in self.nodes:
            if node.concept == concept.lower():
                return node
        new_node = Node(concept)
        self.nodes.append(new_node)
        return new_node

    def add_relationship(self, concept1, relation, concept2):
        """_summary_
        Adds a relationship between two concepts.

        Arguments:
            concept1 (str): The first concept.
            relation (str): The type of relationship.
            concept2 (str): The second concept.
        """
        node1 = self.add_concept(concept1)
        node2 = self.add_concept(concept2)
        node1.add_relationship(relation, node2)

    def find_node(self, concept):
        """_summary_
        Finds a node by its concept name.

        Arguments:
            concept (str): The name of the concept to find.

        Returns:
            Node or None: The node corresponding to the concept, or None if not found.
        """
        for node in self.nodes:
            if node.concept.lower() == concept:
                return node
        return None

    def get_info(self, concept):
        """_summary_
        Retrieves detailed information about a concept and its relationships.

        Arguments:
            concept (str): The name of the concept to retrieve information about.

        Returns:
            str: A formatted string of relationships and inherited knowledge.
        """
        node = self.find_node(concept)
        info = ""
        if node:
            for relation, target in node.get_relationships():
                info += f"- {concept} {relation} {target.concept}\n"
            for rel, target in node.get_relationships():
                info += self.inherited_knowledge_with_relationship(target, concept)
            return info
        else:
            return f"Không tìm thấy khái niệm: {concept}"

    def inherited_knowledge_with_relationship(self, node, mainnode):
        """_summary_
        Recursively gathers inherited knowledge for a node.

        Arguments:
            node (Node): The node to explore.
            mainnode (str): The root node to trace relationships.

        Returns:
            str: A formatted string of inherited knowledge.
        """
        inherited_results = ""
        for rel, target in node.get_relationships():
            inherited_results += f"- {mainnode} {rel} {target.concept} \n"
            node1 = Node(target.concept)
            inherited_results += self.inherited_knowledge_with_relationship(node1, mainnode)
        return inherited_results

    def is_node(self, input):
        """_summary_
        Checks if a given input corresponds to an existing node.

        Arguments:
            input (str): The concept name to check.

        Returns:
            bool: True if the input corresponds to a node, False otherwise.
        """
        return self.find_node(input) is not None

    def is_relationship(self, concept, input):
        """_summary_
        Checks if a given relationship exists for a specific concept.

        Arguments:
            concept (str): The concept name.
            input (str): The relationship to check.

        Returns:
            bool: True if the relationship exists, False otherwise.
        """
        node = self.find_node(concept)
        if node is not None:
            return any(rel == input for rel, _ in node.relationships)
        return False

    def load_data(self, file_name):
        """_summary_
        Loads semantic network data from a file.

        Arguments:
            file_name (str): The name of the file containing the data.
        """
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                concept1, relation, concept2 = line.strip().split(";")
                self.add_relationship(concept1, relation, concept2)

    def search_by_relationship(self, concept, relation):
        """_summary_
        Searches for nodes with a specific relationship to a given concept.

        Arguments:
            concept (str): The concept to search from.
            relation (str): The relationship type to search for.

        Returns:
            str: A formatted string of results or an error message if the concept is not found.
        """
        node = self.find_node(concept)
        if node:
            results = []
            info = ""
            for rel, target in node.get_relationships():
                if rel == relation:
                    results.append(target.concept)
            if results:
                for obj in results:
                    info += f"- {concept} {relation} {obj}\n"
            for rel, target in node.get_relationships():
                info += self.inherited_knowledge_with_relationship(target, concept)
            return info
        else:
            return f"Không tìm thấy khái niệm: {concept}"
