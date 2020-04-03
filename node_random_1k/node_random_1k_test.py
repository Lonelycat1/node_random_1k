# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 15:31:52 2020

@author: LX
"""
import networkx as nx
import pandas as pd
import random
import copy

'''
###################################################
#函数名称：text_save
#功能：文本文件保存
#输入参数：
#        参数1：content(待保存内容)
#        参数2：filename(待生成文件名称)
#        参数3：mode(文件打开模式，默认'a'追加)
#输出参数：X(返回纠错后的新种群)
###################################################
'''       
def text_save(content,filename,mode='a'):
   file = open(filename,mode)
   for edge in content:
        node_1 = str(edge[0])
        node_2 = str(edge[1])        
        file.write(node_1+' '+node_2+'\n')
   file.close()

def load_Graph(filename):
    #读入网络数据
    network = open(filename)            #
    network = network.read()
    #生成无向图
    G = nx.Graph()    
    line = network.split('\n')          #用回车符分裂字符串,得到每一行的数据   
    for i in range(0,len(line)-1):
        pair_node = line[i].split()     #用空格分裂得到节点对    
        node_1 = int(pair_node[0])      #得到第一个节点
        node_2 = int(pair_node[1])      #得到第二个节点
        G.add_edge(node_1,node_2)       #添加边至空网络
    
    return G


def load_Graph_str(filename):
    #读入网络数据
    network = open(filename)            #
    network = network.read()
    #生成无向图
    G = nx.Graph()    
    line = network.split('\n')          #用回车符分裂字符串,得到每一行的数据   
    for i in range(0,len(line)-1):
        pair_node = line[i].split()     #用空格分裂得到节点对    
        node_1 = str(pair_node[0])      #得到第一个节点
        node_2 = str(pair_node[1])      #得到第二个节点
        G.add_edge(node_1,node_2)       #添加边至空网络
    
    return G
'''
###################################################
#函数名称：node_random_1k
#功能：1阶随机节点置乱
#输入参数：
        参数1：node(待置乱节点)
        参数2：G0(待改变结构网络)
        参数3：nswap(改变成功的系数，默认值为1)
        参数4：maxtries(最大尝试次数，默认值为2)
        参数5：connected(网络的联通特性，参数为1需要保持，参数为0不需要保持)
#输出参数：G(改变结构后的网络)
###################################################
'''
def node_random_1k(node,G0,nswap=1,max_tries=100,connected=1):
    #约束条件1
    if not nx.is_connected(G0):
        raise nx.NetworkXError("非连通图，必须为连通图")
    #约束条件2
    if G0.is_directed():
        raise nx.NetworkXError("仅适用于无向图")
    #约束条件3
    if nswap > max_tries:
        raise nx.NetworkXError("交换次数超过允许的最大次数")
    #约束条件4
    if len(G0) < 3:
        raise nx.NetworkXError("节点数太少，至少要含三个节点")    
        
    #变量初始化
    tries_count = 0           #尝试次数计数器
    swap_count = 0          #交换次数计数器
    node_neighbors_list = []

    G = nx.Graph()
    G = copy.deepcopy(G0)   #复制待改变网络
    
    #计算改变前的度分布
    keys,degrees = zip(*G.degree())         #keys为节点列表，degrees为对应的度列表
    cdf = nx.utils.cumulative_distribution(degrees) #计算度的累计分布
    
    #找到待置乱节点的所有连边
    node_neighbors_list = list(G.neighbors(node))   #待置乱节点的所有邻居节点
    select_node_edges = [(node,neighbor_node) for neighbor_node in node_neighbors_list ]
    
    #找到与待置乱节点node不相连的边
    reamin_edges = set(G.edges()).difference(set(select_node_edges))
    
    while swap_count < nswap:
        
        if tries_count >= max_tries:
            e = '尝试次数 (%s) 已超过允许的最大次数,'%tries_count + '当前有效交换次数为：（%s)'%swap_count
            print(e)
            break
        
        tries_count = tries_count + 1
        
        #在保证度分布不变的情况下，随机选取两条连边u-v，x-y
        (ui,xi)=nx.utils.discrete_sequence(2,cdistribution=cdf)
        #保证随机选取的边不为同一条边且必须有一条为待置乱节点的连边
        if ui==xi or ui != keys.index(node):
            continue
        
        #u-v为待置乱节点node的其中一条连边,x-y为随机选取的与node不相连的边
        u = keys[ui] 
        x = keys[xi]
        v = random.choice(list(G[u]))
        y = random.choice(list(G[x]))
        
        #保证是四个独立节点
        if len(set([u,v,x,y])) == 4:        
            #保证选取的边u-v为与node相连的边，x-y为与node不相连的边
            if (u,v) in select_node_edges and (x,y) in reamin_edges:       
                #保证新生成的边为u-y为 select_node_edges中不存在的边， 且v-x为reamin_edges中不存在的边
                if(u,y) not in select_node_edges and (v,x) not in reamin_edges:
                    #保证新生成的边为改变前网络中不存在的边
                    if (y not in G[u]) and (v not in G[x]):
                        G.add_edge(u,y)                           #增加两条新连边
                        G.add_edge(v,x)
                         
                        G.remove_edge(u,v)                        #删除两条旧连边
                        G.remove_edge(x,y)
                
                       #判断是否需要保持联通特性，为1的话则需要保持该特性
                        if connected == 1:
                            #保证网络是全联通的:若网络不是全联通网络，则撤回交换边的操作并执行下一次循环
                            if not nx.is_connected(G):              
                                G.add_edge(u,v)
                                G.add_edge(x,y)
                                G.remove_edge(u,y)
                                G.remove_edge(x,v)
                                continue 
#                        判断置乱前后的度累积分布是否一样
                        keys_new,degrees_new = list(zip(*list(G.degree()))) 
                        cdf_new = nx.utils.cumulative_distribution(degrees_new)
                        if cdf_new != cdf_new:
                            G.add_edge(u,v)
                            G.add_edge(x,y)
                            G.remove_edge(u,y)
                            G.remove_edge(x,v)
                            continue 
                        swap_count = swap_count + 1
    
    return G,swap_count


##############################test—program##############################

origin_G = nx.Graph()
origin_G = load_Graph_str('./brain_47_bh/network_brain_bh_47.txt')

M = origin_G.number_of_edges()             #网络中总边数
N = origin_G.number_of_nodes()             #网络中总节点数

nswap = 2*M
max_tries = 10*nswap
MAX = 200           #零模型最大调用次数

no_finish = []

for node  in origin_G.nodes():
    ##变量初始化
    actual_swap = 0             #实际成功交换次数
    node_random_time = 0        #零模型调用次数
    changed_G = nx.Graph()      #改变后的网络
    
    selected_node = node                #当前要被置乱的节点
    number_of_neighbors = len(list(origin_G.neighbors(selected_node)))  #当前要被置乱节点的连边数量

    print('now,it is node %s',node)
    #保证置乱节点的所有边都被断开重连
    while actual_swap < number_of_neighbors and node_random_time <= MAX:
        
        node_random_time = node_random_time + 1
        #调用节点置乱零模型
        changed_G,actual_swap = node_random_1k(selected_node,origin_G,nswap,max_tries)
        #若调用500次后仍不能将node的所有边置乱，则跳出循环，进入下一个节点的置乱
        if node_random_time == MAX:
            no_finish.append(node)      #记录不能全部置乱的节点
#            break
    
    text_save(changed_G.edges(),'./brain_47_bh/changed_network_node'+str(node)+'.txt')
    