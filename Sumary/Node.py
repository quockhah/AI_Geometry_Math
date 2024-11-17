class Node:
    def __init__(self, concept):
        """_summary_

        Arguments:
            concept -- Node content
        """

        self.concept = concept.lower() 
        self.relationships = [] 

    def add_relationship(self, relation, target_node):
        """_summary_

        Arguments:
            relation -- Relation of node
            target_node -- Node have relationship with this node
        """

        self.relationships.append((relation, target_node))

    def get_relationships(self):
        """_summary_

        Returns:
            Node relationships
        """

        return self.relationships