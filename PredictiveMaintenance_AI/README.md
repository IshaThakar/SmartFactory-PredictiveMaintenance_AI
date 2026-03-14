## **Smart Factory Digital Twin – AI Predictive Maintenance System**



An AI-powered industrial monitoring system that predicts machine failures, estimates remaining useful life, logs machine health data, and visualizes factory performance in real time.



Built using machine learning, real-time data simulation, and cloud logging to replicate how modern Industry 4.0 smart factories operate.



##### **Project Overview**



This system simulates a Digital Twin of a factory floor, where machines continuously generate sensor data and AI models analyze their health.



The platform:



* Predicts machine failure probability



* Estimates Remaining Useful Life (RUL)



* Detects possible root causes



* Logs operational data for continuous model retraining



* Visualizes factory performance using a real-time dashboard



The dashboard is built with Streamlit and integrates with Firebase Realtime Database for cloud data streaming.



##### **AI Models Used**



1. ###### **Failure Prediction Model**



* **Algorithm:**



   Scikit-learn Random Forest Classifier



* **Input features:**



1.  air\_temperature
2.  process\_temperature
3.  rotational\_speed
4.  torque
5.  tool\_wear



* **Output:**



Probability of machine failure.



###### **2. Remaining Useful Life (RUL) Model**

###### 

* **Algorithm:**



Gradient Boosting Regressor



* **Predicts:**



Estimated remaining operational hours before failure



###### **3. Diagnosis Model**



* **Algorithm:**



Random Forest Classifier



**Identifies possible issues such as:**



1. Tool Wear Failure
2. Mechanical Overload
3. Cooling System Failure
4. Bearing Stress
5. Healthy Operation



##### **Dashboard Features**



The application provides four main monitoring panels.



* ###### **Live Machine Monitoring**



1. Displays real-time machine metrics:
2. Air temperature
3. Process temperature
4. Rotational speed
5. Torque
6. Tool wear


**Also shows:**

* Machine health %
* Failure probability
* Suggested maintenance actions
* Estimated time before failure



* ######  **Factory Overview**



1. Shows health status of all machines simultaneously.



**Each machine displays:**



* Failure risk
* Status indicator



**Status categories:**



1. Health
2. Warning
3. Critical



* ###### **Machine Timeline**



Visualizes machine risk trend over time.



**Data is pulled from Firebase sensor logs and displayed using:**



Plotly interactive graphs



* ###### **Alert History**



Displays historical records of machine performance including:



* Timestamp



* Sensor values



* Failure probability



Users can filter by:



* Year



* Month



* Day



###### **4. Continuous Learning System**



The project implements a feedback loop where the system continuously improves itself.



**Data Logging**



All machine sensor data is stored in:



alert\_logs/

   ├── year

   ├── month

   ├── machine

   └── weekly CSV files



**Automatic Model Retraining**



Every 30 minutes:



* Machine logs are aggregated.



* Failure labels are generated.



* The failure prediction model is retrained.



* This simulates real-world industrial AI pipelines.



###### **5. Cloud Integration**



Sensor data is streamed to:



* Firebase Realtime Database



Firebase stores:



sensor\_data

   ├── Machine\_A

   ├── Machine\_B

   ├── Machine\_C

   └── Machine\_D



**This allows:**



1. real-time monitoring
2. timeline visualization
3. scalable data storage



###### **6.  Data Retention System**



* To prevent storage overflow:



Logs older than 60 days are removed



* Critical failures are archived in



critical\_logs/



This ensures the system remains lightweight and efficient.



###### **7. Tech Stack**



* **Programming Language**



Python



* **Libraries**



1. NumPy
2. Pandas
3. Scikit-learn
4. Plotly
5. Streamlit
6. Cloud
7. Firebase Realtime Database
8. Machine Learning Models
9. Random Forest
10. Gradient Boosting



### **Project Structure**



PredictiveMaintenance\_AI

│

├── app.py

├── train\_model.py

├── machine\_model.pkl

├── rul\_model.pkl

├── diagnosis\_model.pkl

│

├── firebase\_key.json

│

├── alert\_logs/

│

├── critical\_logs/

│

└── README.md



#### **Running the Project**



1\. Install dependencies

pip install streamlit pandas numpy scikit-learn plotly firebase-admin joblib



2\. Run the dashboard

streamlit run app.py



#### 

#### **Future Improvements**



Possible upgrades for this system:



* Integration with IoT sensors



* Deployment on cloud platforms



* Real industrial datasets



* Deep learning models for anomaly detection



* Predictive maintenance scheduling optimization
