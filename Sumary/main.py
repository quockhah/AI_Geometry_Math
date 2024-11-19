from SemanticNetwork import *

test = SemanticNetwork()
test.load_data("./Sumary/data.txt")
print(test.nodes[1].concept)