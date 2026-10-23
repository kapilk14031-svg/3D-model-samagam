const { spawn } = require('child_process');

async function test() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9230',
    'about:blank'
  ]);
  await new Promise(r => setTimeout(r, 1500));

  try {
    const list = await (await fetch('http://127.0.0.1:9230/json')).json();
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
    await send('Runtime.enable');
    await send('Page.navigate', { url: 'http://127.0.0.1:8080/samagam-3d.html' });
    await new Promise(r => setTimeout(r, 4000));

    const check = await send('Runtime.evaluate', {
      expression: `(() => {
        const sel = document.getElementById('gpsSelect');
        const errs = [];
        try {
          initGPSJumpDropdown();
        } catch(e) {
          errs.push(e.message);
        }
        return JSON.stringify({
          selExists: !!sel,
          optionsCount: sel ? sel.options.length : -1,
          optgroupsCount: sel ? sel.querySelectorAll('optgroup').length : -1,
          sampleOption: sel && sel.options[1] ? sel.options[1].textContent : null,
          errs
        });
      })()`,
      returnByValue: true
    });

    console.log('Dropdown evaluation result:', check.result.value);
    ws.close();
  } catch (err) {
    console.error('Test error:', err);
  } finally {
    chrome.kill();
  }
}
test();
