import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score

# ==========================================
# 1. 推理引擎 
# ==========================================
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
        fault_scores["Partial Discharge"] += 1
    if r_ch4_h2 < 0.1:
        fault_scores["Partial Discharge"] += 1

    # ---------------- Arcing ----------------
    if r_c2h2_c2h4 > 1:
        fault_scores["Low Energy Arcing"] += 1
    if 0.1 <= r_c2h2_c2h4 <= 1:
        fault_scores["High Energy Arcing"] += 1

    # ---------------- Thermal ----------------
    if r_ch4_h2 > 1 and r_c2h4_c2h6 < 1:
        fault_scores["Thermal Fault T1 (<300°C)"] += 1
    if 1 <= r_c2h4_c2h6 < 3:
        fault_scores["Thermal Fault T2 (300–700°C)"] += 1
    if r_c2h4_c2h6 >= 3:
        fault_scores["Thermal Fault T3 (>700°C)"] += 1

    # ---------------- Mixed ----------------
    if gases['C2H2'] > 10 and gases['C2H4'] > 100:
        fault_scores["Mixed Fault"] += 1

    final_fault = max(fault_scores, key=fault_scores.get)
    if fault_scores[final_fault] == 0:
        final_fault = "Normal Condition"

    return final_fault

# ==========================================
# 2. Real-World Stress Test
# ==========================================
def generate_stress_dataset(num_samples=1000):
    data = []
    count = num_samples // 8

    # 輔助函數：添加 ±15% 的隨機雜訊 (模擬真實感測器誤差)
    def add_noise(val):
        factor = random.uniform(0.85, 1.15)
        return max(0.1, val * factor)

    for _ in range(count):
        # 1. PARTIAL DISCHARGE
        # 基礎值: H2=1000 (高), CH4=20 (低)。雜訊可能導致 CH4 變高，影響 Ratio。
        base = {'H2': 1000, 'CH4': 20, 'C2H2': 1, 'C2H4': 1, 'C2H6': 1, 'Actual': 'Partial Discharge'}
        data.append({k: add_noise(v) if k != 'Actual' else v for k, v in base.items()})

        # 2. LOW ENERGY ARCING
        # 基礎值: Ratio=2.0 (安全)。雜訊可能導致 Ratio < 1，變成 High Energy。
        base = {'H2': 10, 'CH4': 10, 'C2H2': 200, 'C2H4': 100, 'C2H6': 10, 'Actual': 'Low Energy Arcing'}
        data.append({k: add_noise(v) if k != 'Actual' else v for k, v in base.items()})

        # 3. HIGH ENERGY ARCING
        # 基礎值: Ratio=0.5 (安全)。雜訊可能導致 Ratio < 0.1 或 > 1。
        base = {'H2': 10, 'CH4': 10, 'C2H2': 50, 'C2H4': 100, 'C2H6': 10, 'Actual': 'High Energy Arcing'}
        data.append({k: add_noise(v) if k != 'Actual' else v for k, v in base.items()})

        # 4. THERMAL T1
        # 基礎值: Ratio CH4/H2=4.0, C2H4/C2H6=0.25。雜訊可能導致比率越界。
        base = {'H2': 50, 'CH4': 200, 'C2H2': 1, 'C2H4': 50, 'C2H6': 200, 'Actual': 'Thermal Fault T1 (<300°C)'}
        data.append({k: add_noise(v) if k != 'Actual' else v for k, v in base.items()})

        # 5. THERMAL T2
        # 基礎值: Ratio=2.0 (在 1-3 中間)。雜訊可能導致 Ratio > 3 (變成 T3) 或 < 1 (變成 T1)。
        base = {'H2': 10, 'CH4': 10, 'C2H2': 1, 'C2H4': 200, 'C2H6': 100, 'Actual': 'Thermal Fault T2 (300–700°C)'}
        data.append({k: add_noise(v) if k != 'Actual' else v for k, v in base.items()})

        # 6. THERMAL T3
        # 基礎值: Ratio=6.0 (遠大於 3)。非常穩健，應該很少錯。
        base = {'H2': 10, 'CH4': 10, 'C2H2': 1, 'C2H4': 600, 'C2H6': 100, 'Actual': 'Thermal Fault T3 (>700°C)'}
        data.append({k: add_noise(v) if k != 'Actual' else v for k, v in base.items()})

        # 7. MIXED FAULT
        # 基礎值: C2H2=20 (>10), C2H4=500 (>100)。避開 Arcing Ratio。
        # 雜訊可能導致 C2H2 變低 (<10)，導致規則失效，變成 Thermal T3。這就是真實的錯誤！
        base = {'H2': 100, 'CH4': 10, 'C2H2': 20, 'C2H4': 500, 'C2H6': 1000, 'Actual': 'Mixed Fault'}
        data.append({k: add_noise(v) if k != 'Actual' else v for k, v in base.items()})

        # 8. NORMAL
        base = {'H2': 20, 'CH4': 20, 'C2H2': 1, 'C2H4': 10, 'C2H6': 10, 'Actual': 'Normal Condition'}
        data.append({k: add_noise(v) if k != 'Actual' else v for k, v in base.items()})

    random.shuffle(data)
    return data

# ==========================================
# 3. 執行
# ==========================================
print("--- RUNNING REALISTIC STRESS TEST (N=1000) ---")
test_data = generate_stress_dataset(1000)
df = pd.DataFrame(test_data)

predictions = []
for index, row in df.iterrows():
    input_gases = {k: row[k] for k in ['H2', 'CH4', 'C2H2', 'C2H4', 'C2H6']}
    predictions.append(diagnose_transformer(input_gases))

df['Predicted'] = predictions

# Metrics
acc = accuracy_score(df['Actual'], df['Predicted'])
print(f"✅ Accuracy: {acc*100:.2f}% (Realistic Stress Test)")

# Chart
plt.figure(figsize=(10, 8))
cm = confusion_matrix(df['Actual'], df['Predicted'])
labels = sorted(list(set(df['Actual'])))

sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', xticklabels=labels, yticklabels=labels)
plt.title(f'Robustness Stress Test (Noise ±15%)\nAccuracy: {acc*100:.1f}%')
plt.ylabel('Actual Fault')
plt.xlabel('Predicted Fault')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.savefig('confusion_matrix_stress.png')
df.to_csv('validation_data_stress.csv', index=False)
print("📸 Saved 'confusion_matrix_stress.png'")