"use strict";

var T = require("timbre");

function Voice (filename) {
  this.awoken = false;
  this.sample = T("audio", {}).loadthis(filename);
}

Voice.prototype.awake = function() {
  this.awoken = true;

  this.sample.clone().play().on("ended", function() {
    this.pause();
  });

};

Voice.prototype.sleep = function() {
  this.awoken = false; 
};

module.exports = Voice;
