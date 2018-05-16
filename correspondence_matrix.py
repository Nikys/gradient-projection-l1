def corresp_matrix(input_traffic,output_traffic,func_table):
    rho = dict()
    q = dict()
    r = dict()
    for i,s_i in input_traffic.items():
        for j,d_j in output_traffic.items():
            rho[(i, j)] = s_i*d_j*func_table[(i,j)] / sum([d*func_table[(i,l)] for l,d in output_traffic.items()])
    rho_input_sum = {j: sum([rho[i, j] for i in input_traffic.keys()]) for j in output_traffic.keys()}
    rho_output_sum = {i: sum([rho[i, j] for j in output_traffic.keys()]) for i in input_traffic.keys()}
    iter = 0
    while(True):
        if iter > 0:
            rho_input_sum_sum_old = sum(rho_input_sum)
            rho_input_sum = {j: sum([rho[i, j] for i in input_traffic.keys()]) for j in output_traffic.keys()}
            rho_input_sum_sum_new = sum(rho_input_sum)
            rho_output_sum_sum_old = sum(rho_output_sum)
            rho_output_sum = {i: sum([rho[i, j] for j in output_traffic.keys()]) for i in input_traffic.keys()}
            rho_output_sum_sum_new = sum(rho_output_sum)
            diff1 = abs(rho_input_sum_sum_old-rho_input_sum_sum_new)
            diff2 = abs(rho_output_sum_sum_old-rho_output_sum_sum_new)
            if diff1 < 1e-6 and diff2 < 1e-6:
                break
        sum_changed = False
        for j, d_j in output_traffic.items():
            rho_input_sum_j = rho_input_sum[j]
            if rho_input_sum_j > d_j:
                sum_changed = True
                for i,s_i in input_traffic.items():
                    rho[(i, j)] *= d_j / rho_input_sum_j
                rho_input_sum[j] = d_j
        if sum_changed:
            rho_output_sum = {i: sum([rho[i, j] for j in output_traffic.keys()]) for i in input_traffic.keys()}

        for i, s_i in input_traffic.items():
            q[i] = s_i - rho_output_sum[i]
        for j, d_j in output_traffic.items():
            r[j] = d_j - rho_input_sum[j]
        for i, s_i in input_traffic.items():
            r_sum = sum([r[l] * func_table[(i,l)] for l in output_traffic.keys()])
            for j, d_j in output_traffic.items():
                rho[(i,j)] = rho[(i,j)] + q[i]*r[j]*func_table[(i,j)]/r_sum
        iter += 1
    return rho

