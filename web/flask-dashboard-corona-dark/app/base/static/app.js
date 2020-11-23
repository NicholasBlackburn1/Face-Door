var socket = io.connect('http://' + document.domain + ':' + location.port);
// verify our websocket connection is established
socket.on('connect', function() {
    console.log('Websocket connected!');
    socket.emit('create', {size: 'normal', teams: 2, dictionary: 'Simple'});
});
