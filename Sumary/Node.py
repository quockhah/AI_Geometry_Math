class Node:
    def __init__(self, concept):
        self.concept = concept.lower() 
        self.relationships = [] 

    def add_relationship(self, relation, target_node):
        self.relationships.append((relation, target_node))

    def get_relationships(self):
        return self.relationships