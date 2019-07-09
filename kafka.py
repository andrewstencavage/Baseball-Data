import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle,os
import mysql.connector

train = []
columns = ['TopBottom','Innings','Outs','Balls','Strikes','ScoreDiff','First','Second','Third','WinningTeam']

def loadall(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

def getPitches():
    pickleItems = loadall('pitch.pk1')
    pitches = []
    for item in pickleItems:
        for p in item:
            pitches.append(p)
    for p in pitches:
        topBottom,inning = parseInning(p.inning)
        #(self.ball,self.strike,self.out,self.inning,self.scoreDiff,self.first,self.second,self.third,self.winningTeam)
        train.append([
            topBottom,
            inning,
            int(p.out),
            int(p.ball),
            int(p.strike),
            int(p.scoreDiff),
            int(p.first),
            int(p.second),
            int(p.third),
            int(p.winningTeam)
        ])
    return train

def getCursor():
    mydb = mysql.connector.connect(
        host='10.0.1.5',
        user='nGrok',
        passwd='PythonSucks123!',
        database='baseball'
    )
    pitches = getPitches()
    # mydb = mysql.connector.connect(
    #     host='localhost',
    #     user='svcNode',
    #     passwd='PythonSucks123!',
    #     database='baseball'
    # )
    cursor = mydb.cursor()
    sql = "INSERT INTO pitch (topBottom,inning,numOut,ball,strike,scoreDiff,firstBase,secondBase,thirdBase,winningTeam) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    for p in pitches:
        val = p
        cursor.execute(sql,val)
    mydb.commit()

def parseInning(inInning):
    topBottom = inInning[0:1]
    inning = inInning[1:]
    if inning == '9+':
        inning = '10'
    return (int(topBottom),int(inning))
    
if __name__ == '__main__':
    getCursor()
    # getPitches()