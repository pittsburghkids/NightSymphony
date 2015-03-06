var Voice = require("./voice");
var voices = [
  new Voice("samples/insects/cicada_1.wav"),
  new Voice("samples/insects/moth.wav"),
  new Voice("samples/insects/dragonfly_1.wav"),
  new Voice("samples/insects/cricket_1.wav"),
  new Voice("samples/insects/cricket_2.wav"),
  new Voice("samples/insects/dragonfly_2.wav"),
  new Voice("samples/insects/mosquito.wav"),
  new Voice("samples/insects/cicada_2.wav"),  

  new Voice("samples/bells/bells.plastic.ff.C5B5001.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5003.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5005.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5006.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5008.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5010.wav"),
  new Voice("samples/bells/bells.plastic.ff.C5B5012.wav"),
  new Voice("samples/bells/bells.plastic.ff.C6B6001.wav"),
];

var firmata = require('firmata');
var board = new firmata.Board('/dev/cu.usbmodemfd1241',
  {skipCapabilities: true},
  function(){

    console.log("Board connected!");

    firmata.SYSEX_RESPONSE[0xb0] = function(board) {

      console.log(board.currentBuffer);

      var id = board.currentBuffer[2];
      var pin = board.currentBuffer[4];
      var status = board.currentBuffer[6];

      voice = voices[id];

      if (status) {
        voice.awake();
      } else {
        voice.sleep();
      }

    }

  });  