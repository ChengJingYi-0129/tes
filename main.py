import streamlit as st
import clips # 这里调用 clipspy

# ==========================================
# 1. CLIPS ENGINE FUNCTION
# ==========================================
def run_clips_logic(input_gases):
    """
    Load rules.clp, insert user data, and run the engine.
    """
    try:
        # 创建 CLIPS 环境
        env = clips.Environment()
        
        # 加载规则文件
        # ⚠️ 确保 rules.clp 和 app.py 在同一个文件夹！
        env.load('rules.clp') 
        
        # 将 Python 的数据转换成 CLIPS 的格式 (Assert Facts)
        # 对应 rules.clp 里的 (deftemplate gas (slot name) (slot value))
        env.assert_string(f'(gas (name H2) (value {input_gases["H2"]}))')
        env.assert_string(f'(gas (name CH4) (value {input_gases["CH4"]}))')
        env.assert_string(f'(gas (name C2H2) (value {input_gases["C2H2"]}))')
        env.assert_string(f'(gas (name C2H4) (value {input_gases["C2H4"]}))')
        env.assert_string(f'(gas (name C2H6) (value {input_gases["C2H6"]}))')
        
        # 运行引擎 (Run)
        env.run()
        
        # 从 CLIPS 中提取结果 (Retrieving Facts)
        diagnosis_result = "Normal Condition" # 默认值
        
        # 遍历所有 Facts，寻找 template 是 'diagnosis' 的那个
        for fact in env.facts():
            if fact.template.name == 'diagnosis':
                diagnosis_result = fact['fault']
                # 找到一个故障后，可以 break，或者收集所有故障
                # 这里简单起见，取最后一个被触发的故障
        
        return diagnosis_result

    except Exception as e:
        return f"Error loading CLIPS: {e}"

# ==========================================
# 2. STREAMLIT GUI
# ==========================================

st.set_page_config(page_title="Transformer Fault Diagnosis", page_icon="⚡")

# Header
st.title("⚡ Transformer Fault Diagnosis")
st.markdown("**Core Engine:** CLIPS (C Language Integrated Production System) 6.4")
st.markdown("---")

# Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Input Gas Data (ppm)")
    
    h2 = st.number_input("Hydrogen (H2)", value=180.0)
    ch4 = st.number_input("Methane (CH4)", value=90.0)
    c2h2 = st.number_input("Acetylene (C2H2)", value=2.0)
    c2h4 = st.number_input("Ethylene (C2H4)", value=40.0)
    c2h6 = st.number_input("Ethane (C2H6)", value=50.0)

    # 包装数据
    user_data = {
        'H2': h2, 'CH4': ch4, 'C2H2': c2h2, 'C2H4': c2h4, 'C2H6': c2h6
    }

with col2:
    st.subheader("🔍 Diagnosis Result")
    
    if st.button("Run CLIPS Engine", type="primary"):
        with st.spinner("Reasoning with CLIPS rules..."):
            
            # 调用 CLIPS
            result = run_clips_logic(user_data)
            
            # 显示结果
            if "Error" in result:
                st.error(result)
                st.write("Make sure 'rules.clp' is in the same folder.")
            elif result == "Normal Condition":
                st.success(f"✅ {result}")
            else:
                st.error(f"⚠️ Fault Detected: **{result}**")
                
                # 额外展示一下比率，显得更专业
                st.info("Logic Source: `rules.clp` file executed successfully.")

# Footer
st.markdown("---")
st.caption("Multimedia University | TES6313 Expert Systems Project")