import streamlit as st
import clips 

# ==========================================
# 1. CLIPS ENGINE FUNCTION
# ==========================================
def run_clips_logic(input_gases):
    """
    Load ExpertSystem.clp, insert user data, and run the engine.
    """
    try:

        env = clips.Environment()
        

        env.load('ExpertSystem.clp') 

        env.assert_string(f'(gas (name H2) (value {input_gases["H2"]}))')
        env.assert_string(f'(gas (name CH4) (value {input_gases["CH4"]}))')
        env.assert_string(f'(gas (name C2H2) (value {input_gases["C2H2"]}))')
        env.assert_string(f'(gas (name C2H4) (value {input_gases["C2H4"]}))')
        env.assert_string(f'(gas (name C2H6) (value {input_gases["C2H6"]}))')
        

        env.run()

        diagnosis_result = "Normal Condition" 
        

        for fact in env.facts():
            if fact.template.name == 'diagnosis':
                diagnosis_result = fact['fault']
        
        return diagnosis_result

    except Exception as e:
        return f"Error loading CLIPS: {e}"

# ==========================================
# 2. STREAMLIT GUI
# ==========================================

st.set_page_config(page_title="Transformer Fault Diagnosis")

# Header
st.title("Transformer Fault Diagnosis")
st.markdown("**Core Engine:** CLIPS (C Language Integrated Production System) 6.4")
st.markdown("---")

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Gas Data (ppm)")
    
    h2 = st.number_input("Hydrogen (H2)", value=0.0)
    ch4 = st.number_input("Methane (CH4)", value=0.0)
    c2h2 = st.number_input("Acetylene (C2H2)", value=.0)
    c2h4 = st.number_input("Ethylene (C2H4)", value=.0)
    c2h6 = st.number_input("Ethane (C2H6)", value=.0)

    # 包装数据
    user_data = {
        'H2': h2, 'CH4': ch4, 'C2H2': c2h2, 'C2H4': c2h4, 'C2H6': c2h6
    }

with col2:
    st.subheader("Diagnosis Result")
    
    if st.button("Run CLIPS Engine", type="primary"):
        with st.spinner("Reasoning with CLIPS rules..."):
            
            result = run_clips_logic(user_data)
            
            if "Error" in result:
                st.error(result)
                st.write("Make sure 'ExpertSystem.clp' is in the same folder.")
            elif result == "Normal Condition":
                st.success(f"{result}")
            else:
                st.error(f"Fault Detected: **{result}**")
                
                st.info("Logic Source: `ExpertSystem.clp` file executed successfully.")

# Footer
st.markdown("---")
st.caption("Multimedia University | TES6313 Expert Systems Project By Group Cincai")