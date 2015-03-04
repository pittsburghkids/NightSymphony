var Voice = require("./voice");
var voices = [


    new Voice("samples/bells/bells.plastic.ff.C5B5001.wav"),
    new Voice("samples/bells/bells.plastic.ff.C5B5003.wav"),
    new Voice("samples/bells/bells.plastic.ff.C5B5005.wav"),
    new Voice("samples/bells/bells.plastic.ff.C5B5006.wav"),
    new Voice("samples/bells/bells.plastic.ff.C5B5008.wav"),
    new Voice("samples/bells/bells.plastic.ff.C5B5010.wav"),
    new Voice("samples/bells/bells.plastic.ff.C5B5012.wav"),
    new Voice("samples/bells/bells.plastic.ff.C6B6001.wav"),
	
	new Voice("samples/insects/cicada_1.wav"),
	new Voice("samples/insects/cicada_1.wav"),
	new Voice("samples/insects/cicada_1.wav"),
	new Voice("samples/insects/cicada_1.wav"),
	new Voice("samples/insects/cicada_1.wav"),
	new Voice("samples/insects/cicada_1.wav"),
	new Voice("samples/insects/cicada_1.wav"),
	new Voice("samples/insects/cicada_1.wav"),	
];

var ArduinoFirmata = require('arduino-firmata');
var arduino = new ArduinoFirmata().connect();

arduino.on('connect', function(){
  console.log("connect!! "+arduino.serialport_name);
  console.log("board version: "+arduino.boardVersion);

});

arduino.on('sysex', function(e){

	switch (e.command) {
		case 0xa0:

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
