import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import time

test_df = pd.read_csv('test.csv')

with open('linear_regression_model.pkl', 'rb') as file:
    model = pickle.load(file)

st.title("Turbine Power Consumption Simulation")

test_size = st.slider("Select % of test data to showcase:", 10, 100, 10) / 100.0

num_samples = int(len(test_df) * test_size)
test_df_sampled = test_df.iloc[:num_samples]

voltage_placeholder = st.empty()
predict_placeholder = st.empty()
run_turbine_placeholder = st.empty()

def plot_voltage_over_time(data):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['time'], data['input_voltage'], color='blue', label='Input Voltage')
    ax.set_xlabel('Time [sec]')
    ax.set_ylabel('Input Voltage [V]')
    ax.set_title('Input Voltage over Time')
    ax.legend()
    ax.grid(True)
    return fig

def plot_power_over_time(data, y_test, y_pred, title='Actual vs. Predicted Electrical Power over Time'):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['time'], y_test, color='green', label='Actual Electrical Power')
    ax.plot(data['time'], y_pred, color='red', linestyle='--', label='Predicted Electrical Power')
    ax.set_xlabel('Time [sec]')
    ax.set_ylabel('Electrical Power [W]')
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    return fig

voltage_placeholder.pyplot(plot_voltage_over_time(test_df_sampled))

if st.button('Predict'):
    X_test = test_df_sampled[['input_voltage']]
    y_test = test_df_sampled['el_power']
    y_pred = model.predict(X_test)

    predict_placeholder.pyplot(plot_power_over_time(test_df_sampled, y_test, y_pred))

if st.button('Simulate Turbine'):
    for i in range(1, 11):
        st.write(f"Displaying {i*10}% of the data")

        num_samples = int(len(test_df) * (i*10) / 100.0)
        test_df_sampled = test_df.iloc[:num_samples]

        X_test = test_df_sampled[['input_voltage']]
        y_test = test_df_sampled['el_power']
        y_pred = model.predict(X_test)

        voltage_placeholder.pyplot(plot_voltage_over_time(test_df_sampled))
        run_turbine_placeholder.pyplot(plot_power_over_time(test_df_sampled, y_test, y_pred, title=f'Run Turbine: {i*10}% Data'))

        # Simulate behavior of turbine running
        time.sleep(0.4)
