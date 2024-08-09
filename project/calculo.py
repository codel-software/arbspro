def getSurebets(surebets):
    num_surebets = len(surebets)
    transaction_cost = 3 / num_surebets if num_surebets else 0
    total_return = sum(surebet['expected_return'] for surebet in surebets)
    total_volatility = sum(surebet['volatility'] for surebet in surebets)
    total_c = transaction_cost * num_surebets
    total_ponderacao_ajustada = 0
    if total_return == 0 or total_volatility == 0 or total_c == 0:
        for surebet in surebets:
            surebet['ponderacao_ajustada'] = 0
            surebet['wi'] = 0
        return surebets
    for surebet in surebets:
        ponderacao_ajustada = (surebet['expected_return'] / total_return) * \
                              (1 - (surebet['volatility'] / total_volatility)) * \
                              (1 - (transaction_cost / total_c))
        surebet['ponderacao_ajustada'] = ponderacao_ajustada
        total_ponderacao_ajustada += ponderacao_ajustada
    if total_ponderacao_ajustada == 0:
        for surebet in surebets:
            surebet['wi'] = 0
    else:
        for surebet in surebets:
            surebet['wi'] = surebet['ponderacao_ajustada'] / total_ponderacao_ajustada
    minimum_profit_on_listing = 0
    maximum_profit_on_listing = 0
    for surebet in surebets:
        odd_a = surebet['odds'][0]
        odd_b = surebet['odds'][1]
        odd_c = surebet['odds'][2]
        implied_probability = surebet['implied_probability']
        allocation_a = ((odd_a / implied_probability) * surebet['wi'])
        allocation_b = ((odd_b / implied_probability) * surebet['wi'])
        allocation_c = ((odd_c / implied_probability) * surebet['wi'])
        result_allocation_a = allocation_a * odd_a
        result_allocation_b = allocation_b * odd_b
        result_allocation_c = allocation_c * odd_c
        return_allocation_a = result_allocation_a * odd_a
        return_allocation_b = result_allocation_b * odd_b
        return_allocation_c = result_allocation_c * odd_c
        maximum_possible_profit = max(return_allocation_a, return_allocation_b, return_allocation_c)
        minimum_possible_profit = min(return_allocation_a, return_allocation_b, return_allocation_c)
        maximum_profit_on_listing += maximum_possible_profit
        minimum_profit_on_listing += minimum_possible_profit
        surebet['maximum_possible_profit'] = maximum_possible_profit
        surebet['minimum_possible_profit'] = minimum_possible_profit
    data = {
        'surebets' : surebets,
        'minimum_profit_on_listing' : minimum_profit_on_listing,
        'maximum_profit_on_listing' : maximum_profit_on_listing
    }
    return data
        
