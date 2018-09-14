from itertools import combinations
from sympy.logic.algorithms.dpll import dpll_int_repr
__author__ = "Piyush Umate"
import copy
INPUT_FILE = "input.txt"
OUTPUT_FILE = "output.txt"
group_count = 0
pot_count = 0
countries, pots, regions, region_names, cnf = [None], [], [], [], []
key_constant = 1000
import time
start_time = time.time()
import operator

def group_greater_country():
    groups = ['None' for x in range(group_count)]
    current_index = 0
    for country in countries:
        if country:
            groups[current_index] = country
            current_index += 1
    groups = ['Yes'] + groups
    process_output(groups)
    exit(0)

def create_countries_and_pots(input_data):
    global countries, pots
    for pot in input_data:
        countries_in_pot = pot.split(',')
        countries_in_pot_count = len(countries_in_pot)
        countries.extend(countries_in_pot)
    countries.sort()
    if group_count >= len(countries)-1:
        group_greater_country()
    for pot in input_data:
        countries_in_pot = pot.split(',')
        if len(countries_in_pot) > group_count:
            process_output(['No'])
            exit(0)
        pots.append([countries.index(c) for c in countries_in_pot])

def create_regions(input_data):
    global regions
    for input_line in input_data:
        input = input_line.split(':')
        region_names.append(input[0])
        countries_in_region = input[1].split(',')
        if input[0] != 'UEFA':
            if len(countries_in_region) > group_count:
                process_output(['No'])
                exit(0)
        else:
            if len(countries_in_region) > 2*group_count:
                process_output(['No'])
                exit(0)
        if len(countries_in_region) == 1 and countries_in_region[0] == 'None':
            regions.append([])
        else:
            regions.append([countries.index(c) for c in countries_in_region])


def create_symbols(cnf, model={}):
    symbols = []
    for clause in cnf:
        symbols.extend(clause)
    symbols = [abs(symbol) for symbol in symbols]
    symbols = set(symbols)
    return symbols
    #return symbols.difference(set(model.keys()))
    # for k in model:
    #     if k in symbols:
    #         symbols.remove(k)
    # return symbols

def find_pure_symbol(symbols, clauses):
    for symbol in symbols:
        lookup_symbol = -symbol
        if lookup_symbol not in symbols:
            return symbol, True
    return None, None
    # for symbol in symbols:
    #     lookup_symbol = -symbol
    #     pos_flag, neg_flag = False, False
    #     for clause in clauses:
    #         if not pos_flag and symbol in clause:
    #             pos_flag = True
    #         if not neg_flag and lookup_symbol in clause:
    #             neg_flag = True
    #     if pos_flag != neg_flag:
    #         return symbol, pos_flag
    # return None, None

def find_unit_clause(clauses, model):
    for clause in clauses:
        difference = set(clause) - set(model.keys())
        if len(difference) == 1:
            val = difference.pop()
            return val, True
    return None, None

def is_not_false_clause(clause, model):
    for literal in clause:
        if literal not in model:
            return True
    return False

def is_true_clause(clause, model):
    for literal in clause:
        if literal in model and model[literal]:
            return True
    return False

# def evaluate_proposition_logic(clause, model):
#     absolute_clause = set([abs(literal) for literal in clause])
#     assigned_literals = set(model.keys())
#     if absolute_clause < assigned_literals:
#         eval = False
#         for literal in clause:
#             val = model[abs(literal)]
#             if literal < 0:
#                 eval = eval or (not val)
#             else:
#                 eval = eval or val
#             if eval:
#                 return True
#         return eval
#     else:
#         for literal in clause:
#             if abs(literal) in model:
#                 if literal < 0:
#                     if not model[abs(literal)]:
#                         return True
#                 else:
#                     if model[literal]:
#                         return True
#         return None

def max_common_symbol(clauses):
    counter_dict = {}
    #print 'clauses', clauses
    for clause in clauses:
        for literal in clause:
            if abs(literal) in counter_dict:
                counter_dict[abs(literal)] += 1
            else:
                counter_dict[abs(literal)] = 0
    return max(counter_dict.iteritems(), key=operator.itemgetter(1))[0]

def dpll(cnf, model):
    #print 'model', model
    #print 'cnf', cnf
    blank_clauses = []
    for clause in cnf:
        if is_true_clause(clause, model):
            continue
        elif is_not_false_clause(clause, model):
            blank_clauses.append(clause)
        else:
            return False

    if not blank_clauses:
        return model

    symbols = create_symbols(blank_clauses, model)
    #find pure symbol
    pure_symbol, value = find_pure_symbol(symbols, blank_clauses)
    if pure_symbol:
        model.update({pure_symbol:value, -pure_symbol: not value})
        # symbols.remove(pure_symbol)
        # if -pure_symbol in symbols:
        #     symbols.remove(-pure_symbol)
        return dpll(blank_clauses, model)
    #find unit clauses
    unit_symbol, value = find_unit_clause(blank_clauses, model)
    if unit_symbol:
        model.update({unit_symbol:value, -unit_symbol: not value})
        # symbols.remove(unit_symbol)
        # if -unit_symbol in symbols:
        #     symbols.remove(-unit_symbol)
        return dpll(blank_clauses, model)
        #add to model

    # symbols_copy = copy.deepcopy(symbols)
    symbol = max_common_symbol(blank_clauses)
    symbols.discard(symbol)
    # if -symbol in symbols:
    #     symbols.remove(-symbol)
    model_copy = copy.copy(model)
    model.update({symbol:True, -symbol:False})
    model_copy.update({symbol:False, -symbol:True})

    return dpll(blank_clauses,model) or dpll(blank_clauses, model_copy)

def extend(s, var, val):
    s2 = s.copy()
    s2[var] = val
    return s2

def dpll_satisfy(symbols):
    global cnf
    return dpll(cnf, {})

def encode_sym(country_index, group_index, key=key_constant):
    return int(country_index*key + group_index)

def decode_sym(encoded_index):
    return countries[encoded_index / key_constant], encoded_index % key_constant

def create_cnf(constraints, is_region=False):
    if is_region:
        uefa_index = region_names.index('UEFA')
    for constraint_index, constraint in enumerate(constraints):
        if is_region and constraint_index == uefa_index:
            combination_length = 3
        else:
            combination_length = 2
        same_constraint_combinations = combinations(constraint, combination_length)
        for c in same_constraint_combinations:
            for group_index in range(1,group_count+1):
                if combination_length == 2:
                    cnf.append({-encode_sym(c[0], group_index), -encode_sym(c[1], group_index)})
                else:
                    cnf.append({-encode_sym(c[0], group_index), -encode_sym(c[1], group_index),
                    -encode_sym(c[2], group_index)})

def xor_cnf_combinations():
    global cnf
    for country_index in range(1, len(countries)):
        country_group_expression = []
        for group_index in range(1,group_count+1):
            country_group_expression.append(encode_sym(country_index, group_index))
        cnf.append(set(country_group_expression))
        country_group_expression = [-c for c in country_group_expression]
        country_group_expression = combinations(country_group_expression, 2)
        for expr in country_group_expression:
            cnf.append(set(expr))

# def constraint_checker(constraint, is_region, model):
#     if is_region: #region constraint
#         uefa_index = region_names.index('UEFA')
#     for c in constraint:

def process_input(input=INPUT_FILE):
    with open(input, 'r') as file_pointer:
        lines = file_pointer.read().splitlines()
    global group_count, pot_count
    group_count, pot_count = int(lines[0]), int(lines[1])
    create_countries_and_pots(lines[2:2+pot_count])
    create_regions(lines[2+pot_count:])
    #working cnf
    #speed - cnf no issue
    #----------------------------
    create_cnf(regions, True)
    create_cnf(pots)
    xor_cnf_combinations()
    symbols = create_symbols(cnf)
    model = dpll_int_repr(cnf,symbols,{})
    #print model
    #print 'model', mod[0]
    #----------------------------

    # model = dpll_satisfy({})
    if not model:
        #print model
        process_output(['No'])
    else:
        group_countries = ['None' for x in range(group_count)]
        for key in model:
            if key > 0 and model[key]:
                country, group_index = decode_sym(key)
                if group_countries[group_index-1] != 'None':
                    group_countries[group_index-1] += ','+country
                else:
                    group_countries[group_index-1] = country
        #print 'gc',group_countries
        #print group_countries
        group_countries = ['Yes'] + group_countries
        process_output(group_countries)
    #print("--- %s seconds ---" % (time.time() - start_time))

def process_output(output):
    #print 'hey'
    file_handle = open(OUTPUT_FILE, "w")
    file_handle.write("\n".join(output))
    file_handle.close()

process_input()
