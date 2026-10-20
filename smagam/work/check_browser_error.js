const { spawn } = require('child_process');

async function test() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9228',
    'about:blank'
  ]);
  await new Promise(r => setTimeout(r, 1500));

  try {
    const list = await (await fetch('http://127.0.0.1:9228/json')).json();
    console.log('Available targets:', list.map(t => ({ type: t.type, title: t.title, url: t.url })));
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

    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      if (msg.method === 'Runtime.consoleAPICalled') {
        console.log('CONSOLE:', msg.params.type, msg.params.args.map(a => a.value || a.description));
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        console.error('EXCEPTION:', JSON.stringify(msg.params.exceptionDetails, null, 2));
      }
    };

    await send('Page.enable');
    await send('Runtime.enable');
    console.log('Navigating to http://127.0.0.1:8080/samagam-3d.html ...');
    await send('Page.navigate', { url: 'http://127.0.0.1:8080/samagam-3d.html' });

    // Wait 5 seconds
    await new Promise(r => setTimeout(r, 5000));

    const res = await send('Runtime.evaluate', {
      expression: `JSON.stringify({
        href: window.location.href,
        title: document.title,
        loadingDisplay: document.getElementById('loading') ? document.getElementById('loading').style.display : 'no loading elem',
        loadingText: document.getElementById('loading') ? document.getElementById('loading').innerText : '',
        hasCanvas: !!document.getElementById('model'),
        canvasWidth: document.getElementById('model') ? document.getElementById('model').width : 0
      })`,
      returnByValue: true
    });
    console.log('Page State:', res.result ? res.result.value : res);

    ws.close();
  } catch (err) {
    console.error('Test error:', err);
  } finally {
    chrome.kill();
  }
}
test();
