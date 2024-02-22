def validate_cpf(cpf):
    
    if len(cpf) != 11:
        return False
    
    if cpf == cpf[0] * 11:
        return False
    
    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    remainder = total % 11
    if remainder < 2:
        verification_digit_1 = 0
    else:
        verification_digit_1 = 11 - remainder
    
    if verification_digit_1 != int(cpf[9]):
        return False
    
    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    remainder = total % 11
    if remainder < 2:
        verification_digit_2 = 0
    else:
        verification_digit_2 = 11 - remainder
    
    if verification_digit_2 != int(cpf[10]):
        return False
    
    return True