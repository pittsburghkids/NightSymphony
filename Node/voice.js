"use strict";

var play = require('play');

function Voice (filename) {
  this.awoken = false;
  this.sample = filename;
}

Voice.prototype.awake = function() {
  this.awoken = true;
  play.sound(this.sample, function(){});
};

Voice.prototype.sleep = function() {
  this.awoken = false; 
};

module.exports = Voice;