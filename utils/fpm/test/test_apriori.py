#coding:utf8
'''
@author: chin
@date: 2016年6月16日
'''

import sys
sys.path.append("..")

from main.apriori.mainframe import AprioriMethod

apriori_method = AprioriMethod()
apriori_method.load_data_from_file(filename = "test.txt")
apriori_method.gen_frequent(min_supp=3)


# apriori_method.load_data_from_file(filename = "../../sourcedata/plugin_no.txt")
# apriori_method.gen_frequent(min_supp=100)

# print apriori_method.transaction_list
# print apriori_method.item_list


print len(apriori_method.frequent_list)
print len(apriori_method.support_dict)

apriori_method.gen_associated_rules(min_conf=0.7)

apriori_method.show_rules()
