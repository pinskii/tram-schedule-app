import requests
import datetime
import time
import json
import tkinter as tk

url = "https://api.digitransit.fi/routing/v1/routers/waltti/index/graphql"
headers = {
    "Content-type": "application/graphql",
    "digitransit-subscription-key": ""
}
"""Etelä-Hervanta: 0837, Kauppi: 0907, Hervannan kampus: 0835"""
data = '''{
    stop1: stop(id: "tampere:0837"){
        name
        stoptimesWithoutPatterns {
            scheduledArrival
            realtimeArrival
            arrivalDelay
            scheduledDeparture
            realtimeDeparture
            departureDelay
            realtime
            realtimeState
            headsign
            }
        }
    stop2: stop(id: "tampere:0835"){
        name
        stoptimesWithoutPatterns {
            scheduledArrival
            realtimeArrival
            arrivalDelay
            scheduledDeparture
            realtimeDeparture
            departureDelay
            realtime
            realtimeState
            headsign
            }
        }
        stop3: stop(id: "tampere:0907"){
        name
        stoptimesWithoutPatterns {
            scheduledArrival
            realtimeArrival
            arrivalDelay
            scheduledDeparture
            realtimeDeparture
            departureDelay
            realtime
            realtimeState
            headsign
            }
        }
    }
'''

def update_clock():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    clockLabel.configure(text=time, fg="white", bg="black")
    window.after(1000, update_clock)

def update_data():
    try:
        # Request data from API
        response = requests.post(url, headers=headers, data=data)
        responseData = response.json()

        stopData = responseData['data']

        # Closes possibly open windows
        for widget in frame.winfo_children():
            widget.destroy()

        # Get the data per requested stop
        for stop in stopData.values():
            # Get and print the stop name
            stopName = stop['name']
            title = tk.Label(frame, text="\nNext 5 arrivals for " + stopName + ":", font="bold", fg="white", bg="black")
            title.pack(side=tk.TOP, pady=10)
            
            # Get the stop times
            stopTimes = stop['stoptimesWithoutPatterns'][:5]
            for stopTime in stopTimes:
                if stopTime['realtime']:
                    nextArrival = datetime.datetime.utcfromtimestamp(stopTime['realtimeArrival']).strftime('%H:%M:%S')
                    realTime = False
                    if stopTime['arrivalDelay'] > 0:
                        realTimeDelayed = True
                        arrivalDelay = datetime.datetime.utcfromtimestamp(stopTime['arrivalDelay']).strftime('%S')
                        arrivalInfo = f" myöhässä {arrivalDelay} s"
                    else:
                        realTime = True
                        arrivalInfo = ""
                else:
                    nextArrival = datetime.datetime.utcfromtimestamp(stopTime['scheduledArrival']).strftime('%H:%M:%S')
                    realTime = False
                    realTimeDelayed = False 
                    arrivalInfo = ""
                             
                rowFrame = tk.Frame(frame)
                rowFrame.configure(bg="black")
                rowFrame.pack(side=tk.TOP, anchor='w', padx=(20, 0))
                
                if realTime:
                    arrivalLabelBold = tk.Label(rowFrame, text=nextArrival, font=("Arial", 11, "bold"), fg="#5ced73", bg="black")
                elif realTimeDelayed:
                    arrivalLabelBold = tk.Label(rowFrame, text=nextArrival, font=("Arial", 11, "bold"), fg="red", bg="black")
                else:
                    arrivalLabelBold = tk.Label(rowFrame, text=nextArrival, font=("Arial", 11, "bold"), fg="white", bg="black")
                arrivalLabelBold.pack(side=tk.LEFT)
                
                arrivalLabel = tk.Label(rowFrame, text=arrivalInfo, font=("Arial", 9), fg="red", bg="black")
                arrivalLabel.pack(side=tk.RIGHT)

    except Exception as e:
        print(f"An error occurred while requesting data: {e}")

    window.after(15000, update_data)

window = tk.Tk()
window.title("Tram Arrival Times")
window.configure(bg="black")

clockFrame = tk.Frame(window)
clockFrame.configure(bg="black")
clockFrame.pack(side=tk.TOP)

clockLabel = tk.Label(clockFrame, font=("Arial", 18))
clockLabel.pack(side=tk.TOP, pady=20)
update_clock()

frame = tk.Frame(window)
frame.configure(bg="black")
frame.pack(padx=10, pady=10)

update_data()
window.mainloop()
