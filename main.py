import streamlit as st

# ==========================================
# PART 1: TEAMMATE'S LOGIC (EXACT COPY)
# ==========================================
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


# ==========================================
# PART 2: GUI (Streamlit Interface)
# ==========================================

# 1. Page Configuration 
st.set_page_config(page_title="Transformer Fault Diagnosis", page_icon="⚡")

# 2. Title & Header 
st.title("Transformer Fault Diagnosis System")
st.markdown("**Project:** Rule-Based Expert System for Power Transformer Fault Diagnosis")
st.markdown("---")

# 3. Sidebar Inputs 
st.sidebar.header("Input Gas Concentrations (ppm)")
st.sidebar.markdown("Enter the Dissolved Gas Analysis (DGA) values below:")

# Creating input fields for the 5 gases
h2_val = st.sidebar.number_input("Hydrogen (H2)", min_value=0.0, value=0.0, step=1.0)
ch4_val = st.sidebar.number_input("Methane (CH4)", min_value=0.0, value=0.0, step=1.0)
c2h2_val = st.sidebar.number_input("Acetylene (C2H2)", min_value=0.0, value=0.0, step=1.0)
c2h4_val = st.sidebar.number_input("Ethylene (C2H4)", min_value=0.0, value=0.0, step=1.0)
c2h6_val = st.sidebar.number_input("Ethane (C2H6)", min_value=0.0, value=0.0, step=1.0)

# 4. Packaging input into dictionary 
input_gases = {
    'H2': h2_val,
    'CH4': ch4_val,
    'C2H2': c2h2_val,
    'C2H4': c2h4_val,
    'C2H6': c2h6_val
}

# 5. Main Display Area 
col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Readings")
    st.json(input_gases) # Display input data nicely

with col2:
    st.subheader("Diagnosis Action")
    # The Button to trigger diagnosis
    if st.button("🔍 Run Diagnosis", use_container_width=True):
        
        # CALLING TEAMMATE'S FUNCTION HERE
        result = diagnose_transformer(input_gases)
        
        # Displaying the result
        st.markdown("### Result:")
        
        if result == "Normal Condition":
            st.success(f"✅ {result}")
            st.balloons() # Fun effect for normal condition
        elif result == "Partial Discharge":
            st.warning(f"⚠️ {result}")
        else:
            st.error(f"🚨 {result}")

# 6. Footer / Credits
st.markdown("---")
st.caption("MMU TES6313 Expert Systems Project | Developed by Group Cincai")