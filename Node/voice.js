"use strict";

var T = require("timbre");

function Voice (filename) {
  //this.readPort = readPort;
  this.awoken = false;
  this.singing = false;
  this.sample = T("audio").loadthis(filename, function() {
    //this.set({bang: false}).play();
  });
 }

Voice.prototype.awake = function() {
  this.awoken = true;
  console.log("WAKE" + this.readPort);

  var voice = this;

  if (!this.singing) {
    this.singing = true;
      this.sample.clone().play().on("ended", function() {
        voice.singing = false;
        this.pause();
      });
  }

};

Voice.prototype.sleep = function() {
  this.awoken = false; 
  console.log("SLEEP");
};

module.exports = Voice;