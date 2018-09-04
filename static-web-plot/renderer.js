// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// All of the Node.js APIs are available in this process.
'use strict';

console.log("defining helper functions")

const VALUE = 1
const DTM = 0

var d = {
    hercules: {
        depthseries:[]
    },
    nautilus: {}
}



function onlyUnique(value, index, self) {
    return self.indexOf(value) === index;
}

function findFirstOccurrence(needle, haystack) {
    for (var i = 0; i < haystack.length; i++){
        if (haystack[i] === needle){
            return i
        }
    }
}

function deduplicate(series) {
    console.log("deduplicating series")
    var dedup = []
    for (var i = 0; i < data.length-1; i++) {
        if ((series[i][VALUE] != series[i+1][VALUE]) &&
            (series[i][DTM] != series[i+1][DTM])){
                dedup.push(series[i])
            }
        else{
            i = i+1;
        }
    }
    return dedup
}

// a series in an array of array(2)
function dedup_unsorted_timeseries(series){

    console.log("deduplicating")
    var included_dtm = []
    var dedup = []
    for (var i = 0; i < series.length; i++) {
        if (included_dtm.includes(series[i][DTM]) == false){

            included_dtm.push(series[i][DTM])
            dedup.push([
                series[i][DTM],
                series[i][VALUE]
            ])
        }
    }
    return dedup
}
