import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة واستخدام صورة اللوغو كأيقونة للمتصفح
st.set_page_config(
    page_title="EcoAudit AI - Enterprise Carbon Dashboard",
    page_icon="logo.png.jpg",
    layout="wide"
)

# 2. الهيكل الرئيسي لمحرك الحسابات (GHG Protocol Engine)
class EnterpriseCarbonAuditor:
    def __init__(self):
        self.emission_factors = {
            "diesel_liter": 2.68,
            "petrol_liter": 2.31,
            "electricity_kwh": 0.475,
            "natural_gas_m3": 1.90,
            "air_travel_km": 0.15
        }
        
    def calculate_audit(self, data):
        scope_1 = (data["diesel_liters"] * self.emission_factors["diesel_liter"]) + \
                  (data["petrol_liters"] * self.emission_factors["petrol_liter"]) + \
                  (data["gas_m3"] * self.emission_factors["natural_gas_m3"])
        
        scope_2 = data["electricity_kwh"] * self.emission_factors["electricity_kwh"]
        scope_3 = data["flight_km"] * self.emission_factors["air_travel_km"]
        
        total_co2_kg = scope_1 + scope_2 + scope_3
        total_co2_tons = total_co2_kg / 1000.0
        
        return {
            "Scope 1 (Direct)": round(scope_1 / 1000.0, 2),
            "Scope 2 (Electricity)": round(scope_2 / 1000.0, 2),
            "Scope 3 (Value Chain)": round(scope_3 / 1000.0, 2),
            "Total CO2e (Tons)": round(total_co2_tons, 2)
        }

    def simulate_decarbonization(self, current_audit, ev_fleet_pct, solar_energy_pct):
        reduced_scope_1 = current_audit["Scope 1 (Direct)"] * (1 - (ev_fleet_pct / 100.0))
        reduced_scope_2 = current_audit["Scope 2 (Electricity)"] * (1 - (solar_energy_pct / 100.0))
        
        new_total = reduced_scope_1 + reduced_scope_2 + current_audit["Scope 3 (Value Chain)"]
        saved_tons = current_audit["Total CO2e (Tons)"] - new_total
        reduction_rate = (saved_tons / current_audit["Total CO2e (Tons)"]) * 100 if current_audit["Total CO2e (Tons)"] > 0 else 0
        
        return {
            "New Total": round(new_total, 2),
            "Saved Tons": round(saved_tons, 2),
            "Reduction Rate": round(reduction_rate, 1)
        }

auditor = EnterpriseCarbonAuditor()

# 3. واجهة المستخدم مع دمج اللوغو
# إدراج اللوغو في أعلى القائمة الجانبية
st.sidebar.image("logo.png.jpg", use_container_width=True)
st.sidebar.markdown("---")

# عرض اللوغو مع العنوان الرئيسي في منتصف الشاشة
col_logo, col_title = st.columns([1, 4])
with col_logo:
    st.image("logo.png.jpg", width=120)

with col_title:
    st.title("EcoAudit AI: Enterprise Decarbonization Platform")
    st.caption("GHG Protocol Compliant Carbon Accounting & Strategic Decision Simulator")

st.markdown("---")

# القائمة الجانبية لإدخال البيانات
st.sidebar.header("📥 Annual Consumption Data")
company_name = st.sidebar.text_input("Company Name", "Global Logistics Corp")

diesel = st.sidebar.number_input("Fleet Diesel (Liters)", min_value=0, value=45000, step=1000)
petrol = st.sidebar.number_input("Fleet Petrol (Liters)", min_value=0, value=12000, step=500)
gas = st.sidebar.number_input("Natural Gas (m³)", min_value=0, value=5000, step=500)
electricity = st.sidebar.number_input("Electricity Usage (kWh)", min_value=0, value=180000, step=5000)
flights = st.sidebar.number_input("Employee Business Air Travel (km)", min_value=0, value=85000, step=5000)

input_data = {
    "diesel_liters": diesel,
    "petrol_liters": petrol,
    "gas_m3": gas,
    "electricity_kwh": electricity,
    "flight_km": flights
}

# إجراء الحسابات الحالية
current_results = auditor.calculate_audit(input_data)

# عرض التقرير الأساسي
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Footprint", f"{current_results['Total CO2e (Tons)']} Tons")
col2.metric("Scope 1 (Direct)", f"{current_results['Scope 1 (Direct)']} Tons")
col3.metric("Scope 2 (Grid Power)", f"{current_results['Scope 2 (Electricity)']} Tons")
col4.metric("Scope 3 (Travel & Value)", f"{current_results['Scope 3 (Value Chain)']} Tons")

st.markdown("---")

# قسم محاكي القرارات الاستراتيجية
st.header("🔮 Strategic Decarbonization Simulator")
st.write("Simulate investment decisions to forecast carbon reductions before execution.")

col_sim_1, col_sim_2 = st.columns(2)

with col_sim_1:
    st.subheader("⚙️ Action Parameters")
    ev_pct = st.slider("Convert Fleet to Electric Vehicles (EV %)", 0, 100, 40)
    solar_pct = st.slider("Transition to Solar Energy (Solar %)", 0, 100, 50)
    
    sim_results = auditor.simulate_decarbonization(current_results, ev_pct, solar_pct)

with col_sim_2:
    st.subheader("📈 Projected Environmental Impact")
    st.metric("New Projected Annual CO2e", f"{sim_results['New Total']} Tons", delta=f"-{sim_results['Saved Tons']} Tons ({sim_results['Reduction Rate']}%)")
    st.progress(sim_results['Reduction Rate'] / 100.0)

# رسم بياني للمقارنة
chart_data = pd.DataFrame({
    "Category": ["Scope 1", "Scope 2", "Scope 3"],
    "Current Baseline (Tons)": [
        current_results["Scope 1 (Direct)"], 
        current_results["Scope 2 (Electricity)"], 
        current_results["Scope 3 (Value Chain)"]
    ],
    "Simulated Target (Tons)": [
        round(current_results["Scope 1 (Direct)"] * (1 - (ev_pct / 100.0)), 2),
        round(current_results["Scope 2 (Electricity)"] * (1 - (solar_pct / 100.0)), 2),
        current_results["Scope 3 (Value Chain)"]
    ]
}).set_index("Category")

st.subheader("📊 Baseline vs. Simulated Emissions Breakdown")
st.bar_chart(chart_data)
# use "python -m streamlit run ECOAUDIT.py" to run the code please so it can work :)
