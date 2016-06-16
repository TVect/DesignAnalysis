#coding:utf8
'''
@author: chin
@date: 2016年6月16日
'''

class AprioriMethod(object):

    def __init__(self):
        self.support_dict = {}          # 支持度的dict
        self.frequent_list = []         # 频繁项集的list
        self.rules_list = []            # 关联规则的list

        self.item_list = []             # 项的list
        self.transaction_list = []      # 交易数据的list


    def load_data_from_file(self, filename, sep=","):
        with open(filename) as fr:
            for line in fr.readlines():
                transaction = []
                for item in line.strip().split(sep):
                    if item not in self.item_list:
                        self.item_list.append(item)
                    transaction.append(self.item_list.index(item))
                self.transaction_list.append(transaction)


    def gen_frequent(self, min_supp=3):
        '''
        生成频繁项集
        '''
        cand_list = self._gen_cand_1()
        while True:
            large_list, large_supp_dict = self._filter_cand_to_large(cand_list, min_supp)
            cand_list = self._gen_cand_from_large(large_list)
            self.frequent_list.append(large_list)
            self.support_dict.update(large_supp_dict)
            if not cand_list:
                return


    def gen_associated_rules(self, min_conf=0.7):
        '''
        生成关联规则
        '''
        freq_k_max = len(self.frequent_list)
        for k in xrange(2, freq_k_max+1):
            large_list = self.frequent_list[k-1]
            if k == 2:
                for large in large_list:
                    righthand_list = [frozenset([item]) for item in large]
                    self._cal_and_filter_conf(large, righthand_list, min_conf)
            else:
                for large in large_list:
                    righthand_list = [frozenset([item]) for item in large]
                    self._rules_from_conseq(large, righthand_list, min_conf)


    def show_rules(self):
        for rule in self.rules_list:
            from_detail = [self.item_list[idx] for idx in rule[0]]
            to_detail = [self.item_list[idx] for idx in rule[1]]
            print from_detail, "--->", to_detail, "    :", rule[2]


    def _cal_and_filter_conf(self, base_set, righthand_list, min_conf):
        '''
        计算置信度
        @param base_set: 关联规则左件和右件的并集
        @param righthand_list: 关联规则中右件的集合列表 
        @param min_conf: 最小置信度
        '''
        suitable_righthand = []
        for righthand in righthand_list:
            conf = float(self.support_dict[base_set]) / (self.support_dict[base_set-righthand])
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


    def _gen_cand_1(self):
        '''
        @return: 候选1-项集, frozenset保证其可作为dict的key值
        '''
        return [frozenset([item]) for item in range(len(self.item_list))]


    def _filter_cand_to_large(self, cand_list, min_supp):
        '''
        从cand_list中过滤出频繁项集large_list
        '''
        supp_cnt = {}
        for transaction in self.transaction_list:
            for cand in cand_list:
                if cand.issubset(transaction):
                    supp_cnt[cand] = supp_cnt[cand] + 1 if supp_cnt.has_key(cand) else 1
        large_list = []
        large_supp_dict = {}
        for cand, supp in supp_cnt.items():
            if supp >= min_supp:
                large_list.append(cand)
                large_supp_dict[cand] = supp
        return large_list, large_supp_dict


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
