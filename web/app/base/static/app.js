$(document).ready(function(){
  var socket = io.connect();
  // this is a callback that triggers when the "my response" event is emitted by the server.
  socket.on('connect', function(msg) {
    console.log('Connected to server')
    socket.emit('connected',{"data": "hello"}, broadcast=true)
  })
  socket.on('test', function(msg) {
    console.log('recevied message to server')
    $('#unknwon').append('<h6>Received: ' + msg+ '</h6>');

  });
});
