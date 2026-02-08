import streamlit as st
import pandas as pd
from main import calc_4_credit, calc_5_credit, calc_2_credit, grade_point

st.title("📊 SGPA Calculator — Table-Style Inputs")

# Subject definitions
subjects = [
    {"name": "Python", "credits":5, "has_lab":True, "has_int":True},
    {"name": "Physics", "credits":5, "has_lab":True, "has_int":True},
    {"name": "Electric", "credits":4, "has_lab":False, "has_int":True},
    {"name": "Mechanical", "credits":4, "has_lab":False, "has_int":True},
    {"name": "Math", "credits":4, "has_lab":False, "has_int":True},
    {"name": "EVS", "credits":2, "has_lab":False, "has_int":False}
]

# Create placeholders for inputs
inputs = {}

# Build table-style inputs
st.write("Enter the marks in the table below:")

for sub in subjects:
    name = sub["name"]
    cols = st.columns([2,1,1,1,1,1])
    cols[0].write(f"**{name} ({sub['credits']} cr)**")
    
    # ISA1/ISA2 ranges
    if name == "EVS":
        inputs[f"{name}_isa1"] = cols[1].number_input("ISA1 (0–30)", 0, 30, key=f"{name}_isa1")
        inputs[f"{name}_isa2"] = cols[2].number_input("ISA2 (0–30)", 0, 30, key=f"{name}_isa2")
        # no internals for EVS
        cols[3].write("Int —")
        inputs[f"{name}_esa"] = cols[4].number_input("ESA (0–50)", 0, 50, key=f"{name}_esa")
        cols[5].write("Lab —")
    else:
        inputs[f"{name}_isa1"] = cols[1].number_input("ISA1 (0–40)", 0, 40, key=f"{name}_isa1")
        inputs[f"{name}_isa2"] = cols[2].number_input("ISA2 (0–40)", 0, 40, key=f"{name}_isa2")
        if sub["has_int"]:
            inputs[f"{name}_int"] = cols[3].number_input("Int (0–10)", 0, 10, key=f"{name}_int")
        else:
            cols[3].write("Int —")
        inputs[f"{name}_esa"] = cols[4].number_input("ESA (0–100)", 0, 100, key=f"{name}_esa")
        if sub["has_lab"]:
            inputs[f"{name}_lab"] = cols[5].number_input("Lab (0–20)", 0, 20, key=f"{name}_lab")
        else:
            cols[5].write("Lab —")

st.write("---")

if st.button("📡 Calculate SGPA"):
    results = []
    total_points = 0
    credit_sum = 0

    for sub in subjects:
        name = sub["name"]
        cr = sub["credits"]

        # EVS logic
        if name == "EVS":
            isa1 = inputs[f"{name}_isa1"]
            isa2 = inputs[f"{name}_isa2"]
            esa  = inputs[f"{name}_esa"]
            final = calc_2_credit(isa1, isa2, esa)
        elif cr == 5:
            isa1 = inputs[f"{name}_isa1"]
            isa2 = inputs[f"{name}_isa2"]
            internals = inputs[f"{name}_int"]
            esa = inputs[f"{name}_esa"]
            lab = inputs[f"{name}_lab"]
            final = calc_5_credit(isa1, isa2, internals, esa, lab)
        else:
            isa1 = inputs[f"{name}_isa1"]
            isa2 = inputs[f"{name}_isa2"]
            internals = inputs[f"{name}_int"]
            esa = inputs[f"{name}_esa"]
            final = calc_4_credit(isa1, isa2, internals, esa)

        # grade and grade points
        gp = grade_point(final)
        total_points += gp * cr
        credit_sum += cr

        results.append({
            "Subject": name,
            "Final %": round(final,2),
            "Grade": "S" if final>=90 else "A" if final>=80 else "B" if final>=70 else "C" if final>=60 else "D" if final>=50 else "F",
            "Grade Point": gp
        })

    df = pd.DataFrame(results)
    st.write("### 📋 Results Table")
    st.dataframe(df)

    sgpa = total_points / credit_sum
    st.write(f"### 🎓 Final SGPA: **{sgpa:.2f}**")



