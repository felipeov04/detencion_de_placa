import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# Muestra la versión de Python junto con detalles adicionales
st.write("Versión de Python:", platform.python_version())

values = 0.0
act1="OFF"

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

        


broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("Ustayalejandro")
client1.on_message = on_message



st.title("MQTT Control")

if st.button('Abrir'):
    act1="CKN 364"
    client1= paho.Client("Ustayalejandro")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Gesto":act1})
    ret= client1.publish("Usta", message)
 
    #client1.subscribe("Sensores")
    
    
else:
    st.write('')

if st.button('Cerrar'):
    act1="MXL 931"
    client1= paho.Client("Ustayalejandro")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Gesto":act1})
    ret= client1.publish("Usta", message)
  
    
else:
    st.write('')

