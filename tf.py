import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle,os
import mysql.connector

train = []
columns = ['TopBottom','Innings','Outs','Balls','Strikes','ScoreDiff','First','Second','Third','WinningTeam']

checkpoint_path = "checkpoints/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

    # Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

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
        host='localhost',
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

def runTraining(loadModel):
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
    dataset = pd.DataFrame(train,columns=columns)

    train_dataset = dataset.sample(frac=0.8,random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_stats = train_dataset.describe()
    train_stats.pop("WinningTeam")
    train_stats = train_stats.transpose()
    print(train_stats)

    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']

    train_labels = train_dataset.pop('WinningTeam')
    test_labels = test_dataset.pop('WinningTeam')   

    # normed_train_data = norm(train_dataset)
    # normed_test_data = norm(test_dataset)
    normed_train_data = train_dataset
    normed_test_data = test_dataset
    

    

    x_val = normed_train_data[:10000]
    partial_x_train = normed_train_data[10000:]

    y_val = train_labels[:10000]
    partial_y_train = train_labels[10000:]
      
    # The patience parameter is the amount of epochs to check for improvement
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

    model = ''
    if (os.path.exists('./checkpoints/my_model.h5') and loadModel):
        print("LOAD MODEL")
        model = keras.models.load_model('./checkpoints/my_model.h5')
    else:
        print("NEW MODEL")
        model = keras.Sequential([
            layers.Dense(64, activation=tf.nn.relu, input_shape=[len(normed_train_data.keys())]),
            layers.Dense(64, activation=tf.nn.relu),
            layers.Dense(2)
        ])
        model.compile(optimizer='adam',
                        loss='binary_crossentropy',
                        metrics=['acc'])
        history = model.fit(partial_x_train,
                            partial_y_train,
                            # epochs=40,
                            epochs=5,
                            batch_size=512,
                            validation_data=(x_val,y_val),
                            verbose=0,
                            callbacks=[early_stop,PrintDot()])

        model.save('./checkpoints/my_model.h5')

    results = model.evaluate(normed_test_data,test_labels)
    print(results)

    predictions = model.predict(normed_test_data).flatten()

    plt.scatter(test_labels,predictions)
    plt.xlabel('True Values')
    plt.ylabel('Predictions')
    plt.axis('equal')
    plt.axis('square')
    plt.xlim([0,plt.xlim()[1]])
    plt.ylim([0,plt.ylim()[1]])
    _ = plt.plot([-100, 100], [-100, 100])
    plt.show()
    
if __name__ == '__main__':
    getCursor()
    # getPitches()