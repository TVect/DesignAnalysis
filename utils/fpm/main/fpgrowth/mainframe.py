#coding:utf8
'''
@author: chin
@date: 2016年6月16日
'''

class FpGrowthMethod(object):

    def __init__(self):
        self.support_dict = {}          # 支持度的dict
        self.frequent_list = []         # 频繁项集的list
        self.rules_list = []            # 关联规则的list

        self.item_list = []             # 项的list
        self.transaction_list = []      # 交易数据的list


    class TreeNode(object):
        def __init__(self, name, count, parent):
            self.name = name
            self.count = count
            self.node_link = None
            self.parent = parent      #needs to be updated
            self.children = {} 

        def incr(self, numOccur):
            self.count += numOccur

        def disp(self, ind=0):
            print '\t'*ind, self.name, ':', self.count
            for child in self.children.values():
                child.disp(ind+1)


    def load_data_from_file(self, filename, sep=","):
        with open(filename) as fr:
            for line in fr.readlines():
                transaction = []
                for item in line.strip().split(sep):
                    if item not in self.item_list:
                        self.item_list.append(item)
                    transaction.append(self.item_list.index(item))
                self.transaction_list.append(transaction)


    def create_init_data(self):
        trans_dict = {}
        for transaction in self.transaction_list:
            trans_dict[frozenset(transaction)] = trans_dict.get(frozenset(transaction), 0) + 1
        return trans_dict


    def create_fp_tree(self, trans_dict, min_supp):
        header_table = {}
        for transaction, count in trans_dict.iteritems():
            for item in transaction:
                header_table[item] = header_table.get(item, 0) + count
        header_table = filter(lambda item: item[1] >= min_supp, header_table.items())
        if not header_table:
            return None, None
        header_table = dict([[key, [value, None]] for key, value in header_table])
        
        fp_tree = FpGrowthMethod.TreeNode("root", 0, None)
        # 构建 FP-树
#         for transaction, count in trans_dict.items():
#             #用dict不用list，list会保持原有的部分顺序，会不适合
#             item_dict = dict([(item, header_table.get(item)[0]) for item in transaction if header_table.has_key(item)])
#             if item_dict:
#                 item_list = sorted(item_dict.items(), key=lambda item: item[1], reverse=True)   #这里有问题，相同的count时候，排序不稳定
#                 self.update_fp_tree(item_list, fp_tree, header_table, count)
        sorted_item_list = sorted(header_table.keys(), key = lambda item: header_table[item][0], reverse=True)
        for transaction, count in trans_dict.items():
            #保证每一次都是按sorted_item_list的顺序,防止在出现item的计数相同时，排序顺序不稳定
            item_list = [item for item in sorted_item_list if item in transaction]
            if item_list:
                self.update_fp_tree(item_list, fp_tree, header_table, count)
        return fp_tree, header_table


    def update_fp_tree(self, item_list, fp_tree, header_table, count):
        if item_list[0] in fp_tree.children:
            fp_tree.children[item_list[0]].incr(count)
        else:
            fp_tree.children[item_list[0]] = FpGrowthMethod.TreeNode(item_list[0], count, fp_tree)
            self.update_header_table(header_table, fp_tree.children[item_list[0]])

        if len(item_list) > 1:
            self.update_fp_tree(item_list[1:], fp_tree.children[item_list[0]], header_table, count)


    def update_header_table(self, header_table, fp_node):
        if header_table[fp_node.name][1] == None:
            header_table[fp_node.name][1] = fp_node
        else:
            node = header_table[fp_node.name][1]
            while node.node_link:
                node = node.node_link
            node.node_link = fp_node


    def gen_frequent(self, min_supp=3):
        trans_dict = self.create_init_data()
#         print trans_dict
        _, header_table = self.create_fp_tree(trans_dict, min_supp)
        self.mine_fp_tree(header_table, [], min_supp)
        return self.frequent_list


    def gen_associated_rules(self, min_conf=0.7):
        for frequent in self.frequent_list:
            righthand_list = [frozenset([item]) for item in frequent]
#             self._cal_and_filter_conf(frequent, righthand_list, min_conf)
            self._rules_from_conseq(frozenset(frequent), righthand_list, min_conf)


    def _cal_and_filter_conf(self, base_set, righthand_list, min_conf):
        '''
        计算置信度
        @param base_set: 关联规则左件和右件的并集
        @param righthand_list: 关联规则中右件的集合列表 
        @param min_conf: 最小置信度
        '''
        suitable_righthand = []
        for righthand in righthand_list:
            try:
                conf = float(self.support_dict[base_set]) / (self.support_dict[base_set-righthand])
            except Exception as e:
                print e
            if conf >= min_conf:
                self.rules_list.append((base_set-righthand, righthand, conf))
#                 print base_set-righthand,"--->" ,righthand, conf
                suitable_righthand.append(righthand)
        return suitable_righthand


    def _rules_from_conseq(self, base_set, righthand_list, min_conf):
        '''
        获取关联规则
        @param base_set: 关联规则左件和右件的并集
        @param righthand_list: 关联规则中右件的集合列表 
        @param min_conf: 最小置信度
        '''
        if not righthand_list:
            return
        if len(base_set) <= len(righthand_list[0]):
            return
        suitable_righthand_list = self._cal_and_filter_conf(base_set, righthand_list, min_conf)
        if suitable_righthand_list:
            suitable_righthand_list = self._gen_cand_from_large(suitable_righthand_list)
            self._rules_from_conseq(base_set, suitable_righthand_list, min_conf)


    def _gen_cand_from_large(self, large_list):
        '''
        从large_list中组合出新的备选k项集
        '''
        large_len = len(large_list)
        if large_len < 2:
            return
        k = len(large_list[0])
        cand_list = []
        for i in xrange(large_len):
            large_i = sorted(list(large_list[i]))
            for j in xrange(i+1, large_len):
                large_j = sorted(list(large_list[j]))
                if large_i[:k-1] == large_j[:k-1]:
                    cand_list.append(frozenset(large_i) | frozenset(large_j))
        return cand_list


    def ascend_tree(self, leaf_node, prefix_path):
        if leaf_node.parent != None:
    #         prefix_path.append(leaf_node)
            prefix_path.append(leaf_node.name)
            self.ascend_tree(leaf_node.parent, prefix_path)


    def find_prefix_paths(self, tree_node):
        cond_paths = {}
        while tree_node:
            prefix_path = []
            self.ascend_tree(tree_node, prefix_path)
    #         ret_paths.append(prefix_path)
            if len(prefix_path) > 1: 
                cond_paths[frozenset(prefix_path[1:])] = tree_node.count
            tree_node = tree_node.node_link
        return cond_paths


    def mine_fp_tree(self, header_table, prefix, min_supp):
        for item in header_table:
            if frozenset([item]) | frozenset(prefix) in self.frequent_list:
                print item, prefix
            else:
                self.frequent_list.append(frozenset([item]) | frozenset(prefix))  # 添加频繁项集
                self.support_dict[frozenset(set([item]) | frozenset(prefix))] = header_table[item][0]

        for key in header_table:
            cond_paths = self.find_prefix_paths(header_table[key][1])
            _, cond_header_table = self.create_fp_tree(cond_paths, min_supp)
            if cond_header_table:
                self.mine_fp_tree(cond_header_table, prefix + [key], min_supp)


    def show_frequent(self):
        for frequent in self.frequent_list:
            print [self.item_list[item] for item in frequent]


    def show_rules(self):
        for rule in self.rules_list:
            from_detail = [self.item_list[idx] for idx in rule[0]]
            to_detail = [self.item_list[idx] for idx in rule[1]]
            print from_detail, "--->", to_detail, "    :", rule[2]
