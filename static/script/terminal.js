// TextScramble
class TextScramble {
    constructor(el) {
        this.el = el;
        this.chars = "!<>-_\\/[]{}—=+*^?#________";
        this.update = this.update.bind(this);
    }
    
    setText(newText) {
        const oldText = toString(this.el.innerText);
        const length = Math.max(oldText.length, newText.length);
        const promise = new Promise(resolve => this.resolve = resolve);
        this.queue = [];
        for (let i = 0; i < length; i++) {
            const from = oldText[i] || '';
            const to = newText[i] || '';
            const start = Math.floor(Math.random() * 40);
            const end = start + Math.floor(Math.random() * 40);
            this.queue.push({ from, to, start, end });
        }
        cancelAnimationFrame(this.frameRequest);
        this.frame = 0;
        this.update(newText);
        return promise;
    }
    update() {
        let output = "";
        let complete = 0;
        for (let i = 0, n = this.queue.length; i < n; i++) {
            let { from, to, start, end, char } = this.queue[i];
            if (this.frame >= end) {
                complete++;
                output += to;
            } else if (this.frame >= start) {
                if (!char || Math.random() < 0.28) {
                    char = this.randomChar();
                    this.queue[i].char = char;
                }
                output += `<span class="dud">${char}</span>`;
            } else {
                output += from;
            }
        }
        if (complete === this.queue.length) {
            this.el.innerHTML = output;
            let ul = document.getElementById("chat-messages");
            let li = document.createElement("li");
            let pre = document.createElement("pre");
            li.classList.add('fade_in_el');
            if (output.includes('\\')) {li.classList.add('centered-li');}
            if (RegExp('[|]').test(output)) {li.classList.add('centered-li');}
            li.appendChild(pre);
            pre.appendChild(document.createTextNode(output));
            ul.appendChild(li);
            ul.scrollTop = ul.scrollHeight;
            this.el.classList.add('fade_out_el')
            this.el.classList.remove('fade_in_el')
            console.log('after')
            this.resolve();
        } else {
            this.el.classList.add('fade_in_el')
            this.el.classList.remove('fade_out_el')
            this.el.innerHTML = output;
            this.frameRequest = requestAnimationFrame(this.update);
            this.frame++;
        }
    }
    randomChar() {
        return this.chars[Math.floor(Math.random() * this.chars.length)];
    }}
    

let el = document.querySelector("#msglst");
const fx = new TextScramble(el);

    const scrapping_on = document.getElementById('scrapping')
    var socket = io({autoConnect: false});
    
    socket.connect();
    socket.on('connect', function() {
        console.log('connecting...')
        socket.emit('my_event', 'Start scrapping')

    if (scrapping_on == null) {
    const welcome_screen = [
        " /^--^\\     /^--^\\     /^--^\\",
        ' \\____/     \\____/     \\____/',
        ' /      \\   /      \\   /      \\',
        ' |        | |        | |        |',
        ' \\__  __/   \\__  __/   \\__  __/',
        '|^|^|^|^|^|^|^|^|^|^|^|^|^|^\\ \\^|^|^|^/ /^|^|^|^|^\\ \\^|^|^|^|^|^|^|^|^|^|^|^|^|',
        '|_|_|_|_|_|_|_|_|_|_|_|_|_|_|\\ \\|_|_|/ /|_|_|_|_|_|\\ \\|_|_|_|_|_|_|_|_|_|_|_|_|',
        '|  ___          _   ___    _ /_/    _\\ \\        _  /_/        _               |',
        '| | _ \\___ __ _| | | __|__| |_ __ _| |_/___    /_\\  _ _  __ _| |_  _____ _ _  |',
        "| |   / -_) _` | | | _|(_-<  _/ _` |  _/ -_)  / _ \\| ' \\/ _` | | |/ / -_) '_| |",
        '| |_|_\\___\\__,_|_| |___/__/\\__\\__,_|\\__\\___| /_/ \\_\\_||_\\__,_|_|   /\\___|_|   |',
        '|______________________________________________________________/__/___________|',
        '| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |',
        '| | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |'
    ];
    
    function task(i) {
        setTimeout(function() {
            fx.setText(welcome_screen[i])
            console.log(i);
        }, 1350 * i);
    }

    for (let i=0; i<14; i++) {
        task(i);
    }

    socket.emit('response_handler', 'Terminal logo done');

    }
    else{
    }  
});

    
socket.on("my_response", function(data) {
    console.log(data, 'myresp');
    fx.setText(data);
    });