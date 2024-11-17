class SemanticNetwork:
    def __init__(self):
        self.nodes = []

    def add_concept(self, concept):
        for node in self.nodes:
            if node.concept == concept.lower():
                return node
        new_node = Node(concept)
        self.nodes.append(new_node)
        return new_node

    def add_relationship(self, concept1, relation, concept2):
        node1 = self.add_concept(concept1)
        node2 = self.add_concept(concept2)
        node1.add_relationship(relation, node2)

    def find_node(self, concept):
        for node in self.nodes:
            if node.concept.lower() == concept:
                return node
        return None

    def get_info(self, concept):
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
        node = self.find_node(concept)
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
        inherited_results =""
        for rel, target in node.get_relationships():
                inherited_results+=f"- {mainnode} {rel} {target.concept} \n"
                node1=Node(target.concept)
                inherited_results += self.inherited_knowledge_with_relationship(node1,mainnode)
        return inherited_results
    
    def load_data(self, file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                concept1, relation, concept2 = line.strip().split(";")
                self.add_relationship(concept1, relation, concept2)

    def is_node(self, concept):
        return self.find_node(concept) is not None

    def is_relationship(self, concept, relation):
        node = self.find_node(concept)
        if node is not None:
            return any(rel == relation for rel, _ in node.relationships)
        return False

    