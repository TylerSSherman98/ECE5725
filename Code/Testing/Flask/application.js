$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/pir');

    //receive details from server
    socket.on('motion', function(msg) {
        console.log("Received number" + msg.pir);
        $('#log').html(msg.pir);
    });

});