const { spawn } = require('child_process');

async function test() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
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
        title: document.title,
        loadingDisplay: document.getElementById('loading') ? document.getElementById('loading').style.display : 'no loading elem',
        loadingText: document.getElementById('loading') ? document.getElementById('loading').innerText : '',
        hasCanvas: !!document.getElementById('model'),
        gpsHudVisible: !!document.getElementById('gpsHud'),
        gpsCoords: document.getElementById('gpsLatLon') ? document.getElementById('gpsLatLon').textContent : null,
        gpsFeatureName: document.getElementById('gpsFeatureName') ? document.getElementById('gpsFeatureName').textContent : null,
        gpsSelectCount: document.getElementById('gpsSelect') ? document.getElementById('gpsSelect').querySelectorAll('option').length : 0,
        gpsSelectOptgroups: document.getElementById('gpsSelect') ? document.getElementById('gpsSelect').querySelectorAll('optgroup').length : 0,
        totalGpsPointsInJS: typeof GPS_POINTS !== 'undefined' ? GPS_POINTS.length : 0,
        depUnitsCount: typeof depUnits !== 'undefined' ? depUnits.length : 0
      })`,
      returnByValue: true
    });
    console.log('GPS Alignment & Viewer State:\n', JSON.stringify(JSON.parse(res.result.value), null, 2));

    // Test jumping to a point via dropdown
    console.log('Testing jump to point 1 (Gate 3)...');
    await send('Runtime.evaluate', {
      expression: `
        const sel = document.getElementById('gpsSelect');
        sel.value = "1";
        sel.dispatchEvent(new Event('change'));
      `
    });
    await new Promise(r => setTimeout(r, 1000));

    const jumpRes = await send('Runtime.evaluate', {
      expression: `JSON.stringify({
        target: typeof target !== 'undefined' ? target : null,
        gpsCoords: document.getElementById('gpsLatLon').textContent,
        gpsFeatureName: document.getElementById('gpsFeatureName').textContent,
        navMessage: document.getElementById('navMessage').textContent
      })`,
      returnByValue: true
    });
    console.log('Jump Result:\n', JSON.stringify(JSON.parse(jumpRes.result.value), null, 2));

    ws.close();
  } catch (err) {
    console.error('Test error:', err);
  } finally {
    chrome.kill();
  }
}
test();
