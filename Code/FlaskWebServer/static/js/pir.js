//#################################################
//# Avisha Kumar (ak754) & Tyler Sherman (tss86)  #
//# ECE 5725: Embedded OS                         #
//# 04/23/2020                                    #
//# Lab 5: Final Project                          #
//#################################################
$(document).ready(function(){
    var output = document.getElementById("pirStatus");
    output.innerHTML = "";
    
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/pir');
    //receive details from server
    socket.on('pirStatus', function(msg) {
        //console.log("PIR status = " + msg.pir);
        //$('#pirStatus').html(msg.pir);
        if(msg.pir == "Detected") {
            var sentence = "<h3 class='w3-xlarge w3-text-red'><b>WARNING - The PIR sensor has detected motion!</b></h3>"
            var img = "<img src=../static/img/Intruder.png class='pirImage'>"
            output.innerHTML = sentence + img;
        } else {
            var sentence = "<p>No motion has been detected.</p>"
            var img = "<img src=../static/img/AllClear.jpg class='pirImage'>"
            output.innerHTML = sentence + img;
        }
    });
});
