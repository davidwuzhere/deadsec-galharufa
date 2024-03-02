def format_cpf(cpf: str) -> str:
    if cpf is not None:
        if len(cpf) == 11:
            cpf = cpf[0:3] + "." + cpf[3:6] + \
                "." + cpf[6:9] + "-" + cpf[9:11]
    return cpf
