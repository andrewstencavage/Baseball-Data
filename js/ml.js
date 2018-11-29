let model;

let inputs;

let xs;

const train_xs = tf.tensor2d([
  [0, 0],
  [1, 0],
  [0, 1],
  [1, 1]
]);
const train_ys = tf.tensor2d([
  [0],
  [1],
  [1],
  [0]
]);

function setup(jsonData) {
  let inputs = fillInput(jsonData);
  // Create the input data
  inputs = [
    [1,1],
    [0,1],
    [0,0]
  ];
//   for (let i = 0; i < cols; i++) {
//     for (let j = 0; j < rows; j++) {
//       let x1 = i / cols;
//       let x2 = j / rows;
//       inputs.push([x1, x2]);
//     }
//   }
  xs = tf.tensor2d(inputs);


  model = tf.sequential();
  let hidden = tf.layers.dense({
    inputShape: [2],
    units: 16,
    activation: 'sigmoid'
  });
  let output = tf.layers.dense({
    units: 1,
    activation: 'sigmoid'
  });
  model.add(hidden);
  model.add(output);

  const optimizer = tf.train.adam(0.2);
  model.compile({
    optimizer: optimizer,
    loss: 'meanSquaredError'
  })

  setTimeout(train, 10);
  test();
}

function parseInning(jInning) {
  let topBottom = jInning.substring(0,1);
  let inning = jInning.substring(1);
  if (inning == '9+') {
    inning = 10;
  }
  return {
    topBottom,
    inning
  }
}
function fillInput(jsonData) {

  let inps = [];
  console.table(jsonData)
//pitchDict[pitch.inning][pitch.scoreDiff][pitch.out][pitch.ball][pitch.strike][int(pitch.first)][int(pitch.second)][int(pitch.third)][int(winner)] += 1
  // for (let inning in jsonData) {
  //   let jInning = jsonData[inning];
  //   for (let scoreDiff in jInning) {
  //     let jScoreDiff = jInning[scoreDiff];
  //     for (let outs in jScoreDiff ) {
  //       let jOuts = jScoreDiff[outs];
  //       for (let balls in jOuts) {
  //         let jBalls = jOuts[balls];
  //         for (let strikes in jBalls) {
  //           let jStrikes = jBalls[strikes];
  //           for (let first in jStrikes) {
  //             let jfirst = jStrikes[first];
  //             for (let second in jfirst) {
  //               let jsecond = jfirst[second];
  //               for (let third in jsecond) {
  //                 let jthird = jsecond[third];
  //                 for (let winner in jthird) {
  //                   let res = jthird[winner];
  //                   //let res = jsonData[inning][scoreDiff][outs][balls][strikes][first][second][third][winner];
  //                   let getInning = parseInning(inning);
  //                   // for(let i = 0; i < res;i++){
  //                   //   inps.push([getInning.inning,getInning.topBottom,scoreDiff,outs,balls,strikes,first,second,third,winner]);
  //                   // }
                    
  //                 }
  //               }
  //             }
  //           }
  //         }
  //       }
  //     }
  //   }
    
  }
  console.log(inps)
}

function train() {
  trainModel().then(result => {
    ///console.log(result.history.loss[0]);
    //setTimeout(train, 10);
  });
}

function trainModel() {
  return model.fit(train_xs, train_ys, {
    shuffle: true,
    epochs: 1
  });
}

function test() {
  tf.tidy(() => {
    // Get the predictions
    let ys = model.predict(xs);
    let y_values = ys.dataSync();
    console.table(y_values);
  });

}