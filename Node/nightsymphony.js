var Voice = require("./voice");
var voices = [


    // new Voice("samples/bells/bells.plastic.ff.C5B5001.wav"),
    // new Voice("samples/bells/bells.plastic.ff.C5B5003.wav"),
    // new Voice("samples/bells/bells.plastic.ff.C5B5005.wav"),
    // new Voice("samples/bells/bells.plastic.ff.C5B5006.wav"),
    // new Voice("samples/bells/bells.plastic.ff.C5B5008.wav"),
    // new Voice("samples/bells/bells.plastic.ff.C5B5010.wav"),
    // new Voice("samples/bells/bells.plastic.ff.C5B5012.wav"),
    // new Voice("samples/bells/bells.plastic.ff.C6B6001.wav"),
	
	new Voice("samples/insects/cicada_1.wav"),
	new Voice("samples/insects/moth.wav"),
	new Voice("samples/insects/dragonfly_1.wav"),
	new Voice("samples/insects/cricket_1.wav"),
	new Voice("samples/insects/cricket_2.wav"),
	new Voice("samples/insects/dragonfly_2.wav"),
	//new Voice("samples/insects/cicada_1.wav"),
	//new Voice("samples/insects/cicada_1.wav"),	
];



var firmata = require('firmata');

var board = new firmata.Board('/dev/cu.usbmodemfd1241',
	{skipCapabilities: true},
	function(){

		console.log("SUP");

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


/*

var ArduinoFirmata = require('arduino-firmata');
var arduino = new ArduinoFirmata().connect();

arduino.on('connect', function(){
  console.log("connect!! "+arduino.serialport_name);
  console.log("board version: "+arduino.boardVersion);

  arduino.sysex(0x01, [13, 5, 2]); 

});

arduino.on('sysex', function(e){

  console.log("command : " + e.command);
  console.log("data    : " + JSON.stringify(e.data));

	switch (e.command) {
		case 0xb0:

			var id = e.data[0];
			var pin = e.data[2];
			var status = e.data[4];

			console.log(e);
			
			voice = voices[id];

			if (status) {
				voice.awake();
			} else {
				voice.sleep();
			}

		break;
	}


});
*/
