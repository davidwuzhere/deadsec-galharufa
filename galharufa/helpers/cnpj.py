def format_cnpj(cnpj: str) -> str:
    if cnpj is not None:
        if len(cnpj) == 14:
            cnpj = cnpj[0:2] + "." + cnpj[2:5] + "." + cnpj[5:8] + \
                "/" + cnpj[8:12] + "-" + cnpj[12:14]
    return cnpj
