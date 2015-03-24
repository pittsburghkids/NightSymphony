var Voice = require("./voice");

var boards = [
  '/dev/cu.usbmodemfd121',
  '/dev/cu.usbmodemfa131'
]


var voices = [];

voices[0] = [
  new Voice("samples/insects/cicada_1.wav"), 
  new Voice("samples/insects/dragonfly_1.wav"),
  new Voice("samples/insects/cricket_1.wav"),
  new Voice("samples/insects/cricket_2.wav"),
  new Voice("samples/insects/dragonfly_2.wav"),
  new Voice("samples/insects/cicada_2.wav"),  
];

voices[1] = [
  new Voice("samples/bells/bells.plastic.ff.C5B5001.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5003.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5005.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5006.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5008.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5010.wav"),
];



var firmata = require('firmata');

for (var i = 0; i < boards.length; i++) {
  var board = new firmata.Board(boards[i],
    {skipCapabilities: true},
    function() {
      console.log("Board connected!");
    }
  );  
}

firmata.SYSEX_RESPONSE[0xb0] = function(board) {

  console.log(board.currentBuffer);

  var address = board.currentBuffer[2];
  var id = board.currentBuffer[4];
  var pin = board.currentBuffer[6];
  var status = board.currentBuffer[8];

  voiceBank = voices[address];
  if (!voiceBank) return;

  voice = voiceBank[id];
  if (!voice) return;

  if (status) {
    console.log("AWAKE");
    voice.awake();
  } else {
    console.log("ASLEEP");
    voice.sleep();
  }

}