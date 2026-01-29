import streamlit as st
import clips  # 需要 pip install clipspy

# ==========================================
# 1. SETUP CLIPS ENGINE
# ==========================================
def run_clips_engine(h2, ch4, c2h2, c2h4, c2h6):
    try:
        # 创建环境
        env = clips.Environment()
        
        # 加载你的规则文件 (确保 rules.clp 在同一个文件夹)
        env.load('rules.clp') 
        
        # 将用户数据转换成 CLIPS 的 Facts
        # 对应你的 (deftemplate gas (slot name) (slot value))
        env.assert_string(f'(gas (name H2) (value {h2}))')
        env.assert_string(f'(gas (name CH4) (value {ch4}))')
        env.assert_string(f'(gas (name C2H2) (value {c2h2}))')
        env.assert_string(f'(gas (name C2H4) (value {c2h4}))')
        env.assert_string(f'(gas (name C2H6) (value {c2h6}))')
        
        # 运行引擎
        env.run()
        
        # 抓取结果
        # 我们遍历所有的 Facts，找到 template 叫 'diagnosis' 的那个
        final_fault = "Unknown"
        
        for fact in env.facts():
            if fact.template.name == 'diagnosis':
                # 获取 slot 'fault' 的值
                final_fault = fact['fault']
                break # 找到一个就够了
                
        return final_fault

    except Exception as e:
        return f"Error: {e}"

# ==========================================
# 2. STREAMLIT GUI
# ==========================================
st.set_page_config(page_title="Transformer Diagnosis (CLIPS)", page_icon="⚡")
st.title("⚡ Transformer Fault Diagnosis (CLIPS Engine)")

st.sidebar.header("Input Gas Data (ppm)")
h2 = st.sidebar.number_input("H2", value=0.0)
ch4 = st.sidebar.number_input("CH4", value=0.0)
c2h2 = st.sidebar.number_input("C2H2", value=0.0)
c2h4 = st.sidebar.number_input("C2H4", value=0.0)
c2h6 = st.sidebar.number_input("C2H6", value=0.0)

if st.button("Run Diagnosis"):
    st.write("Processing with CLIPS 6.4...")
    
    # 调用上面的函数
    result = run_clips_engine(h2, ch4, c2h2, c2h4, c2h6)
    
    if "Error" in result:
        st.error(result)
    elif result == "Normal Condition":
        st.success(f"✅ Diagnosis: {result}")
    else:
        st.error(f"⚠️ Diagnosis: {result}")