import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle,os
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

def parseInning(inInning):
    topBottom = inInning[0:1]
    inning = inInning[1:]
    if inning == '9+':
        inning = '10'
    return (int(topBottom),int(inning))

def trainModel():
    pickleItems = loadall('pitch.pk1')
    pitches = []
    for item in pickleItems:
        for p in item:
            pitches.append(p)
    for p in pitches:
        # print(p)
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
        # mnist = tf.keras.datasets.mnist
    dataset = pd.DataFrame(train,columns=columns)

    train_dataset = dataset.sample(frac=0.8,random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    train_stats = train_dataset.describe()
    train_stats.pop("WinningTeam")
    train_stats = train_stats.transpose()
    print(train_stats)


    def norm(x):
        return (x - train_stats['mean']) / train_stats['std']

    normed_train_data = norm(train_dataset)[:10000]
    normed_test_data = norm(test_dataset)[:10000]
    
    train_labels = normed_train_data.pop('WinningTeam')
    test_labels = normed_test_data.pop('WinningTeam')   

    model = keras.Sequential([
        layers.Dense(64, activation=tf.nn.relu, input_shape=[len(normed_train_data.keys())]),
        layers.Dense(64, activation=tf.nn.relu),
        layers.Dense(1)
    ])

    optimizer = tf.train.RMSPropOptimizer(0.001)

    model.compile(loss='mse',
                    optimizer=optimizer,
                    metrics=['mae', 'mse'])

      
    # early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=50)
    # Create checkpoint callback
    cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path, 
                                                 save_weights_only=True,
                                                 verbose=1)

    model.fit(normed_train_data, train_labels, epochs=5,
                    validation_data = (normed_test_data,test_labels),
                    callbacks=[cp_callback])

    loss, mae, mse = model.evaluate(normed_test_data, test_labels, verbose=0)

    print('Loss: {} MAE: {} MSE: {}'.format(loss,mae,mse))
    

if __name__ == '__main__':
    trainModel()