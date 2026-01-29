import streamlit as st

# ==========================================
# PART 1: INFERENCE ENGINE (YOUR NEW CODE)
# ==========================================

def diagnose_transformer(gases):
    """
    Diagnose transformer fault using a Scoring System.
    Returns: (Final Diagnosis, List of Fired Rules)
    """

    def ratio(a, b):
        return a / b if b != 0 else 0

    # Calculate Ratios
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
    # R1: Hydrogen Dominant (Example rule)
    if gases['H2'] > 100 and gases['H2'] > gases['CH4']:
        fired_rules.append("R1: PD – Hydrogen dominant (>100ppm & >CH4)")
        fault_scores["Partial Discharge"] += 1

    # R2: Low CH4/H2 Ratio
    if r_ch4_h2 < 0.1:
        fired_rules.append(f"R2: PD – Low CH4/H2 ratio ({r_ch4_h2:.2f} < 0.1)")
        fault_scores["Partial Discharge"] += 1

    # ---------------- D1 ----------------
    if 0.1 <= r_c2h2_c2h4 <= 1:
        fired_rules.append(f"R3: D1 – Low energy arcing ratio (0.1 <= {r_c2h2_c2h4:.2f} <= 1)")
        fault_scores["Low Energy Arcing"] += 1

    # ---------------- D2 ----------------
    if r_c2h2_c2h4 > 1:
        fired_rules.append(f"R4: D2 – High energy arcing ratio ({r_c2h2_c2h4:.2f} > 1)")
        fault_scores["High Energy Arcing"] += 1

    # ---------------- T1 ----------------
    if r_ch4_h2 > 1 and r_c2h4_c2h6 < 1:
        fired_rules.append(f"R5: T1 – Low temp thermal (CH4/H2 > 1 & C2H4/C2H6 < 1)")
        fault_scores["Thermal Fault T1 (<300°C)"] += 1

    # ---------------- T2 ----------------
    if 1 <= r_c2h4_c2h6 < 3:
        fired_rules.append(f"R6: T2 – Medium temp thermal (1 <= {r_c2h4_c2h6:.2f} < 3)")
        fault_scores["Thermal Fault T2 (300–700°C)"] += 1

    # ---------------- T3 ----------------
    if r_c2h4_c2h6 >= 3:
        fired_rules.append(f"R7: T3 – High temp thermal ({r_c2h4_c2h6:.2f} >= 3)")
        fault_scores["Thermal Fault T3 (>700°C)"] += 1

    # ---------------- Mixed ----------------
    if gases['C2H2'] > 10 and gases['C2H4'] > 100:
        fired_rules.append("R8: Mixed fault condition (High C2H2 & C2H4)")
        fault_scores["Mixed Fault"] += 1

    # ---------------- Final Diagnosis ----------------
    # Select the fault with the highest score
    final_fault = max(fault_scores, key=fault_scores.get)

    # If no rules fired (Score is 0), set to Normal
    if fault_scores[final_fault] == 0:
        final_fault = "Normal Condition"
        fired_rules.append("No fault rules triggered.")

    return final_fault, fired_rules


# ==========================================
# PART 2: STREAMLIT USER INTERFACE
# ==========================================

st.set_page_config(page_title="Transformer Diagnosis System", page_icon="⚡", layout="wide")

# Header
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/High_voltage_transformer.jpg/640px-High_voltage_transformer.jpg", width=100) # 这是一个网上的变压器图，你可以换成MMU logo
with col_header2:
    st.title("Transformer Fault Diagnosis Expert System")
    st.markdown("**Method:** Rule-Based Scoring System (IEC/Rogers Logic)")

st.markdown("---")

# Layout: Left for Input, Right for Output
left_col, right_col = st.columns([1, 1.5])

with left_col:
    st.header("1. Input DGA Data (ppm)")
    st.info("Enter the gas concentrations from the oil sample.")
    
    h2_val = st.number_input("Hydrogen (H2)", min_value=0.0, value=180.0, step=1.0)
    ch4_val = st.number_input("Methane (CH4)", min_value=0.0, value=90.0, step=1.0)
    c2h2_val = st.number_input("Acetylene (C2H2)", min_value=0.0, value=2.0, step=1.0)
    c2h4_val = st.number_input("Ethylene (C2H4)", min_value=0.0, value=40.0, step=1.0)
    c2h6_val = st.number_input("Ethane (C2H6)", min_value=0.0, value=50.0, step=1.0)

    # Pack data
    input_gases = {
        'H2': h2_val, 'CH4': ch4_val, 'C2H2': c2h2_val, 'C2H4': c2h4_val, 'C2H6': c2h6_val
    }
    
    run_btn = st.button("🔍 Analyze Fault", type="primary", use_container_width=True)

with right_col:
    st.header("2. Diagnosis Results")
    
    if run_btn:
        # Call the new function (returns TWO values now)
        diagnosis, reasoning_trace = diagnose_transformer(input_gases)
        
        # Display Result Card
        if diagnosis == "Normal Condition":
            st.success(f"✅ **Status:** {diagnosis}")
        else:
            st.error(f"⚠️ **Fault Detected:** {diagnosis}")
            
        # Display Reasoning (The "Expert" part)
        st.markdown("### 🧠 Inference Explanation (Why?)")
        with st.expander("View Logic Trace", expanded=True):
            if reasoning_trace:
                for rule in reasoning_trace:
                    st.code(rule, language="text")
            else:
                st.write("No specific rules fired.")
        
        # Visualization (Optional Bonus)
        st.markdown("### 📊 Gas Ratios")
        # Calculate ratios for display
        r1 = input_gases['C2H2']/input_gases['C2H4'] if input_gases['C2H4']!=0 else 0
        r2 = input_gases['CH4']/input_gases['H2'] if input_gases['H2']!=0 else 0
        r3 = input_gases['C2H4']/input_gases['C2H6'] if input_gases['C2H6']!=0 else 0
        
        col_r1, col_r2, col_r3 = st.columns(3)
        col_r1.metric("R1 (C2H2/C2H4)", f"{r1:.2f}")
        col_r2.metric("R2 (CH4/H2)", f"{r2:.2f}")
        col_r3.metric("R3 (C2H4/C2H6)", f"{r3:.2f}")

# Footer
st.markdown("---")
st.caption("Developed for TES6313 Expert Systems | Multimedia University")