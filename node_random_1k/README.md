# 项目说明  
## 功能描述：    
置乱网络中的每一个节点生成新网络并保存置乱后的网络
## 流程描述：  
1、读取原始网络数据；  
2、获取待置乱节点的所有连边；  
3、计算原始网络的节点度的累积分布；  
4、保证在度分布不变的随机选取两条（u-v和x-y）；  
5、保证随机选取的边，一条为待置乱节点的连边（u-v），另一条不为其连边（x-y）；  
6、断开旧边（u-v和x-y），生成新边（u-y和v-x）；  
7、保证生成的u-y不为原始网络中待置乱节点的任何一条连边，保证v-x不为原始网络中与待置乱节点不相连的任何一条边；  
8、保证生成的两条新边为原始网络中不存在的边；  
9、否则撤销断边重连操作；  
10、判断是否与原始网络的连通性保持一致，否则撤销操作；  
11、保证待置乱节点的所有边均被置乱，保存新网络。或者，调用node_random次数超过200次仍没有将节点的所有连边置乱则不再调用直接保存新网络。  
## 相关说明   
brain_71.txt为原始网络即测试网络  
node_random_1k_test.py为测试程序  
changed_network_node0-changed_network_node70为置乱节点0-节点70对应生成的新网络  
compared_featur.csv为保存原始网络和置乱不同节点后的新网络的四种统计特征的值（平均最短路径l、平均聚类系数c、匹配系数r、模块度Q）  
distance.csv为不同节点的四种统计特征与原始网络统计特征的差值  
