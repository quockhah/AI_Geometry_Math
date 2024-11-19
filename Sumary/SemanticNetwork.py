from Node import Node

class SemanticNetwork:
    def __init__(self):
        self.nodes = []

    def add_concept(self, concept):
        """_summary_

        Arguments:
            concept -- Node content

        Returns:
            Node
        """

        for node in self.nodes:
            if node.concept == concept.lower():
                return node
        new_node = Node(concept)
        self.nodes.append(new_node)
        return new_node

    def add_relationship(self, concept1, relation, concept2):
        """_summary_

        Arguments:
            concept1 -- First node content
            relation -- Relationship between first node and second node
            concept2 -- Second node content
        """

        node1 = self.add_concept(concept1)
        node2 = self.add_concept(concept2)
        node1.add_relationship(relation, node2)

    def find_node(self, concept):
        """_summary_

        Arguments:
            concept -- Node content

        Returns:
            Node or None
        """

        for node in self.nodes:
            if node.concept.lower() == concept:
                return node
        return None

    def get_info(self, concept):
        """_summary_

        Arguments:
            concept -- Node content

        Returns:
            Info about input node content
        """

        node = self.find_node(concept)
        info=""
        if node:
            for relation, target in node.get_relationships():
                info += f"- {concept} {relation} {target.concept}\n"
            for rel,target in node.get_relationships():
                info += self.inherited_knowledge_with_relationship(target,concept)
            return info
        else:
            return f"Không tìm thấy khái niệm: {concept}"
        
    def search_by_relationship(self, concept, relation):
        """_summary_

        Arguments:
            concept -- Node content
            relation -- Relationship of node

        Returns:
            _description_
        """

        node = self.find_node(concept)
        self.get_info
        if node:
            results = []
            info=""
            for rel, target in node.get_relationships():
                if rel == relation:
                    results.append(target.concept)
            if results:
                for obj in results:
                    info += f"- {concept} {relation} {obj}\n"
            for rel,target in node.get_relationships():
                info += self.inherited_knowledge_with_relationship(target,concept)
            return info
        else:
            return f"Không tìm thấy khái niệm: {concept}"
        
    def inherited_knowledge_with_relationship(self, node,mainnode):
        """_summary_

        Arguments:
            node -- Node
            mainnode -- Root node which want to find node have relationship with it

        Returns:
            Content of node which have relationship with root node
        """

        inherited_results =""
        for rel, target in node.get_relationships():
                inherited_results+=f"- {mainnode} {rel} {target.concept} \n"
                node1=Node(target.concept)
                inherited_results += self.inherited_knowledge_with_relationship(node1,mainnode)
        return inherited_results
    
    def load_data(self, file_name):
        """_summary_

        Arguments:
            file_name -- Name of file have data to summary topic
        """

        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                concept1, relation, concept2 = line.strip().split(";")
                self.add_relationship(concept1, relation, concept2)

    def is_node(self, input):
        """_summary_

        Arguments:
            input -- Node content

        Returns:
            Input is node content or not
        """

        return self.find_node(input) is not None

    def is_relationship(self, concept, input):
        """_summary_

        Arguments:
            concept -- Node content
            input -- Relation

        Returns:
            Input is relation or not
        """

        node = self.find_node(concept)
        if node is not None:
            return any(rel == input for rel, _ in node.relationships)
        return False

    