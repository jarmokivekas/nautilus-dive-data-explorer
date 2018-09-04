// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
'use strict';
var request = require('request');

var fs = require('fs');
var path = process.cwd();
var buffer = fs.readFileSync(path + "../data/2018-06-22T18-31-08.json");
console.log(buffer.toString())
