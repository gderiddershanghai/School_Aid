import textstat

def get_readability_features(txt):
    flesch_kincaid = textstat.flesch_kincaid_grade(txt)
    gunning_grade = textstat.gunning_fog(txt)
    coleman_grade = textstat.coleman_liau_index(txt)
    linsear_grade = textstat.linsear_write_formula(txt)

    res = f"""
    \nFlesch-Kincaid Grade Level: {flesch_kincaid}
    \nGunning Fog Index Grade Level: {gunning_grade}
    \nColeman-Liau Index Grade Level: {coleman_grade}
    \nLinsear Write Formula Grade Level: {linsear_grade }
    """
    return res
