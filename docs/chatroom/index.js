function $(id) {
  return document.getElementById(id);
}

function log(text) {
  $('log').value += text + '\n';
}

function xhrWithAuth(method, url, interactive, callback) {
  var access_token;

  var retry = true;

  getToken();

  function getToken() {
    chrome.identity.getAuthToken({ interactive: interactive }, function(token) {
      if (chrome.runtime.lastError) {
        callback(chrome.runtime.lastError);
        return;
      }

      access_token = token;
      requestStart();
    });
  }

  function requestStart() {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.setRequestHeader('Authorization', 'Bearer ' + access_token);
    xhr.onload = requestComplete;
    xhr.send();
  }

  function requestComplete() {
    if (this.status == 401 && retry) {
      retry = false;
      chrome.identity.removeCachedAuthToken({ token: access_token },
                                            getToken);
    } else {
      callback(null, this.status, this.response);
    }
  }
}

var person;
function onUserInfoFetched(error, status, response) {
  if (!error && status == 200) {
    user_info = JSON.parse(response);
    person = user_info.name.givenName;
  }
}

chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
  xhrWithAuth('GET', 'https://www.googleapis.com/plus/v1/people/me', true, onUserInfoFetched);
});

function revokeToken() {
  user_info_div.innerHTML="";
  chrome.identity.getAuthToken({ 'interactive': false },
    function(current_token) {
      if (!chrome.runtime.lastError) {

        // @corecode_begin removeAndRevokeAuthToken
        // @corecode_begin removeCachedAuthToken
        // Remove the local cached token
        chrome.identity.removeCachedAuthToken({ token: current_token },
          function() {});
        // @corecode_end removeCachedAuthToken

        // Make a request to revoke token in the server
        var xhr = new XMLHttpRequest();
        xhr.open('GET', 'https://accounts.google.com/o/oauth2/revoke?token=' +
                 current_token);
        xhr.send();
        // @corecode_end removeAndRevokeAuthToken

        // Update the user interface accordingly
        changeState(STATE_START);
        sampleSupport.log('Token revoked and removed from cache. '+
          'Check chrome://identity-internals to confirm.');
      }
  });
}

var port = 9999;
var isServer = false;
if (http.Server && http.WebSocketServer) {
  // Listen for HTTP connections.
  var server = new http.Server();
  var wsServer = new http.WebSocketServer(server);
  server.listen(port);
  isServer = true;

  server.addEventListener('request', function(req) {
    var url = req.headers.url;
    if (url == '/')
      url = '/index.html';
    // Serve the pages of this chrome application.
    req.serveUrl(url);
    return true;
  });

  // A list of connected websockets.
  var connectedSockets = [];

  wsServer.addEventListener('request', function(req) {
    log('Client connected');
    var socket = req.accept();
    connectedSockets.push(socket);

    // When a message is received on one socket, rebroadcast it on all
    // connected sockets.
    socket.addEventListener('message', function(e) {
      for (var i = 0; i < connectedSockets.length; i++)
        connectedSockets[i].send(person + ': ' + e.data);
    });

    // When a socket is closed, remove it from the list of connected sockets.
    socket.addEventListener('close', function() {
      log('Client disconnected');
      for (var i = 0; i < connectedSockets.length; i++) {
        if (connectedSockets[i] == socket) {
          connectedSockets.splice(i, 1);
          break;
        }
      }
    });
    return true;
  });
}

document.addEventListener('DOMContentLoaded', function() {
  log('Proximity Chrome v0.0.1');
// FIXME: Wait for 1s so that HTTP Server socket is listening...
setTimeout(function() {
  var address = isServer ? 'ws://localhost:' + port + '/' :
      window.location.href.replace('http', 'ws');
  var ws = new WebSocket(address);
  ws.addEventListener('open', function() {
    log('Connected to localhost port ' + port);
  });
  ws.addEventListener('close', function() {
    log('Connection lost');
    $('input').disabled = true;
  });
  ws.addEventListener('message', function(e) {
    log(e.data);
  });
  $('input').addEventListener('keydown', function(e) {
    if (ws && ws.readyState == 1 && e.keyCode == 13) {
      ws.send(this.value);
      this.value = '';
    }
  });
}, 1e3);
});
