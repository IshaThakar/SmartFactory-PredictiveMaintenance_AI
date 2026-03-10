import streamlit as st
import joblib
import numpy as np
import random
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

model = joblib.load("machine_model.pkl")

st.set_page_config(layout="wide")

st.title("🏭 Smart Factory Digital Twin Control Center")

# auto refresh every 3 seconds
st_autorefresh(interval=3000, key="datarefresh")

machines = ["Machine A","Machine B","Machine C","Machine D"]

# Generate shared machine data
machine_data = {}

for machine in machines:

    air_temp = random.randint(295,305)
    process_temp = random.randint(305,315)
    speed = random.randint(1000,3000)
    torque = random.randint(10,80)
    tool_wear = random.randint(0,300)

    input_data = np.array([[air_temp,process_temp,speed,torque,tool_wear]])
    probability = model.predict_proba(input_data)[0][1]

    machine_data[machine] = {
        "air":air_temp,
        "process":process_temp,
        "speed":speed,
        "torque":torque,
        "wear":tool_wear,
        "risk":round(probability*100,2)
    }

tab1, tab2 = st.tabs(["Live Machine Monitoring","🏭 Factory Overview"])

# -------- LIVE MACHINE --------

with tab1:

    machine = st.selectbox("Select Machine",machines)

    data = machine_data[machine]

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("Air Temperature",data["air"])
        st.metric("Process Temperature",data["process"])

    with col2:
        st.metric("Rotational Speed",data["speed"])
        st.metric("Torque",data["torque"])

    with col3:
        st.metric("Tool Wear",data["wear"])

    risk = data["risk"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={'text':"Failure Probability %"},
        gauge={
          'axis':{'range':[None,100]},
          'bar': {'color': "black", 'thickness': 0.25},
          'steps':[
              {'range':[0,40],'color':"green"},
              {'range':[40,70],'color':"yellow"},
              {'range':[70,100],'color':"red"}]
    })) 

    st.plotly_chart(fig,use_container_width=True)

    if risk > 70:
        st.error("🔴 Critical Risk")

    elif risk > 40:
        st.warning("🟡 Maintenance Required Soon")

    else:
        st.success("🟢 Healthy")


# -------- FACTORY OVERVIEW --------

with tab2:

    cols = st.columns(4)

    for i,machine in enumerate(machines):

        data = machine_data[machine]

        with cols[i]:

            st.subheader(machine)

            st.metric("Failure Risk %",data["risk"])

            if data["risk"] > 70:
                st.error("🔴 Critical")

            elif data["risk"] > 40:
                st.warning("🟡 Warning")

            else:
                st.success("🟢 Healthy")
# ---------------- MACHINE HEALTH TIMELINE ----------------

with st.tabs(["📈 Machine Health Timeline"])[0]:

    st.subheader("Machine Degradation Timeline")

    machine = st.selectbox(
        "Select Machine for Health Timeline",
        machines,
        key="timeline_machine"
    )

    # create fake historical health data
    history = []
    timestamps = []

    for i in range(20):

        air_temp = random.randint(295,305)
        process_temp = random.randint(305,315)
        speed = random.randint(1000,3000)
        torque = random.randint(10,80)
        tool_wear = random.randint(0,300)

        input_data = np.array([[air_temp,process_temp,speed,torque,tool_wear]])
        probability = model.predict_proba(input_data)[0][1]

        history.append(round(probability*100,2))
        timestamps.append(i)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=timestamps,
        y=history,
        mode='lines+markers',
        name='Failure Risk %'
    ))

    fig.update_layout(
        title=f"{machine} Health Degradation Over Time",
        xaxis_title="Time",
        yaxis_title="Failure Probability %",
        yaxis=dict(range=[0,100])
    )

    st.plotly_chart(fig, use_container_width=True)