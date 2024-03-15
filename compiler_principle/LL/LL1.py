def eliminate_left_recursion(N, P):
    new_non_terminals = []
    new_productions = P.copy()  # 复制原有的产生式字典，以便修改
    
    for non_terminal in N:
        productions = P[non_terminal]
        alpha_productions = []
        beta_productions = []
        
        for production in productions:
            if production.startswith(non_terminal):
                alpha_productions.append(production[len(non_terminal):])
            else:
                beta_productions.append(production)
        
        if alpha_productions:
            new_non_terminal = non_terminal + "'"
            new_non_terminals.append(new_non_terminal)
            
            new_alpha_productions = [p +" "+ new_non_terminal for p in alpha_productions] + ['ε']
            new_productions[non_terminal] = [p + " " +new_non_terminal for p in beta_productions]
            new_productions[new_non_terminal] = new_alpha_productions
    
    N = N.union(new_non_terminals)
    
    return N, new_productions

def compute_first(N, T, P):
    print(P)

    # 初始化FIRST集，将所有非终结符的FIRST集初始化为空集
    FIRST = {symbol: set() for symbol in N.union(T).union({'ε'})}
    
    # 终结符的FIRST集就是其自身
    for terminal in T.union({'ε'}):
        FIRST[terminal].add(terminal)
    
    # 根据文法规则逐步计算FIRST集
    changed = True
    while changed:
        changed = False
        for non_terminal in N:
            for production in P[non_terminal]:
                symbols = production.split()
                for symbol in symbols:
                    if symbol in T.union({"ε"}):
                        # 如果是终结符，直接加入FIRST集
                        if symbol not in FIRST[non_terminal]:
                            FIRST[non_terminal].add(symbol)
                            changed = True
                        break
                    else:
                        # 如果是非终结符，加入其FIRST集
                        for sym in FIRST[symbol]:
                            if sym != 'ε' and sym not in FIRST[non_terminal]:
                                FIRST[non_terminal].add(sym)
                                changed = True
                        if 'ε' not in FIRST[symbol]:
                            # 如果该非终结符不包含ε，不再往后推导
                            break
                    # 如果所有符号的FIRST集都包含ε，那么ε也加入FIRST集
                    if all(sym == 'ε' or sym in FIRST[sym] for sym in production):
                        if 'ε' not in FIRST[non_terminal]:
                            FIRST[non_terminal].add('ε')
                            changed = True
    
    return FIRST

def compute_follow(N, P, S, first):
    # 初始化FOLLOW集，将所有非终结符的FOLLOW集初始化为空集
    FOLLOW = {non_terminal: set() for non_terminal in N}

    # 设定起始符号S的FOLLOW集为$
    FOLLOW[S].add('$')
    for i in range(2):
        for non_terminal in N:
            for production in P[non_terminal]:
                symbols = production.split()
                for i, symbol in enumerate(symbols):
                    if symbol not in N:
                        continue
                    list = symbols[i+1:]
                    if is_list_epsilon(list, N, first):
                        FOLLOW[symbol].update(cal_list_first(list, N, first))
                        FOLLOW[symbol].update(FOLLOW[non_terminal])
                    else:
                        FOLLOW[symbol].update(cal_list_first(list, N, first))
                    FOLLOW[symbol].discard("ε")

    return FOLLOW


# 判断单个字符可不可以推导为空
def is_epsilon(A, N, first):
    if A == 'ε':
        return True
    if A not in N:
        return False
    result = False
    for symbol in first[A]:
        if symbol == 'ε':
            result = True
            break
    return result


# 判断字符串可不可以推导成空
def is_list_epsilon(list, N, first):
    result = True
    for item in list:
        if not is_epsilon(item, N, first):
            return False
    return result    
    
# 找出list串的first集
def cal_list_first(list, N, first):
    FIRST = set()
    for i, item in enumerate(list):
        if item not in N:
            FIRST = {item}
            break
        FIRST.update(first[item])
        if not is_epsilon(item, N, first):
            break
    return FIRST    


def build_predict_map(N, T, P, first, follow):
    predict_map = {}
    for non_terminal in N:
        predict_map[non_terminal] = {}
        for terminal in T.union({"$"}):
            predict_map[non_terminal][terminal] = []
            
    for non_terminal in N:
        for production in P[non_terminal]:
            symbols = production.split()
            FIRST = cal_list_first(symbols, N, first)
            for a in FIRST:
                if a not in T:
                    break
                predict_map[non_terminal][a].append(production)
            if "ε" in FIRST:
                for b in follow[non_terminal]:
                    predict_map[non_terminal][b].append(production)

    return predict_map


def ll_parser(T, S, predict_map, first):
    stack = ["$", S]    # 初始化栈
    ip = 0              # 向前指针指向第一个符号
    input_string = input("请输入待分析的串，每个符号用空格分隔: ").split()

    while stack[-1] != "$" and ip < len(input_string):
        
        print("栈状态",stack)
        x = stack[-1]
        a = input_string[ip]
        print("a:",a)
        print("x:",x)
        if x in T or x == "$":
            if x == a:
                stack.pop()
                ip += 1
                print("匹配到",a,"弹出")
            else:
                print("Error: 无法匹配输入符号", a)
                break
        elif x == "ε":
            stack.pop()
        else:
            production = predict_map[x][a]
            for proc in production:
                proc_list = proc.split()
            print("使用产生式：", proc_list)
            stack.pop()
            if production != 'ε':
                stack.extend(reversed(proc_list))
            else:
                print("Error: 找不到合适的产生式")
                break
    
    while len(stack) >= 2 and "ε" in first[stack[-1]]:
        print("由于栈顶符号"+stack[-1]+"可以生成ε，弹出")
        stack.pop()
        

    print(stack)
    print(ip)
    if stack == ['$'] and ip == len(input_string):
        print("分析成功")
    else:
        print("分析失败")


def print_predict_map(predict_map, N, T):
    # 打印表头（终结符）
    header = ["Non-Terminal"]
    header.extend(T.union({"$"}))
    print("".join(f"{cell:<20}" for cell in header))
    
    for non_terminal in N:
        # 打印非终结符行
        row = [non_terminal]
        for terminal in T.union({"$"}):
            productions = predict_map[non_terminal][terminal]
            cell = " | ".join(productions)
            row.append(cell)
        print("".join(f"{cell:<20}" for cell in row))


T = {"(", ")", "+", "-", "*", "/", "num"}
N = {"E", "T", "F"}
P = {
        'E':['E + T', 'E - T', 'T'],
        'T':['T * F', 'T / F', 'F'],
        'F':['( E )','num']
    }
S = 'E'

N, P = eliminate_left_recursion(N, P) 
print("修改后的非终结符集合:", N)
print("修改后的产生式:")
for non_terminal in N:
    print(f"{non_terminal} -> {' | '.join(P[non_terminal])}")


first = compute_first(N, T, P)
print("FIRST集合:")
for non_terminal in N:
    print(f"FIRST({non_terminal}) = {first[non_terminal]}")

follow = compute_follow(N, P, S, first)
print("FOLLOW集合:")
for non_terminal in N:
    print(f"FOLLOW({non_terminal}) = {follow[non_terminal]}")

predict_map = build_predict_map(N, T, P, first, follow)
print_predict_map(predict_map, N, T)

ll_parser(T, S, predict_map, first)