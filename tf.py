import tensorflow as tf
import pickle
x_train = []

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
        print(p)
        topBottom,inning = parseInning(p.inning)
        #(self.ball,self.strike,self.out,self.inning,self.scoreDiff,self.first,self.second,self.third,self.winningTeam)
        x_train.append([
            topBottom,
            inning,
            int(p.out),
            int(p.ball),
            int(p.strike),
            p.scoreDiff,
            p.first,
            p.second,
            p.third,
        ])
# mnist = tf.keras.datasets.mnist

# (x_train, y_train), (x_test, y_test) = mnist.load_data()
# x_train, x_test = x_train / 255.0, x_test / 255.0

# model = tf.keras.models.Sequential([
#   tf.keras.layers.Flatten(),
#   tf.keras.layers.Dense(512, activation=tf.nn.relu),
#   tf.keras.layers.Dropout(0.2),
#   tf.keras.layers.Dense(10, activation=tf.nn.softmax)
# ])

# model.compile(optimizer='adam',
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

# model.fit(x_train, y_train, epochs=5)

# model.evaluate(x_test, y_test)

if __name__ == '__main__':
    trainModel()