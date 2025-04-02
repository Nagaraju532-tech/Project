import time
import tkinter
from tkinter import *
import math
import random
from threading import Thread 
import time 
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import json
from web3 import Web3, HTTPProvider
import hashlib
import timeit

dct = defaultdict(list)
global canvas, text, details
details=''
transaction_time = []
global simulation_status
global nodes, node_x, node_y
global fn1, fn2, fn3, labels, line1, line2, line3
global option
option = 0
global bac1, bac2, bac3, bac4

def readDetails(contract_type):
    global details
    details = ""
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'BlockAccessWLAN.json' #WLAN Block Access contract code
    deployed_contract_address = '0x129CA343157c29E611a4C1118394bC5a3fce95d6' #hash address to access WLAN contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'minetransaction':
        details = contract.functions.getTransaction().call()
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'BlockAccessWLAN.json' #WLAN Block Access contract file
    deployed_contract_address = '0x129CA343157c29E611a4C1118394bC5a3fce95d6' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'minetransaction':
        details+=currentData
        msg = contract.functions.setTransaction(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    
    	
def calculateDistance(iot_x,iot_y,x1,y1):
    flag = False
    for i in range(len(iot_x)):
        dist = math.sqrt((iot_x[i] - x1)**2 + (iot_y[i] - y1)**2)
        if dist < 60:
            flag = True
            break
    return flag     

def startWLANDataGenerate(text,canvas):
    class WLANThread(Thread):
        global transaction_time, simulation_status
        global option
        global line1,line2,line3, fn1, fn2, fn3, nodes, node_x, node_y, labels
        global bac1, bac2, bac3, bac4
        bac1 = []
        bac2 = []
        bac3 = []
        bac4 = []
        def __init__(self,text,canvas): 
            Thread.__init__(self)
            self.canvas = canvas
            self.text = text
             
        def run(self):
            print(simulation_status)
            option = 0
            while(simulation_status):
                src = random.randint(1, 19)
                if src != fn1 and src != fn2 and src != fn3:
                    src_x = node_x[src]
                    src_y = node_y[src]
                    distance = 10000
                    hop = 0
                    selected_fn = 0
                    for i in range(1,20):
                        temp_x = node_x[i]
                        temp_y = node_y[i]
                        if i != src and i != fn1 and i != fn2 and i != fn3 and temp_x < src_x:
                            dist = math.sqrt((src_x - temp_x)**2 + (src_y - temp_y)**2)
                            if dist < distance:
                                distance = dist
                                hop = i
                    if hop != 0:
                        hop_x = node_x[hop]
                        hop_y = node_y[hop]
                        fn1_transfer = math.sqrt((hop_x - node_x[fn1])**2 + (hop_y - node_y[fn1])**2)
                        fn2_transfer = math.sqrt((hop_x - node_x[fn2])**2 + (hop_y - node_y[fn2])**2)
                        fn3_transfer = math.sqrt((hop_x - node_x[fn3])**2 + (hop_y - node_y[fn3])**2)
                        bac1.append((fn1_transfer + fn2_transfer + fn3_transfer) * 0.2)
                        bac4.append(fn1_transfer * 0.2)
                        bac2.append(fn2_transfer * 0.2)
                        bac3.append(fn3_transfer * 0.2)
                        if fn1_transfer <= fn2_transfer and fn1_transfer <= fn3_transfer:
                            selected_fn = fn1                            
                        elif fn2_transfer <= fn1_transfer and fn2_transfer <= fn3_transfer:
                            selected_fn = fn2                            
                        else:
                            selected_fn = fn3                            
                    if selected_fn != 0 and hop != 0:
                        text.insert(END,"Selected Full Node is : "+str(selected_fn)+"\n")
                        line1 = canvas.create_line(node_x[src]+20, node_y[src]+20,node_x[hop]+20, node_y[hop]+20,fill='black',width=3)
                        line2 = canvas.create_line(node_x[hop]+20, node_y[hop]+20,node_x[selected_fn]+20, node_y[selected_fn]+20,fill='black',width=3)
                        line3 = canvas.create_line(node_x[selected_fn]+20, node_y[selected_fn]+20,node_x[0]+20, node_y[0]+20,fill='black',width=3)
                        current_time = time.strftime("%Y/%m/%d-%H:%M:%S")
                        sense = random.randint(5, 45)
                        dct[src].append(str(sense)+","+str(current_time))
                        sense_data = str(src)+" "+str(sense)
                        h = hashlib.sha512(sense_data.encode())
                        hashcodes = h.hexdigest()
                        data = str(src)+"#"+str(sense)+"#"+str(current_time)+"#"+hashcodes+"\n"
                        start_time = timeit.timeit()
                        saveDataBlockChain(data,"minetransaction")
                        end_time = timeit.timeit()
                        text.insert(END,"Sensor Data : Node "+str(src)+" sense temperature : "+str(sense)+" at time "+str(current_time)+"SHA512 = "+hashcodes+" Blockchain Transaction Time: "+str(end_time - start_time)+"\n")
                        text.update_idletasks()
                        for i in range(0,2):
                            self.canvas.delete(line1)
                            self.canvas.delete(line2)
                            self.canvas.delete(line3)
                            time.sleep(1)
                            line1 = canvas.create_line(node_x[src]+20, node_y[src]+20,node_x[hop]+20, node_y[hop]+20,fill='black',width=3)
                            line2 = canvas.create_line(node_x[hop]+20, node_y[hop]+20,node_x[selected_fn]+20, node_y[selected_fn]+20,fill='black',width=3)
                            line3 = canvas.create_line(node_x[selected_fn]+20, node_y[selected_fn]+20,node_x[0]+20, node_y[0]+20,fill='black',width=3)
                            time.sleep(1)
                        self.canvas.delete(line1)
                        self.canvas.delete(line2)
                        self.canvas.delete(line3)
                        canvas.update()                   
                    
    newthread = WLANThread(text,canvas) 
    newthread.start()
    

def startBlockMining():
    global option
    global line1,line2,line3, fn1, fn2, fn3
    text.delete('1.0', END)
    startWLANDataGenerate(text, canvas)
    

def startSimulation():
    global nodes, node_x, node_y, labels
    global fn1, fn2, fn3
    text.delete('1.0', END)
    distance = 10000
    for i in range(1,20):
        x1 = node_x[i]
        y1 = node_y[i]
        dist = math.sqrt((x1 - 5)**2 + (y1 - 350)**2)
        if dist < distance and y1 > 5 and y1 < 200:
            distance = dist
            fn1 = i
    print(distance)        
    distance = 10000
    for i in range(1,20):
        x1 = node_x[i]
        y1 = node_y[i]
        dist = math.sqrt((x1 - 5)**2 + (y1 - 350)**2)
        if dist < distance and i != fn1 and y1 > 250 and y1 <= 350 :
            distance = dist
            fn2 = i
    print(distance)
    distance = 10000
    for i in range(1,20):
        x1 = node_x[i]
        y1 = node_y[i]
        dist = math.sqrt((x1 - 5)**2 + (y1 - 350)**2)
        if dist < distance and i != fn1 and i != fn2 and y1 > 450 and y1 < 650:
            distance = dist
            fn3 = i            
    print(distance)
    text.insert(END,"Selected Full Node 1 is : "+str(fn1)+"\n")
    text.insert(END,"Selected Full Node 2 is : "+str(fn2)+"\n")
    text.insert(END,"Selected Full Node 3 is : "+str(fn3)+"\n")
    canvas.delete(nodes[fn1])
    canvas.delete(nodes[fn2])
    canvas.delete(nodes[fn3])
    canvas.delete(labels[fn1])
    canvas.delete(labels[fn2])
    canvas.delete(labels[fn3])
    name = canvas.create_oval(node_x[fn1],node_y[fn1],node_x[fn1]+40,node_y[fn1]+40, fill="green")
    nodes[fn1] = name
    name = canvas.create_oval(node_x[fn2],node_y[fn2],node_x[fn2]+40,node_y[fn2]+40, fill="green")
    nodes[fn2] = name
    name = canvas.create_oval(node_x[fn3],node_y[fn3],node_x[fn3]+40,node_y[fn3]+40, fill="green")
    nodes[fn3] = name
    lbl = canvas.create_text(node_x[fn1]+20,node_y[fn1]-10,fill="green",font="Times 10 italic bold",text="FN1-"+str(fn1))
    labels[fn1] = lbl
    lbl = canvas.create_text(node_x[fn2]+20,node_y[fn2]-10,fill="green",font="Times 10 italic bold",text="FN2-"+str(fn2))
    labels[fn2] = lbl
    lbl = canvas.create_text(node_x[fn3]+20,node_y[fn3]-10,fill="green",font="Times 10 italic bold",text="FN3-"+str(fn3))
    labels[fn3] = lbl

    canvas.create_oval(50,5,500,245)
    canvas.create_oval(50,240,500,450)
    canvas.create_oval(50,430,500,670)
    
    canvas.update()
    startBlockMining()

def setupNetwork():
    global canvas, text
    global simulation_status
    global nodes, node_x, node_y, labels
    nodes = []
    node_x = []
    node_y = []
    labels = []
    simulation_status = True
    canvas.update()
    x = 5
    y = 350
    node_x.append(x)
    node_y.append(y)
    name = canvas.create_oval(x,y,x+40,y+40, fill="red")
    lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 7 italic bold",text="AP")
    labels.append(lbl)
    nodes.append(name)
    for i in range(1,20):
        run = True
        while run == True:
            x = random.randint(100, 450)
            y = random.randint(50, 600)
            flag = calculateDistance(node_x,node_y,x,y)
            if flag == False:
                node_x.append(x)
                node_y.append(y)
                run = False
                name = canvas.create_oval(x,y,x+40,y+40, fill="blue")
                lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 10 italic bold",text="LN "+str(i))
                labels.append(lbl)
                nodes.append(name)
    

def stopSimulation():
    global simulation_status
    simulation_status = False

def throughputGraph():
    global bac1, bac2, bac3, bac4
    plt.figure(figsize=(10,6))
    plt.grid(True)
    plt.xlabel('Number of Transaction')
    plt.ylabel('Throughput')
    plt.plot(bac1)
    plt.plot(bac2)
    plt.plot(bac3)
    plt.plot(bac4)
    plt.legend(['BAC-1','BAC-2','BAC-3','BAC-4'], loc='upper left')
    plt.title('Throughput Graph on Different Block Access')
    plt.show()

def Main():
    global canvas, text
    root = tkinter.Tk()
    root.geometry("1300x1200")
    root.title("Block Access Control in Wireless Blockchain Network: Design, Modeling and Analysis")
    root.resizable(True,True)
    canvas = Canvas(root, width = 800, height = 700)
    canvas.pack()

    text=Text(root,height=30,width=60)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=750,y=210)
    font1 = ('times', 12, 'bold')

    graphButton = Button(root, text="Setup WLAN Network", command=setupNetwork)
    graphButton.place(x=800,y=10)
    graphButton.config(font=font1)
    
    graphButton = Button(root, text="Start Block Access WLAN Simulation", command=startSimulation)
    graphButton.place(x=800,y=60)
    graphButton.config(font=font1)

    responseButton = Button(root, text="Transaction Throughput Graph", command=throughputGraph)
    responseButton.place(x=800,y=110)
    responseButton.config(font=font1)

    stopButton = Button(root, text="Stop simulation", command=stopSimulation)
    stopButton.place(x=800,y=160)
    stopButton.config(font=font1)

    root.mainloop()
   
 
if __name__== '__main__' :
    Main ()
    
