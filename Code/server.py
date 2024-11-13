from statistics import mean
from flask import Flask, render_template
from numpy import std


def get_data(temp_source):   #Returns the data collected from the sensors
    data = []
    stats = []
    with open("./sensor_data.txt", 'r') as data_file:
        for line in data_file:    
            values = line.split(" ")
            values.pop(5)
            for i in range(len(values)):
                    values[i] = round(float(values[i]), 1)
            
            data.append(values)

        if temp_source==1:
            data.pop(4)
        else:
            temp02 = data.pop(4)
            data[0] = temp02

        for values in data:    
            stats.append([round(mean(values), 1), round(std(values), 1)])

    return data, stats

def get_last_visit():   #Returns the measured values in the last visit
    data = []
    last = []
    with open("./last_visit.txt", "r") as file:
        for line in file:
            last = line.split()
            for i in range(len(last)):
                last[i] = float(last[i])
            data.append(line)
    return last

def update_last_visit(values):     #Updates the file containing the files measured in the last visit
    with open("./last_visit.txt", 'w') as file:
        file.write(" ".join(values))

def get_difference(new_data, last_visit_data):     #Returns the precentage increase between the last visit and now for all sensors
    dif = []
    for i in range(len(last_visit_data)):
        new_val = float(new_data[i][0])
        last_val = float(last_visit_data[i])
        dif.append(round((new_val/last_val)*100-100, 1))
    
    for i in range(len(dif)):
        if dif[i] >= 0:
            dif[i] = f"+{dif[i]}%"
        else:
            dif[i] = f"-{abs(dif[i])}%"
    return dif

def get_alarms():
    alarms = []
    with open("./alarms.txt", "r") as file:
        for line in file:
            alarms = line.split(" ")
    
    for i in range(len(alarms)):
        alarms[i] = float(alarms[i])

    return alarms

def get_temp_source():
    with open("./temp_source.txt", 'r') as file:
        return file.read()

app = Flask(__name__)

@app.route("/")
def home():
    temp_source = get_temp_source()
    data, stats = get_data(int(temp_source))
    last_visit = get_last_visit()
    update_last_visit([str(data[0][0]), str(data[1][0]), str(data[2][0]), str(data[3][0])])
    dif = get_difference(data, last_visit)
    for i in range(len(dif)):
        data[i].append(dif[i])

    return render_template("index.html", content = data, temp=data[0][:-1], sound=data[1][:-1], lux=data[2][:-1], press=data[3][:-1], stats = stats)

@app.route("/alarms.html")
def alarms():
    temp_source = get_temp_source()
    data = get_data(temp_source)[0]
    alarms = get_alarms()
    return render_template("alarms.html", content = data, alarms = alarms)

if __name__ == "__main__":
    app.run()