import streamlit as st
import pandas as pd
import joblib
import time

# ----------------------------
# Load Model
# ----------------------------
model = joblib.load("water_quality_model.pkl")

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Water Quality Prediction",
    page_icon="💧",
    layout="wide"
)

# ----------------------------
# CSS
# ----------------------------
st.markdown("""
<style>

.main{
    background:#F8FCFF;
}

.block-container{
    padding-top:1rem;
}

.title{
    text-align:center;
    color:#0077B6;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
}

.stButton>button{
    width:100%;
    background:#0096C7;
    color:white;
    border-radius:10px;
    height:55px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#0077B6;
    color:white;
}

div[data-testid="metric-container"]{
    background:#EEF8FF;
    border-radius:10px;
    padding:15px;
}

</style>
""",unsafe_allow_html=True)

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.title("💧 Water Quality")

st.sidebar.markdown("---")

st.sidebar.write("**Algorithm**")

st.sidebar.success("Random Forest")

st.sidebar.write("**Input Features**")

st.sidebar.info("9 Parameters")

st.sidebar.markdown("---")

st.sidebar.write("Enter all values and click Predict.")

# ----------------------------
# Heading
# ----------------------------

st.markdown('<p class="title">💧 Water Quality Prediction</p>',unsafe_allow_html=True)

st.markdown('<p class="subtitle">Predict whether water is safe for drinking.</p>',unsafe_allow_html=True)

st.divider()

# ----------------------------
# Inputs
# ----------------------------

left,right=st.columns(2)

with left:

    ph=st.number_input("pH",0.0,14.0,7.0)

    hardness=st.number_input("Hardness",0.0,500.0,200.0)

    solids=st.number_input("Solids",0.0,70000.0,20000.0)

    chloramines=st.number_input("Chloramines",0.0,15.0,7.0)

    sulfate=st.number_input("Sulfate",0.0,500.0,330.0)

with right:

    conductivity=st.number_input("Conductivity",0.0,1000.0,420.0)

    organic_carbon=st.number_input("Organic Carbon",0.0,30.0,14.0)

    trihalomethanes=st.number_input("Trihalomethanes",0.0,150.0,65.0)

    turbidity=st.number_input("Turbidity",0.0,10.0,4.0)

st.divider()

# ----------------------------
# Predict
# ----------------------------

if st.button("🔍 Predict"):

    input_df=pd.DataFrame({

        "ph":[ph],

        "Hardness":[hardness],

        "Solids":[solids],

        "Chloramines":[chloramines],

        "Sulfate":[sulfate],

        "Conductivity":[conductivity],

        "Organic_carbon":[organic_carbon],

        "Trihalomethanes":[trihalomethanes],

        "Turbidity":[turbidity]

    })

    with st.spinner("Analyzing water quality..."):

        time.sleep(1.5)

    prediction=model.predict(input_df)[0]

    confidence=max(model.predict_proba(input_df)[0])*100

    c1,c2=st.columns(2)

    with c1:

        if prediction==1:

            st.metric("Prediction","Safe Water ✅")

        else:

            st.metric("Prediction","Unsafe Water ❌")

    with c2:

        st.metric("Confidence",f"{confidence:.2f}%")

    st.progress(int(confidence))

    if prediction==1:

        st.balloons()

        st.success("The given water sample is safe for drinking.")

    else:

        st.error("The given water sample is not safe for drinking.")

    st.subheader("Input Summary")

    st.dataframe(
        input_df,
        use_container_width=True
    )

    st.subheader("Recommendations")

    if prediction==1:

        st.success("""
✔ Safe for Drinking

✔ Safe for Cooking

✔ Suitable for Household Use
""")

    else:

        st.warning("""
• Boil the water before use

• Use RO/UV filtration

• Test the water in a laboratory

• Avoid direct drinking
""")

st.divider()

st.caption("Water Quality Prediction")