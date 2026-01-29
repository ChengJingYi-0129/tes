import streamlit as st
import clips

# ==========================================
# 1. CLIPS ENGINE FUNCTION
# ==========================================
def run_clips_logic(input_gases):
    """
    Loads inference_engine.clp, inserts user data, and runs the inference engine.
    """
    try:
        # Create CLIPS environment
        env = clips.Environment()
        
        # Load the rules file
        # ERROR CHECK: Ensure inference_engine.clp is in the same directory!
        env.load('inference_engine.clp') 
        
        # Insert User Data into CLIPS (Asserting Facts)
        # Matches the template: (deftemplate gas (slot name) (slot value))
        env.assert_string(f'(gas (name H2) (value {input_gases["H2"]}))')
        env.assert_string(f'(gas (name CH4) (value {input_gases["CH4"]}))')
        env.assert_string(f'(gas (name C2H2) (value {input_gases["C2H2"]}))')
        env.assert_string(f'(gas (name C2H4) (value {input_gases["C2H4"]}))')
        env.assert_string(f'(gas (name C2H6) (value {input_gases["C2H6"]}))')
        
        # Run the Engine
        env.run()
        
        # Retrieve Results
        diagnosis_result = "Normal Condition" # Default state
        
        # Iterate through all facts to find the 'diagnosis' template
        for fact in env.facts():
            if fact.template.name == 'diagnosis':
                diagnosis_result = fact['fault']
                # We break here to get the last asserted fault (highest priority logic)
                # Or you can collect them all if you prefer list format
        
        return diagnosis_result

    except Exception as e:
        return f"System Error: {e}"

# ==========================================
# 2. STREAMLIT USER INTERFACE
# ==========================================

st.set_page_config(page_title="Transformer Fault Diagnosis", layout="wide")

# Header Section
col1, col2 = st.columns([1, 5])
with col2:
    st.title("Transformer Fault Diagnosis System")
    st.markdown("**Core Engine:** CLIPS (C Language Integrated Production System) 6.4")
    st.markdown("**Standard:** IEC 60599 / Rogers Ratio Method")

st.markdown("---")

# Layout: Input (Left) & Output (Right)
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Input Gas Concentrations (ppm)")
    st.info("Please enter the dissolved gas analysis (DGA) values:")
    
    # Input Fields
    h2 = st.number_input("Hydrogen (H2)", value=20.0, step=1.0)
    ch4 = st.number_input("Methane (CH4)", value=10.0, step=1.0)
    c2h2 = st.number_input("Acetylene (C2H2)", value=0.0, step=1.0)
    c2h4 = st.number_input("Ethylene (C2H4)", value=10.0, step=1.0)
    c2h6 = st.number_input("Ethane (C2H6)", value=15.0, step=1.0)

    # Dictionary to hold the data
    user_data = {
        'H2': h2, 'CH4': ch4, 'C2H2': c2h2, 'C2H4': c2h4, 'C2H6': c2h6
    }
    
    st.write("") # Spacer
    run_btn = st.button("Run Diagnosis Engine", type="primary", use_container_width=True)

with right_col:
    st.subheader("Diagnosis Results")
    
    if run_btn:
        with st.spinner("Processing rules in CLIPS environment..."):
            
            # CALL THE ENGINE
            result = run_clips_logic(user_data)
            
            # Display Logic
            st.markdown("### Status:")
            
            if "Error" in result:
                st.error("Critical Error")
                st.code(result)
                st.warning("Please ensure 'inference_engine.clp' is present in the application folder.")
            
            elif result == "Normal Condition":
                st.success(f"**{result}**")
                st.balloons()
            
            else:
                st.error(f"**Fault Detected: {result}**")
                
                # Dynamic Recommendation based on fault (Optional Polish)
                st.markdown("#### Recommended Action:")
                if "Thermal" in result:
                    st.write("- Check for hotspots or insulation degradation.")
                    st.write("- Reduce transformer load immediately.")
                elif "Arcing" in result:
                    st.write("- Perform acoustic test to locate arcing.")
                    st.write("- Schedule internal inspection.")
                elif "Partial Discharge" in result:
                    st.write("- Monitor gas trends closely (daily).")
                    st.write("- Check for loose connections.")
                    
    else:
        st.info("Awaiting input to start diagnosis...")

# Footer
st.markdown("---")
st.caption("MMU TES6313 Expert Systems Project | Developed by Group Cincai")