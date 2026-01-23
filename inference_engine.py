# ---------------------------------------------
# Rule-Based Inference Engine
# Transformer Fault Diagnosis Expert System
# ---------------------------------------------

def diagnose_transformer(gases):
    """
    Diagnose transformer fault using DGA rule-based inference.

    Parameters:
        gases (dict): Gas concentrations in ppm
                      Keys: H2, CH4, C2H2, C2H4, C2H6

    Returns:
        str: Fault diagnosis
    """

    # Helper function to avoid division by zero
    def ratio(a, b):
        return a / b if b != 0 else 0

    # Calculate gas ratios
    ch4_h2 = ratio(gases['CH4'], gases['H2'])
    c2h2_c2h4 = ratio(gases['C2H2'], gases['C2H4'])
    c2h4_c2h6 = ratio(gases['C2H4'], gases['C2H6'])

    # -------------------
    # Rule-Based Inference
    # -------------------

    # Arcing Fault
    if c2h2_c2h4 > 1 and ch4_h2 < 0.1:
        return "Arcing Fault"

    # Thermal Fault
    elif ch4_h2 > 1 and c2h4_c2h6 < 1:
        return "Thermal Fault"

    # Partial Discharge
    elif gases['H2'] > gases['CH4'] and gases['H2'] > gases['C2H2']:
        return "Partial Discharge"

    # Normal Condition
    else:
        return "Normal Condition"
    

