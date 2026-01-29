# ---------------------------------------------
# Rule-Based Inference Engine
# Transformer Fault Diagnosis (DGA)
# ---------------------------------------------

def diagnose_transformer(gases):

    def ratio(a, b):
        return a / b if b != 0 else 0

    r_ch4_h2 = ratio(gases['CH4'], gases['H2'])
    r_c2h2_c2h4 = ratio(gases['C2H2'], gases['C2H4'])
    r_c2h4_c2h6 = ratio(gases['C2H4'], gases['C2H6'])

    fired_rules = []
    fault_scores = {
        "Partial Discharge": 0,
        "Low Energy Arcing": 0,
        "High Energy Arcing": 0,
        "Thermal Fault T1 (<300°C)": 0,
        "Thermal Fault T2 (300–700°C)": 0,
        "Thermal Fault T3 (>700°C)": 0,
        "Mixed Fault": 0
    }

    # ---------------- PD ----------------
    if gases['H2'] > 100 and gases['H2'] > gases['CH4']:
        fired_rules.append("R1: PD – Hydrogen dominant")
        fault_scores["Partial Discharge"] += 1

    if r_ch4_h2 < 0.1:
        fired_rules.append("R2: PD – Low CH4/H2 ratio")
        fault_scores["Partial Discharge"] += 1

    # ---------------- D1 ----------------
    if 0.1 <= r_c2h2_c2h4 <= 1:
        fired_rules.append("R3: D1 – Low energy arcing ratio")
        fault_scores["Low Energy Arcing"] += 1

    # ---------------- D2 ----------------
    if r_c2h2_c2h4 > 1:
        fired_rules.append("R4: D2 – High energy arcing ratio")
        fault_scores["High Energy Arcing"] += 1

    # ---------------- T1 ----------------
    if r_ch4_h2 > 1 and r_c2h4_c2h6 < 1:
        fired_rules.append("R5: T1 – Low temp thermal")
        fault_scores["Thermal Fault T1 (<300°C)"] += 1

    # ---------------- T2 ----------------
    if 1 <= r_c2h4_c2h6 < 3:
        fired_rules.append("R6: T2 – Medium temp thermal")
        fault_scores["Thermal Fault T2 (300–700°C)"] += 1

    # ---------------- T3 ----------------
    if r_c2h4_c2h6 >= 3:
        fired_rules.append("R7: T3 – High temp thermal")
        fault_scores["Thermal Fault T3 (>700°C)"] += 1

    # ---------------- Mixed ----------------
    if gases['C2H2'] > 10 and gases['C2H4'] > 100:
        fired_rules.append("R8: Mixed fault condition")
        fault_scores["Mixed Fault"] += 1

    # ---------------- Final Diagnosis ----------------
    final_fault = max(fault_scores, key=fault_scores.get)

    if fault_scores[final_fault] == 0:
        final_fault = "Normal Condition"

    return final_fault, fired_rules


# -----------------------------
# Test
# -----------------------------
if __name__ == "__main__":

    sample_gases = {
        'H2': 180,
        'CH4': 90,
        'C2H2': 2,
        'C2H4': 40,
        'C2H6': 50
    }

    result = diagnose_transformer(sample_gases)

    print("Input Gas Data:", sample_gases)
    print("Fired Rules:")
    for r in result:
        print("-", r)