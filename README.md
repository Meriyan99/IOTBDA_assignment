# Project Group - 2022_11

##### Group Leader - IT19158778 - Lahiru Nuwan S. (lahiru-98)
##### Member 2 - IT19080840 - Kovishwakarunya K. (Karunyak1998)
##### Member 3 - IT19175058 - Mariyam M.S.S  (Mariyam73)
##### Member 4 - IT19101316 - Alahakoon D.N  (DewniNimaya)

# PROJECT DESCRIPTION

As at present, there exist various equipment that helps us regulate the environment temperature to provide human comfort, from the extreme temperature variations. On such context, air conditioners and fans are the most commonly used equipment. Considering the maintenance and cost of these equipment most places make use of fans rather than air conditioners to regulate the environment temperature.

In most cases, people handle the speed of the fan depending on the environmental temperature condition. For example, during extreme hot conditions there is a necessity for the fan speed to be high, and during mild cold conditions there would be a necessity for the fan speed to be low. But performing this manually could be a tedious task and the ability to get this done automatically would be highly beneficial.

Our project aims at identifying the temperature of the environment in degree Celsius through a temperature sensor having a room as the experimental environment. Through the temperature detected, we aim to indicate qualitative information regarding the environment,  through a moving actuator in a gauge controlled by a stepper motor as to whether the environment condition is ‘cool’, ‘warm’ or ‘hot’.

While indicating the temperature, this system aims to visualize the variation of the environment temperature sensed through sensors, via a dashboard. In addition to showing the real time temperature readings, an ARIMA model will be trained for this system which ensures to provide visualization on the predictions regarding the temperature the upcoming time period of twelve months as well.

While this indicator system is developed precisely incorporating the Internet of things concept, as a future work we also aim to regulate the fan speed depending on the temperature indication identified.


# SOLUTION ARCHITECTURE AND DESCRIPTION

![ArchitectureUpdated](https://user-images.githubusercontent.com/68418911/163150164-e7966ebd-bfc4-47f1-8c90-1784d31ce36d.png)

Initially the hardware layer is built comprising of the Raspberry pi device, temperature sensor (DHT11) and a stepper motor which can handle the moving actuator of a gauge. Once the hardware layer is built, configurations are done to connect it with the network layer comprising of the MQTT broker. Here once the MQTT broker is setup, the data collected through the sensor can be published to the broker. Node red dashboard which helps in visualizing the data subscribes to the MQTT broker to receive data whenever published. In addition to these configurations, an ARIMA model which is a time series model will be trained and deployed to provide future predictions of temperature change to be visualized by the Node red dashboard. 

