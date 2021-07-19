document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    const username = document.querySelector('#get-username').innerHTML;

    let room = 'general';
    joinRoom('general')

    socket.on('message', (data) => {
        if (data.msg) {
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br')

            if (data.username == username) {
                p.setAttribute("class", "my-msg");
                span_username.setAttribute("class", "my-username");

                span_username.innerHTML = data.username;

                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerHTML = data.time_stamp;

                p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
                document.querySelector('#messages').append(p);

            } else if (typeof data.username !== 'undefined') {
                p.setAttribute("class", "others-msg");

                // Username
                span_username.setAttribute("class", "other-username");
                span_username.innerText = data.username;

                // Timestamp
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = data.time_stamp;

                // HTML to append
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

                //Append
                document.querySelector('#messages').append(p);
            }
            else {
                printSysMsg(data.msg)
            }

        }
        scrollDownChatWindow();
    });

    document.querySelector('#sendBtn').onclick = () => {
        socket.send({ 'msg': document.querySelector('#message').value, 'username': username, 'room': room });
        document.querySelector('#message').value = '';
    }

    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `You already in ${room} channel.`;
                printSysMsg(msg);
            } else {
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    })


    function leaveRoom(room) {
        socket.emit('leave', { 'username': username, 'room': room });
        document.querySelectorAll('.select-room').forEach(p => {
            p.style.color = "black";
        });
    }

    function joinRoom(room) {
        socket.emit('join', { 'username': username, 'room': room });

        document.querySelector('#messages').innerHTML = '';

        document.querySelector('#message').focus();
    }

    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#messages");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#messages').append(p);
        scrollDownChatWindow()

        document.querySelector('#message').focus();
    }
})