import fix_uv
import func_ewt
from collections import deque
import copy
fix_temp = fix_uv
func = func_ewt


def make_c(lim_cu, contracted, a, i, u, full, poss, f, fptr, store_for_repeat, full_pos,
           i_c, menu, contr_obj, const_obj):
    for n in range(2, lim_cu+1, 2):
        # print('n: ', n)
        # print('lim_cu: ', lim_cu)
        # print('u: ', u)
        if n > 2:
            u_copy = deque([])
            y = copy.deepcopy(u)
            # print('y: ', y)
            for x in range(n):
                u_copy.append(copy.deepcopy(y))
                if y:
                    for item in y:
                        if item.pos == u_copy[-1][0].pos:
                            y.remove(item)
                            break
                else:
                    return   # if there are less no of operators the
                    # fn should return without any result
            while True:
                add = 0
                u_tmp = []
                u_2 = copy.deepcopy(u)
                full_2 = copy.deepcopy(full)
                # pick up all cummulants
                for index in range(len(u_copy)):
                    u_tmp.append(u_copy[index][0])
                for item in u_tmp:
                    if item.dag == '0':
                        add = add-1
                    else:
                        add = add+1
                if add == 0:
                    for item1 in u_tmp:
                        for item2 in u_2:
                            if item1.pos == item2.pos:
                                u_2.remove(item2)
                                break
                        for item2 in full_2:
                            if item1.pos == item2.pos:
                                full_2.remove(item2)
                                break
                    flag1 = 0
                    contracted.append(u_tmp)
                    p_1 = 0  # if the character from string 1 is present or not
                    p_2 = 0
                    if len(contracted) > 0:
                        # this stores all the multiple lambda and stores them in a list, checks them to see redundancy
                        for item1 in store_for_repeat:
                            if func.equality_check(contracted, item1):
                                flag1 = 1
                                break
                        for item in u_tmp:
                            if item.string == 1:
                                p_1 = 1
                            else:
                                p_2 = 1
                        if (flag1 == 0 and p_1 == 1 and p_2 == 1) or menu == '1':
                            make_c(n, contracted, a, i, copy.deepcopy(u_2), copy.deepcopy(full_2), poss, f, fptr,
                                   store_for_repeat, full_pos, i_c, menu, contr_obj, const_obj)
                            # call the function again with smaller u
                            # if not u_2:
                            store_for_repeat.append(copy.deepcopy(contracted))
                    contracted.pop()
                flag = 1
                x = -1
                if len(u_copy[0]) == n:
                    break  # break out of whole function
                while flag == 1:
                    if u_copy[x]:
                        u_copy[x].popleft()
                        if x >= (-len(u_copy[x])):
                            flag = 0
                            tmp_0 = copy.deepcopy(u_copy[x])
                            while x < -1:
                                x = x+1
                                tmp_0.popleft()
                                u_copy[x] = copy.deepcopy(tmp_0)
                    else:
                        x = x-1
        elif n == 2:
            no = int(len(full)/2)
            for lim_cnt in range(0, no+1):
                if lim_cnt > 0:
                    temp_list = copy.deepcopy(poss)
                    op_no = 0
                    flag = 0
                    while temp_list:
                        matched = []
                        contracted_l = []
                        contracted_r = []
                        while not flag:
                            if not temp_list[0]:
                                op_no = op_no+1
                                temp_list.popleft()
                                if not temp_list:
                                    flag = 1
                            else:
                                flag = 1
                        flag = 0
                        if temp_list:
                            contracted_l.append(full[op_no])
                            contracted_r.append(temp_list[0][0])
                            matched.append(full[op_no])
                            matched.append(temp_list[0][0])
                            temp_list[0].popleft()
                            fix_temp.fix_con(copy.copy(op_no), 1, lim_cnt, copy.deepcopy(temp_list), matched,
                                             contracted, contracted_l, contracted_r, a, i, u, full, f, fptr, full_pos,
                                             i_c, contr_obj, const_obj)
                            # print('after fix_con function!!')
                            matched.pop()
                            matched.pop()
                else:
                    temp_list = deque([])
                    op_no = 0
                    matched = []
                    contracted_l = []
                    contracted_r = []
                    fix_temp.fix_con(copy.copy(op_no), 1, lim_cnt, copy.deepcopy(temp_list), matched,
                                     contracted, contracted_l, contracted_r, a, i, u, full, f, fptr, full_pos,
                                     i_c, contr_obj, const_obj)
