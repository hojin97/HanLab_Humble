"""
YOUR NAME HERE!!!!
2016253004 정호진
"""

from math import ceil

MIN_SUPPORT_PERCENT = 0.035

def support(transaction, result_dict, item):
    return len(result_dict[item]) / len(transaction) * 100

def get_input_data(filename):
    input_file = open(filename, 'r')
    transactions = dict()
    itemset = set()
    real_itemset = set()

    for line in input_file:
        item = line.split(', ')
        for item_t in item:
            if item.index(item_t) == 0 or item_t == '\n':           # item[0] == transaction's id
                continue
            itemset.add(item_t)
        tmp_iset = itemset.copy()
        real_itemset = real_itemset | itemset.copy()
        transactions[item[0]] = tmp_iset
        itemset.clear()

    #print(transactions)        # for test
    return transactions, real_itemset

# Print example : {YAL005c, YBR044c} 3.8%
def output_to_file(filename, result_dict, transactions):
    file = open(filename, 'w')

    output_key = set()
    #output_key.add('덤벨컬')
    output_key.add('덤벨 킥 백')

    for key in result_dict.keys():
        if type(key) == type(' '):
            pass
        else:
            tmp_key = set(key)
            if len(tmp_key & output_key) == 0:
                continue
            for item in key:
                file.write(f"{item},")
            file.write(f"\n{support(transactions, result_dict, key):.2}% support :: len : {len(result_dict[key])}\n")
    file.close()

# When itemset passed, it return t(x).
# Frequent closed gene sets : minimum support of 3.5%.
def itemset_to_num_transaction(transaction, itemset, min_support):
    count = set()
    if type(itemset) == type(' '):          # After type compare, if itemset is str?
        tmp = set()
        tmp.add(itemset)
        itemset = tmp.copy()                # Change form.
    index_num = 1                       # Start index num
    for key in transaction.keys():
        if set(transaction[key]) & itemset == itemset:
            count.add(index_num)
        index_num += 1

    if len(count) >= min_support :
        return count

def generate_combination_set(transaction, result_dict, itemsize, min_support):
    if len(list(result_dict)[-1]) < itemsize-1 :    #   "len(list(size_dict)[-1])" means length of previous values
        return                 #   Now itemsize represents the size of the value to be retrieved. so 'itemsize - 1'

    # size == 1
    size_list = []
    for key in result_dict.keys():
        if itemsize == 2 and type(key) == type(' '):   # (itemsize == 2) means, It will make setsize 2. so now we need size 1 set.
            size_list.append(key)
        else:
            if len(key) == itemsize-1:
                size_list.append(key)
        #print(size_list)
    i = 0
    flag_break = False              # variable for i  //  flag_break == True ? escape i : continue
    while True:
        if i >= len(size_list)-1:
            break
        j = i + 1
        #print(len(size_list), end=' ')
        while True:
            #print(i, j)
            if j >= len(size_list):
                break

            tmp_1, tmp_2 = set(), set()
            if type(size_list[i]) == type(' '):
                tmp_1.add(size_list[i])
                tmp_2.add(size_list[j])
            else:
                tmp_1 = set(size_list[i])
                tmp_2 = set(size_list[j])

            tmp = tmp_1 | tmp_2
            #print(itemsize, tmp)
            if len(tmp) == itemsize:
                count = itemset_to_num_transaction(transaction, tmp, min_support)
                tmp = tuple(tmp)
                if count != None:
                    result_dict[tmp] = count
                    f1, f2 = result_dict[size_list[i]] == result_dict[tmp], result_dict[size_list[j]] == result_dict[tmp]
                    #print(size_list)
                    #print(f"{i} :: {size_list[i]} : {result_dict[size_list[i]]}")
                    #print(f"{j} :: {size_list[j]} : {result_dict[size_list[j]]}")
                    #print(f"{itemsize} :: {tmp} : {result_dict[tmp]}")
                    #print(f"{f1},{f2}")

                    if f1:
                        result_dict.pop(size_list[i])
                        size_list.remove(size_list[i])
                        j -= 1
                        flag_break = True

                    elif f2:
                        result_dict.pop(size_list[j])
                        size_list.remove(size_list[j])
                        j -= 1
            j += 1
        if not flag_break:
            i += 1
        else:
            flag_break = False

    remove_items = []
    for index in range(len(size_list)):
        for key in result_dict.keys():
            if type(key) == type(' '):
                pass
            else:
                if len(key) == itemsize:
                    if result_dict[size_list[index]] == result_dict[key]:
                        remove_items.append(size_list[index])
                        break
    for i in range(len(remove_items)):
        result_dict.pop(remove_items[i])
    return result_dict

def generate_all_frequent_itemsets(transaction, item_set, min_support):
    result_dict = dict()
    itemsize = 1

    # size == 1
    for item in item_set:
        count = itemset_to_num_transaction(transaction, item, min_support)
        if count != None:
            result_dict[item] = count

    while True:
        itemsize += 1
        tmp_dict = generate_combination_set(transaction, result_dict, itemsize, min_support)
        if tmp_dict == None:
            break
        result_dict.update(tmp_dict)
    #print(result_dict)
    return result_dict

# The main function
def main():
    input_filename = 'WorkOut_Data.txt'
    output_filename = 'H_for_user.txt'
    transaction, item_set = get_input_data(input_filename)
    min_support = ceil(MIN_SUPPORT_PERCENT * len(transaction))
    result_dict = generate_all_frequent_itemsets(transaction, item_set, min_support)
    output_to_file(output_filename, result_dict, transaction)
    print("Finish!")

if __name__ == '__main__':
    main()