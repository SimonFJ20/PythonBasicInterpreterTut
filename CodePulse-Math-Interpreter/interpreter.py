from nodes import *
from values import Number

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)

    def visit_NumberNode(self, node: NumberNode):
        return Number(node.value)

    def visit_AddNode(self, node: AddNode):
        return Number(self.visit(node.node_a).value + self.visit(node.node_b).value)

    def visit_SubtractNode(self, node: SubtractNode):
        return Number(self.visit(node.node_a).value - self.visit(node.node_b).value)

    def visit_MultiplyNode(self, node: MultiplyNode):
        return Number(self.visit(node.node_a).value * self.visit(node.node_b).value)

    def visit_DivideNode(self, node: DivideNode):
        try:
            return Number(self.visit(node.node_a).value / self.visit(node.node_b).value)
        except ZeroDivisionError:
            raise Exception('Runtime math error')

    def visit_PlusNode(self, node: PlusNode):
        return self.visit(node.node).value

    def visit_MinusNode(self, node: MinusNode):
        return Number(-self.visit(node.node).value)
