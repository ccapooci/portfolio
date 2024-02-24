
def convert_to_metric_length_cm(feet, inches):
    total_inches = feet * 12 + inches
    return total_inches * 2.54

def pick_genotype_values_given_result(age, height, weight, enzyme_inducer_value, amiodarone_value, race, warfarin_dosage):
    cyp2c9_dict = {}
    vkorc1_dict = {}
    vkorc1_result = []
    cyp2c9_result = []
    dosage_level = []
    cyp2c9_dict["cyp2c9_1_2"] = 0.5211
    cyp2c9_dict["cyp2c9_1_3"] = 0.9357
    cyp2c9_dict["cyp2c9_2_2"] = 1.0616
    cyp2c9_dict["cyp2c9_2_3"] = 1.9206
    cyp2c9_dict["cyp2c9_3_3"] = 2.3312
    cyp2c9_dict["cyp2c9_unk"] = 0.2188
    vkorc1_dict["vkorc1_ag"] = 0.8677
    vkorc1_dict["vkorc1_aa"] = 1.6974
    vkorc1_dict["vkorc1_uk"] = 0.4854

    for c_key,c_val in cyp2c9_dict.items():
        for v_key, v_val in vkorc1_dict.items():
            guess_warfarin_dosage = pow(5.6044 - 0.2614 * int(age/10) + 0.0087 * height + 0.0128 * weight - v_val - c_val + 1.1816 * enzyme_inducer_value - 0.5503 * amiodarone_value, 2) 
            if guess_warfarin_dosage < (warfarin_dosage + 0.5) and guess_warfarin_dosage > (warfarin_dosage - 0.5):
                vkorc1_result.append(v_key)
                cyp2c9_result.append(c_key)
                dosage_level.append(guess_warfarin_dosage)

    return cyp2c9_result, vkorc1_result, dosage_level

def compute_genotype(age, height, weight, enzyme_inducer_status, amiodarone_status, race, warfarin_dosage):
    c_geno = ""
    v_geno = ""
    if race != 'C':
        print("unable to compute genotype")
    else:
        enzyme_inducer_value = 0
        amiodarone_value = 0
        if(enzyme_inducer_status):
            enzyme_inducer_value = 1
        if(amiodarone_status):
            amiodarone_value = 1
        c_geno, v_geno, dosage = pick_genotype_values_given_result(age, height, weight, enzyme_inducer_value, amiodarone_value, race, warfarin_dosage)
        
    return c_geno, v_geno, dosage
        
    
age = 56
weight_kg = 72
enzyme_inducer_status = True
amiodarone_status = True
race = 'C'
metric_height_cm = convert_to_metric_length_cm(5, 10)
warfarin_dosage = 21
cyp2c9_geno, vkorc1_geno, dosage_level = compute_genotype(age, metric_height_cm , weight_kg, enzyme_inducer_status, amiodarone_status, race, warfarin_dosage)

for i in range(len(dosage_level)):             
    print("CYPTC9", cyp2c9_geno[i], "VKORC1_GENO", vkorc1_geno[i], "Dosage", dosage_level[i])


