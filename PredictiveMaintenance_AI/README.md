## **Smart Factory Predictive Maintenance System**

## **Overview**



This project is an AI-powered Predictive Maintenance System designed to monitor industrial machines and predict potential failures before they occur. The system simulates a Digital Twin Dashboard for a smart factory environment, allowing operators to monitor machine health in real time and make proactive maintenance decisions.



The goal of this project is to reduce unexpected machine downtime, increase operational efficiency, and enable data-driven maintenance strategies.



### **Key Features**



1. Live Machine Monitoring
   
2. Displays real-time sensor data for individual machines including:
   
3. Air Temperature
   
4. Process Temperature
   
5. Rotational Speed
   
6. Torque
   
7. Tool Wear



The system analyzes these parameters using an AI model to calculate failure probability.



##### **Factory Overview Dashboard**



Provides a high-level overview of multiple machines within the factory.



Each machine is displayed with:



Current failure risk percentage



Health status indicator



🟢 Healthy



🟡 Warning



🔴 Critical



This allows factory operators to quickly identify machines that require attention.



##### **Machine Health Timeline**



A trend visualization that shows how machine failure probability changes over time.



This helps in:



* Identifying degradation patterns



* Understanding machine wear behavior



* Planning predictive maintenance schedules



* AI-Based Failure Prediction



The system uses a **Random Forest Machine Learning model** trained on machine sensor data to estimate the probability of machine failure.



The model evaluates multiple parameters simultaneously to determine machine health and predict potential failures.



##### **Technology Stack**

|Component| 	Technology|
|-|-|
|Programming Language|Python|
|Dashboard Framework|Streamlit|
| <br />Machine Learning|Scikit-learn|
|Data Processing|Pandas, NumPy|
| <br />Visualization|Plotly|
| <br />Model Storage|Joblib|

#### 



	

#### **System Architecture**



&nbsp;                                               Industrial Machines

&nbsp;                                                        ↓

&nbsp;                                              IoT Sensors (Simulated)

&nbsp;                                                        ↓

&nbsp;                                               Data Processing Layer

&nbsp;                                                        ↓

&nbsp;                                                AI Prediction Model

&nbsp;                                                        ↓

&nbsp;                                               Digital Twin Dashboard

&nbsp;                                                        ↓

&nbsp;                                                Maintenance Insights





##### **Installation \& Setup**



1\. Clone the Repository

git clone https://github.com/IshaThakar/PredictiveMaintenance_AI



2\. Navigate to the Project Folder

&nbsp;  cd PredictiveMaintenance\_AI



3\. Install Required Libraries

&nbsp;  pip install streamlit pandas scikit-learn numpy plotly streamlit-autorefresh joblib



4\. Run the Application

py -m streamlit run app.py



The dashboard will open automatically in your browser.

#### 

#### **Use Cases**



This system can be applied in industries such as:



* Manufacturing plants



* Automotive production lines



* Industrial machinery monitoring



* Smart factories (Industry 4.0)



It enables predictive maintenance strategies instead of reactive maintenance, reducing downtime and maintenance costs.



##### **Future Improvements**



Possible enhancements for future versions:



* Integration with real IoT sensors



* Cloud-based machine data streaming



* Remaining Useful Life (RUL) prediction



* Automated maintenance scheduling



* Mobile monitoring dashboard



#### **Project Context**



This project was developed as part of a Hackathon prototype to demonstrate how AI and real-time dashboards can be used to build intelligent maintenance systems for modern factories.


