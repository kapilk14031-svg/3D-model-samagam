const { spawn } = require('child_process');
const fs = require('fs');

async function capture() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--window-size=1600,1000',
    '--remote-debugging-port=9229',
    'about:blank'
  ]);
  await new Promise(r => setTimeout(r, 1500));

  try {
    const list = await (await fetch('http://127.0.0.1:9229/json')).json();
    const target = list.find(t => t.type === 'page') || list[0];
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    let id = 1;
    function send(method, params = {}) {
      return new Promise(resolve => {
        const mid = id++;
        const handler = (e) => {
          const msg = JSON.parse(e.data);
          if (msg.id === mid) {
            ws.removeEventListener('message', handler);
            resolve(msg.result || msg.error);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: mid, method, params }));
      });
    }

    await send('Page.enable');
    await send('Page.navigate', { url: 'http://127.0.0.1:8080/samagam-3d.html' });

    // Wait 5 seconds for WebGL render to settle
    await new Promise(r => setTimeout(r, 5000));

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync('79-th-nirankari-sant-samagam-bhodwal/outputs/samagam-live-browser-view.png', Buffer.from(shot.data, 'base64'));
    console.log('Live browser screenshot saved to outputs/samagam-live-browser-view.png');

    ws.close();
  } catch (err) {
    console.error(err);
  } finally {
    chrome.kill();
  }
}
capture();
