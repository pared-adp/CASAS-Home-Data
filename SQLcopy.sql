\COPY motion FROM 'C:\motionSensors.csv' DELIMITER ',' CSV HEADER;

\COPY battPerc FROM 'C:\battPer.csv' DELIMITER ',' CSV HEADER;

\COPY battVolt FROM 'C:\battVolt.csv' DELIMITER ',' CSV HEADER;

\COPY door FROM 'C:\doorSensor.csv' DELIMITER ',' CSV HEADER;

\COPY fan FROM 'C:\fan.csv' DELIMITER ',' CSV HEADER;

\COPY item FROM 'C:\itemSensor.csv' DELIMITER ',' CSV HEADER;

\COPY light FROM 'C:\lightSensors.csv' DELIMITER ',' CSV HEADER;

\COPY LL FROM 'C:\LL.csv' DELIMITER ',' CSV HEADER;

\COPY L FROM 'C:\L.csv' DELIMITER ',' CSV HEADER;

\COPY temp FROM 'C:\tempSensor.csv' DELIMITER ',' CSV HEADER;

\COPY system FROM 'C:\system.csv' DELIMITER ',' CSV HEADER;

\COPY SS FROM 'C:\SS.csv' DELIMITER ',' CSV HEADER;