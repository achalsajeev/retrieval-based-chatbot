/*
 s* Copyright (c) 2021 Cyfuture India Pvt. Ltd.
 *   All rights reserved.
 */
apiURL = 'http://172.22.9.33:8000'
user = {
}

const LOGOUT_DELAY = 60 * 60 * 1000;
const HELLO_DELAY = 1000;

setInterval(() => {
    status = document.querySelector('.chatbox-user-status');
    statusCircle = document.querySelector('.chatbox-user-status-circle')
    if (window.navigator.onLine) {
        statusCircle.style.backgroundColor = '#00ff2e';
        document.querySelector('.chatbox-user-status').innerText = 'Online';
    } else {
        statusCircle.style.backgroundColor = 'red';
        document.querySelector('.chatbox-user-status').innerText = 'No internet';
    }
}, 2000);


let chatbox = document.querySelector('.chatbox');
let chatboxBubble = document.querySelector('.chatbox-bubble')

let messagebox = document.querySelector('#message');
let msgWrapper = document.querySelector('.chatbox-messages-wrapper');
let messages = document.querySelector('.chatbox-messages');
let messagebtn = document.querySelector("#message-btn")
let hellobtn = document.querySelector("#hello-btn")


async function chatbox_maximize() {
    chatbox.style.display = 'flex';
    chatboxBubble.style.display = 'none';
    if (!messages.children.length) {
        await helloMessage();
    }
}

function chatbox_minimize() {
    chatbox.style.display = 'none';
    chatboxBubble.style.display = 'flex';
}

// Listeners 
chatboxBubble.addEventListener('click', chatbox_maximize)
document.getElementById('chatbox-settings-minimize').addEventListener('click', chatbox_minimize);
messagebtn.addEventListener('click', () => sendMessage());
hellobtn.addEventListener('click', () => helloMessage(0));
messagebox.addEventListener('keypress', function (e) {
    if (e.keyCode == 13) {
        sendMessage();
    }
})
document.body.addEventListener('click', e => {
    if (e.target.classList.contains('chatbox-quicklink')) {
        sendMessage(e.target.innerText.trim());
    }
})

function clearMessages() {
    messages.innerHTML = "";
}

function logout() {
    return setTimeout(async function () {
        clearMessages();
        user = {}
        chatbox_minimize();
    }, LOGOUT_DELAY);
}

async function helloMessage(delay) {
    if (!delay && delay != 0) {
        delay = HELLO_DELAY
    }
    setTimeout(async () => {
        await sendMessage('hello', true);
    }, delay)
}

async function sendMessage(message, hide) {
    if (!message) {
        message = messagebox.value.trim();
        messagebox.value = "";
    }

    if (message.length == 0)
        return;

    if (!hide) {
        node = document.createElement('div');
        node.classList.add('chatbox-message');
        node.classList.add('sent');

        textnode = document.createElement('div');
        textnode.classList.add('chatbox-text');
        textnode.innerHTML = message;

        node.append(textnode);
        messages.prepend(node)

        if (user.timeout) {
            clearTimeout(user.timeout);
        }
        user.timeout = logout();
    }

    let timeout = setTimeout(function () {
        document.getElementById('chatbox-typing').style.display = 'initial';
    }, 500)
    let data = {
        user_id: user.id,
        msg: message
    }

    // let res = await fetch('https://jsonplaceholder.typicode.com/todos/' + Math.floor(Math.random() * 200)).then(res => res.json());
    res = await fetchResponse(data);

    await receiveMessage(res, timeout)
}
async function fetchResponse(data) {
    let headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token 74089e1c25e8f3c65d87724dd75b118fb7b0d05d'
    }
    res = await fetch(apiURL + '/chat', { method: 'POST', body: JSON.stringify(data), headers: headers })
        .then(res => res.json())
        .catch(err => err);
    if (!res || res.errors || res.error) {
        res = {
            response: "Sorry! I am facing a technical breakdown. Let me fix myself up",
        }
    }

    return res;
}


async function receiveMessage(res, timeout) {
    if (res.user_id) {
        user.id = res.user_id;
    }

    node = document.createElement('div');
    node.classList.add('chatbox-message');
    node.classList.add('received');
    textnode = document.createElement('div');
    textnode.classList.add('chatbox-text');
    textnode.innerHTML = res.response;
    node.append(textnode);

    if (res.quicklinks && res.quicklinks.length) {
        listnode = document.createElement('ul');
        listnode.classList.add('chatbox-quicklinks');
        res.quicklinks.forEach(item => {
            itemnode = document.createElement('li')
            itemnode.classList.add('chatbox-quicklink');
            itemnode.innerText = item;
            listnode.append(itemnode);
        })
        node.append(listnode);
    }

    if (timeout) clearTimeout(timeout)
    document.getElementById('chatbox-typing').style.display = 'none';
    messages.prepend(node)
    messages.scrollTo({ top: messages.scrollHeight })
}
