#coding:utf8
'''
@author: chin
@date: 2016年6月20日
'''

class SortedLinkedList(object):
    def __init__(self):
        self.head = SortedLinkedNode("root", 0)

#     def add_node(self, no, priority):
#         pointer = self.head
#         while pointer.next:
#             if pointer.next.priority >= priority:
#                 node = SortedLinkedNode(no, priority)
#                 node.next = pointer.next
#                 pointer.next = node
#                 break
#             pointer = pointer.next
#         else:
#             pointer.next = SortedLinkedNode(no, priority)
#     
    
    def add_node(self, node):
        pointer = self.head
        while pointer.next:
            if pointer.next.priority >= node.priority:
                node.next = pointer.next
                pointer.next = node
                break
            pointer = pointer.next
        else:
            pointer.next = node
            node.next = None

    def pop_node(self, no):
        pointer = self.head
        while pointer.next:
            if pointer.next.no == no:
                ret_node = pointer.next
                pointer.next = pointer.next.next
                return ret_node
            pointer = pointer.next
        return None
    
    def get_node(self, no):
        pointer = self.head
        while pointer.next:
            if pointer.next.no == no:
                return pointer.next
            pointer = pointer.next
        return None

    def find_least_node(self, priority):
        '''
        寻找最小的no，priority使得其和大于priority
        '''
        pointer = self.head
        node_list = []
        priority_sum = 0.0
        while pointer.next:
            pointer = pointer.next
            node_list.append(pointer)
            priority_sum += pointer.priority
            if priority_sum >= priority:
                break
        else:
            return node_list  # 成功找到一系列的no，使得它们的priority之和刚好大于priority
        return None # 无法找到符合条件的no_list，也就是说所有priority之和也还比priority要小

        
class SortedLinkedNode(object):
    def __init__(self, no, priority):
        self.next = None
        self.no = no
        self.priority = priority
