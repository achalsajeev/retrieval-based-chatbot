(
    async function load() {
        let url = 'http://172.22.9.33:8000/static/chatbox';
        // let url = '';
        let head = document.getElementsByTagName('head')[0];
        let body = document.getElementsByTagName('body')[0];

        head.innerHTML += `<link rel="stylesheet" data-id="chatbox-css" href="${url}/static/styles.css">`;
        head.innerHTML += '<link rel="preconnect" href="https://fonts.gstatic.com">';
        head.innerHTML += '<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700&display=swap" rel="stylesheet"></link>';

        chatbot_html = await fetch(`${url}/static/chatbot.html`).then(res => res.text());
        node = document.createElement('div');
        node.innerHTML = chatbot_html;
        body.appendChild(node)


        chatbot_js = document.createElement('script');
        chatbot_js.type = 'text/javascript'; chatbot_js.charset = 'utf-8'; chatbot_js.async = true; chatbot_js.defer = true;
        chatbot_js.src = `${url}/static/chatbot.js`; body.appendChild(chatbot_js);
    }
)()
