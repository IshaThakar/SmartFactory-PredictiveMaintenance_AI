import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# ---------------- FIREBASE INITIALIZATION ----------------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred,{
        "databaseURL":"https://smart-factory-ai-default-rtdb.firebaseio.com/"
    })

import streamlit as st
import joblib
import numpy as np
import random
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import os
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingRegressor

# ---------------- CACHE MODELS ----------------
@st.cache_resource
def load_main_model():
    return joblib.load("machine_model.pkl")

model = load_main_model()

# ---------------- LOAD / TRAIN RUL MODEL ----------------
@st.cache_resource
def load_rul_model():

    if os.path.exists("rul_model.pkl"):
        return joblib.load("rul_model.pkl")

    X=[]
    y=[]

    for i in range(300):

        air=random.randint(295,305)
        process=random.randint(305,315)
        speed=random.randint(1000,3000)
        torque=random.randint(10,80)
        wear=random.randint(0,300)

        risk=(wear/300)*100
        rul=max(1,(100-risk)*1.5)

        X.append([air,process,speed,torque,wear])
        y.append(rul)

    X=np.array(X)
    y=np.array(y)

    model=GradientBoostingRegressor()
    model.fit(X,y)

    joblib.dump(model,"rul_model.pkl")

    return model

rul_model = load_rul_model()

# ---------------- LOAD / TRAIN DIAGNOSIS MODEL ----------------
@st.cache_resource
def load_diagnosis_model():

    if os.path.exists("diagnosis_model.pkl"):
        return joblib.load("diagnosis_model.pkl")

    X=[]
    y=[]

    for i in range(500):

        air=random.randint(295,305)
        process=random.randint(305,315)
        speed=random.randint(1000,3000)
        torque=random.randint(10,80)
        wear=random.randint(0,300)

        if wear>220:
            label="Tool Wear Failure"
        elif torque>70:
            label="Mechanical Overload"
        elif process>312:
            label="Cooling System Failure"
        elif speed>2800:
            label="Bearing Stress"
        else:
            label="Healthy"

        X.append([air,process,speed,torque,wear])
        y.append(label)

    model=RandomForestClassifier()
    model.fit(X,y)

    joblib.dump(model,"diagnosis_model.pkl")

    return model

diagnosis_model = load_diagnosis_model()

machines = ["Machine A","Machine B","Machine C","Machine D"]

# ---------------- PREPROCESSING ----------------
def preprocess_data(a,p,s,t,w):
    return np.array([[float(a),float(p),float(s),float(t),float(w)]])

# ---------------- AUTO MODEL RETRAINING ----------------
def retrain_model():

    base = "alert_logs"
    dfs = []

    if not os.path.exists(base):
        return False

    for root, dirs, files in os.walk(base):
        for file in files:
            if file.endswith(".csv"):
                df = pd.read_csv(os.path.join(root,file))
                dfs.append(df)

    if len(dfs) == 0:
        return False

    data = pd.concat(dfs)

    data["failure"] = data["failure_risk"].apply(lambda x: 1 if x > 70 else 0)

    X = data[
        ["air_temp","process_temp","speed","torque","tool_wear"]
    ]

    y = data["failure"]

    new_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    new_model.fit(X,y)

    joblib.dump(new_model,"machine_model.pkl")

    return True

# ---------------- DATA RETENTION SYSTEM ----------------
def manage_old_logs():

    base="alert_logs"

    if not os.path.exists(base):
        return

    cutoff=datetime.now()-timedelta(days=60)

    for root,dirs,files in os.walk(base):

        for file in files:

            if file.endswith(".csv"):

                path=os.path.join(root,file)

                df=pd.read_csv(path)

                df["timestamp"]=pd.to_datetime(df["timestamp"])

                old=df[df["timestamp"]<cutoff]

                if len(old)==0:
                    continue

                critical=old[old["failure_risk"]>=70]

                if len(critical)>0:

                    os.makedirs("critical_logs",exist_ok=True)

                    critical.to_csv(
                        f"critical_logs/critical_{file}",
                        mode="a",
                        header=not os.path.exists(f"critical_logs/critical_{file}"),
                        index=False
                    )

                df=df[df["timestamp"]>=cutoff]

                df.to_csv(path,index=False)

# ---------------- FEEDBACK LOOP LOGGING ----------------
def log_machine_data(machine,data):

    now=datetime.now()

    year=now.strftime("%Y")
    month=now.strftime("%B")
    week=(now.day-1)//7+1

    machine_folder=machine.replace(" ","_")

    base=f"alert_logs/{year}/{month}/{machine_folder}"

    os.makedirs(base,exist_ok=True)

    path=f"{base}/week_{week}.csv"

    record={
        "timestamp":now,
        "machine":machine,
        "air_temp":data["air"],
        "process_temp":data["process"],
        "speed":data["speed"],
        "torque":data["torque"],
        "tool_wear":data["wear"],
        "failure_risk":data["risk"]
    }

    df=pd.DataFrame([record])

    if os.path.exists(path):
        df.to_csv(path,mode="a",header=False,index=False)
    else:
        df.to_csv(path,index=False)

# ---------------- FIREBASE PUSH ----------------
def send_raw_to_firebase(machine,air,process,speed,torque,wear):

    if "last_firebase_push" not in st.session_state:
        st.session_state.last_firebase_push = datetime.now()

    if datetime.now() - st.session_state.last_firebase_push < timedelta(seconds=20):
        return

    ref = db.reference("sensor_data")

    ref.child(machine.replace(" ","_")).push({
        "timestamp": str(datetime.now()),
        "air_temp": air,
        "process_temp": process,
        "speed": speed,
        "torque": torque,
        "tool_wear": wear
    })

    st.session_state.last_firebase_push = datetime.now()

# ---------------- UI ----------------
st.set_page_config(layout="wide")
st.title("🏭 Smart Factory Digital Twin Control Center")

# refresh every 30 seconds
st_autorefresh(interval=30000,key="refresh")

# cleanup every 10 minutes
if "last_cleanup" not in st.session_state:
    st.session_state.last_cleanup=datetime.now()

if datetime.now()-st.session_state.last_cleanup>timedelta(minutes=10):
    manage_old_logs()
    st.session_state.last_cleanup=datetime.now()

# ---------------- AUTO RETRAIN TIMER ----------------
if "last_retrain" not in st.session_state:
    st.session_state.last_retrain = datetime.now()

if datetime.now() - st.session_state.last_retrain > timedelta(minutes=30):

    success = retrain_model()

    if success:
        st.toast("✅ Model retrained successfully using latest machine logs", icon="🤖")

    st.session_state.last_retrain = datetime.now()

# ---------------- MACHINE DATA ----------------
machine_data={}

for m in machines:

    air=random.randint(295,305)
    process=random.randint(305,315)
    speed=random.randint(1000,3000)
    torque=random.randint(10,80)
    wear=random.randint(0,300)
    
    send_raw_to_firebase(m,air,process,speed,torque,wear)

    inp=preprocess_data(air,process,speed,torque,wear)

    prob=model.predict_proba(inp)[0][1]
    rul_pred=rul_model.predict(inp)[0]
    diagnosis=diagnosis_model.predict(inp)[0]

    data={
        "air":air,
        "process":process,
        "speed":speed,
        "torque":torque,
        "wear":wear,
        "risk":round(prob*100,2),
        "rul":round(rul_pred,2),
        "diagnosis":diagnosis
    }

    machine_data[m]=data
    log_machine_data(m,data)

# ---------------- FACTORY ALERT SYSTEM ----------------
critical_machines=[]

for m in machines:
    if machine_data[m]["risk"]>70:
        critical_machines.append(m)

for m in critical_machines:
    st.toast(f"🚨 ALERT: {m} may fail soon!", icon="⚠")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🔴 Live Machine Monitoring",
    "🏭 Factory Overview",
    "📈 Machine Timeline",
    "📜 Alert History"
])

# ======================================================
# TAB 1
# ======================================================

with tab1:

    machine=st.selectbox("Select Machine",machines,key="live")

    data=machine_data[machine]

    c1,c2,c3=st.columns(3)

    with c1:
        st.metric("Air Temp",data["air"])
        st.metric("Process Temp",data["process"])

    with c2:
        st.metric("Speed",data["speed"])
        st.metric("Torque",data["torque"])

    with c3:
        st.metric("Tool Wear",data["wear"])

    risk=data["risk"]

    if risk>70:
        st.error(f"⚠ Critical Risk - {machine} may fail soon!")
        st.toast(f"🚨 {machine} may fail soon!", icon="⚠")
    elif risk>40:
        st.warning("Maintenance Soon")
    else:
        st.success("Healthy")

    st.divider()

    health=100-risk
    damage=risk

    a,b=st.columns(2)

    with a:
        st.markdown(f"""
        <div style="background:#e8f5e9;padding:30px;border-radius:10px;text-align:center;">
        <h2>Machine Health</h2>
        <h1 style="font-size:60px;color:green;">{health:.1f}%</h1>
        </div>
        """,unsafe_allow_html=True)

    with b:
        st.markdown(f"""
        <div style="background:#ffebee;padding:30px;border-radius:10px;text-align:center;">
        <h2>Damage Level</h2>
        <h1 style="font-size:60px;color:red;">{damage:.1f}%</h1>
        </div>
        """,unsafe_allow_html=True)

    # ---------------- ISSUE DIAGNOSIS ----------------

    st.subheader("Issue Diagnosis & Suggested Solution")

    solution = "Machine operating normally."

    if data["wear"] > 200:
        solution = "High Tool Wear detected. Replace cutting tool."

    elif data["process"] > 312:
        solution = "Process temperature high. Check cooling system."

    elif data["torque"] > 70:
        solution = "High torque detected. Inspect mechanical load."

    elif data["speed"] > 2800:
        solution = "Rotational speed too high. Reduce RPM."

    st.info(solution)

    st.divider()

    # ---------------- REMAINING TIME ----------------

    st.subheader("Estimated Remaining Operating Time")

    failure_prob = risk / 100

    if failure_prob < 0.3:
        time_left = "More than 24 hours"
    elif failure_prob < 0.6:
        time_left = "Approximately 6–12 hours"
    else:
        time_left = "Less than 1 hour"

    st.write(f"Estimated Time Before Failure: **{time_left}**")

    st.divider()

    # ---------------- MAINTENANCE ----------------

    st.subheader("Recommended Maintenance Schedule")

    if risk < 30:
        schedule = "Next routine maintenance within 1 week"
    elif risk < 60:
        schedule = "Maintenance recommended within 48 hours"
    else:
        schedule = "Immediate maintenance required"

    st.write(schedule)

# ======================================================
# TAB 2
# ======================================================

with tab2:

    cols=st.columns(4)

    for i,m in enumerate(machines):

        d=machine_data[m]

        with cols[i]:

            st.subheader(m)
            st.metric("Failure Risk %",d["risk"])

            if d["risk"]>70:
                st.error("Critical")
            elif d["risk"]>40:
                st.warning("Warning")
            else:
                st.success("Healthy")
# ---------------- TAB 3 ----------------
with tab3:

    tm = st.selectbox("Select Machine", machines, key="tab3_machine")

    history=[]
    time_idx=[]

    ref = db.reference(f"sensor_data/{tm.replace(' ','_')}")
    data_snapshot = ref.order_by_key().limit_to_last(20).get()

    if data_snapshot:

        sorted_entries = sorted(data_snapshot.items(), key=lambda x: x[1].get('timestamp', ''))

        for i,(key,entry) in enumerate(sorted_entries):

            a=entry.get("air_temp",0)
            p=entry.get("process_temp",0)
            s=entry.get("speed",0)
            t=entry.get("torque",0)
            w=entry.get("tool_wear",0)

            inp=preprocess_data(a,p,s,t,w)
            prob=model.predict_proba(inp)[0][1]

            history.append(prob*100)
            time_idx.append(i)

        fig=go.Figure()

        fig.add_trace(go.Scatter(
            x=time_idx,
            y=history,
            mode="lines+markers",
            name=f"{tm} Risk"
        ))

        fig.update_layout(
            title=f"{tm} Health Timeline",
            xaxis_title="Time (Latest 20 Entries)",
            yaxis_title="Failure Probability %",
            yaxis=dict(range=[0,100])
        )

        st.plotly_chart(fig,use_container_width=True)

    else:
        st.info("No sensor data available in Firebase yet")
# ======================================================
# TAB 4
# ======================================================

with tab4:

    st.subheader("Alert History")

    machine=st.selectbox("Machine",machines,key="history_machine")

    year=st.text_input("Year","2026")

    month=st.text_input("Month (Example: March)","March")

    day=st.text_input("Day (optional)","")

    folder=f"alert_logs/{year}/{month}/{machine.replace(' ','_')}"

    dfs=[]

    if os.path.exists(folder):

        for f in os.listdir(folder):

            if f.endswith(".csv"):

                df=pd.read_csv(os.path.join(folder,f))

                df["timestamp"]=pd.to_datetime(df["timestamp"])

                if day!="":
                    df=df[df["timestamp"].dt.day==int(day)]

                dfs.append(df)

    if dfs:

        result=pd.concat(dfs)

        st.dataframe(result.tail(100))

    else:

        st.write("No records found.")
