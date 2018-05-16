import numpy as np
from copy import deepcopy
from random import choice
from projecting_linear import project_linear
from projecting_sparse import theta_project_sparse
from rb_tree import RBTree, RBTreeNode

def initial_flows(graph, corresp_matrix, path_dict):
    array = dict()
    for pair,paths in path_dict.items():
        amount = corresp_matrix[pair]
        el = np.zeros(shape=len(paths))
        el[0] = amount
        if len(paths) == 0:
            continue
        p = paths[0]
        for i in range(len(p)-1):
            graph.get_edge(p[i],p[i+1]).add_users(amount)
        array[pair] = el
    return array

def flow_optimize(graph, corresp_matrix, path_dict, is_project_linear = False):
    iter = 0
    print('Iter',iter)
    x = initial_flows(graph, corresp_matrix, path_dict)
    graph.log_amount()
    y = x.copy()
    graph_x = graph
    graph_y = deepcopy(graph)
    iter = 1
    if not is_project_linear:
        T_x_dict = dict()
        x_elements_dict = dict()
        for pair, x_i in x.items():
            T_x = RBTree()
            T_x_dict[pair] = T_x
            x_elements = dict()
            for i, v_el in enumerate(x_i):
                if abs(v_el) > 1e-6:
                    x_elements[i] = T_x.insert(v_el)
            x_elements_dict[pair] = x_elements

        T_y_dict = dict()
        y_elements_dict = dict()
        for pair, y_i in y.items():
            T_y = RBTree()
            T_y_dict[pair] = T_y
            y_elements = dict()
            for i, v_el in enumerate(y_i):
                if abs(v_el) > 1e-6:
                    y_elements[i] = T_y.insert(v_el)
            y_elements_dict[pair] = y_elements

    while iter <= 1000:
        pair, paths = choice(list(path_dict.items()))
        y_i = y[pair]
        x_i = x[pair]
        y_i_new = x_i - 1.0/iter * np.array([graph_x.get_cost(p) for p in paths])
        if is_project_linear:
            y_i_new = np.array(project_linear(y_i_new, corresp_matrix[pair], False, True))
        else:
            diff_y = y_i_new - y_i
            T_y = T_y_dict[pair]
            y_elements = y_elements_dict[pair]
            for i, el in enumerate(diff_y):
                if abs(el) < 1e-6:
                    continue
                if i in y_elements.keys():
                    node = y_elements.pop(i)
                    old_val = node.key
                    T_y.delete_node(node)
                    # if y_i_new[i] = diff_y[i] + y_i[i] != 0 we can add new item
                    if abs(old_val + el) > 1e-6:
                        y_elements[i] = T_y.insert(el)
                else:
                    y_elements[i] = T_y.insert(el)
            # y_elements_dict[pair] = y_elements

            Theta = theta_project_sparse(T_y, len(y_i_new), corresp_matrix[pair])
            for i in list(y_elements.keys()):
                node = y_elements.pop(i)
                old_val = node.key
                T_y.delete_node(node)
                if old_val > Theta:
                    T_y.insert(old_val - Theta)
                    y_i_new[i] = old_val - Theta
                else:
                    y_i_new[i] = 0
            # y_elements_dict[pair] = y_elements
            # T_y_dict[pair] = T_y

        diff_y = y_i_new - y_i
        graph_y.change_amount(paths, diff_y)

        x_i_new = x_i - 1.0 / iter * np.array([graph_y.get_cost(p) for p in paths])
        if is_project_linear:
            x_i_new = np.array(project_linear(x_i_new, corresp_matrix[pair], False, True))
        else:
            diff_x = x_i_new - x_i
            T_x = T_x_dict[pair]
            x_elements = x_elements_dict[pair]
            for i, el in enumerate(diff_x):
                if abs(el) < 1e-6:
                    continue
                if i in x_elements.keys():
                    node = x_elements.pop(i)
                    old_val = node.key
                    T_x.delete_node(node)
                    # if x_i_new[i] = diff_x[i] + x_i[i] != 0 we can add new item
                    if abs(old_val + el) > 1e-6:
                        x_elements[i] = T_x.insert(el)
                else:
                    x_elements[i] = T_x.insert(el)
            # x_elements_dict[pair] = x_elements

            Theta = theta_project_sparse(T_x, len(x_i_new), corresp_matrix[pair], True)
            for i in list(x_elements.keys()):
                node = x_elements.pop(i)
                old_val = node.key
                T_x.delete_node(node)
                if old_val > Theta:
                    T_x.insert(old_val - Theta)
                    x_i_new[i] = old_val - Theta
                else:
                    x_i_new[i] = 0
            #y_elements_dict[pair] = y_elements

        diff_x = x_i_new - x_i
        graph_x.change_amount(paths, diff_x)

        #graph_x.log_amount()

        x[pair] = x_i_new
        y[pair] = y_i_new

        iter += 1
    print('Last iter')
    graph.log_amount()
