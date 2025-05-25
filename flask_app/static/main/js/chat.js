let socket;

document.addEventListener("DOMContentLoaded", function () {
    socket = io('/chat');

    socket.on('connect', function () {
        socket.emit('joined', {});
    });

    socket.on('status', function (data) {
        let style;
        let content;

        if (data.user === "owner@email.com") {
            style = "color: blue; text-align: right;";
            content = data.msg; 
        } else {
            style = "color: grey; text-align: left;";
            content = data.msg;
        }

        appendMessage(content, style);
    });

    socket.on('message', function (data) {
        let style;
        let content;

        if (data.user === "owner@email.com") {
            style = "color: blue; text-align: right;";
            content = data.msg; 
        } else {
            style = "color: grey; text-align: left;";
            content = data.msg;
        }

        appendMessage(content, style);
    });

    document.querySelector(".chat-input").addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            const input = e.target;
            const message = input.value.trim();
            if (message !== "") {
                socket.emit("text", { msg: message });
                input.value = "";
            }
            e.preventDefault();
        }
    });

    document.querySelector(".chat-leave").addEventListener("click", function () {
        socket.emit("left", {});
        window.location.href = "/";
    });
});

function appendMessage(msg, style) {
    const chat = document.getElementById("chat");
    const p = document.createElement("p");
    p.textContent = msg;
    p.style.cssText = style;
    chat.appendChild(p);
    chat.scrollTop = chat.scrollHeight;
}
