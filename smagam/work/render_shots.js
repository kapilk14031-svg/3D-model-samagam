const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const root = path.resolve(__dirname, '..');
const out = path.join(root, 'outputs');
const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const htmlPath = 'file:///' + path.join(out, 'samagam-3d.html').replace(/\\/g, '/');

async function main() {
  console.log('Launching Chrome with remote debugging on port 9222...');
  const chrome = spawn(chromePath, [
    '--headless=new',
    '--remote-debugging-port=9222',
    '--use-gl=angle',
    '--enable-webgl',
    '--window-size=1600,1050',
    '--hide-scrollbars',
    '--mute-audio',
    'about:blank'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  try {
    const listRes = await fetch('http://127.0.0.1:9222/json');
    const tabs = await listRes.json();
    const wsUrl = tabs[0].webSocketDebuggerUrl;
    console.log('Connecting to Chrome CDP via WebSocket:', wsUrl);

    const ws = new WebSocket(wsUrl);
    await new Promise((resolve, reject) => {
      ws.onopen = resolve;
      ws.onerror = reject;
    });

    let id = 1;
    const pending = new Map();
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && pending.has(msg.id)) {
        pending.get(msg.id)(msg.result || msg.error);
        pending.delete(msg.id);
      }
    };

    function send(method, params = {}) {
      return new Promise((resolve) => {
        const mid = id++;
        pending.set(mid, resolve);
        ws.send(JSON.stringify({ id: mid, method, params }));
      });
    }

    async function evaluate(expression) {
      const res = await send('Runtime.evaluate', { expression, returnByValue: true });
      return res && res.result ? res.result.value : null;
    }

    await send('Page.enable');
    await send('Runtime.enable');

    console.log('Navigating to', htmlPath);
    await send('Page.navigate', { url: htmlPath });
    await new Promise(r => setTimeout(r, 3500));

    const title = await evaluate('document.title');
    const tri = await evaluate('typeof triangles !== "undefined" ? triangles : 0');
    console.log(`Page ready: "${title}" (${tri} triangles)`);

    async function captureShot(filename, script, waitMs = 1500) {
      await evaluate(script);
      await new Promise(r => setTimeout(r, waitMs));
      await evaluate('render()');
      const res = await send('Page.captureScreenshot', { format: 'png' });
      if (res && res.data) {
        const buf = Buffer.from(res.data, 'base64');
        fs.writeFileSync(path.join(out, filename), buf);
        console.log(`Saved ${filename} (${buf.length} bytes)`);
      } else {
        console.error(`Failed to capture ${filename}`, res);
      }
    }

    // Shot 1: Grand Overview with Trees, Highway, High Masts, Camp Grounds
    await captureShot('samagam-overview-v2.png', `
      go('overview');
      yaw = 0.52; elevation = 0.78; distance = 2400; target = [50, 0, 280];
      document.getElementById('labels').checked = false;
      render();
    `, 2000);

    // Shot 2: Main Satsang Pandal with illuminated stage, golden canopy, red carpet, and avenue trees
    await captureShot('samagam-pandal-v2.png', `
      go('pandal');
      yaw = 0.65; elevation = 0.62; distance = 720; target = [250, 6, 260];
      document.getElementById('labels').checked = false;
      render();
    `, 1500);

    // Shot 3: Ceremonial Gates (Gate 1 with ivory marble, gold trims, and Nirankari peace flags)
    await captureShot('samagam-gates-preview.png', `
      go('gates');
      yaw = 1.35; elevation = 0.38; distance = 280; target = [390, 16, 490];
      document.getElementById('labels').checked = false;
      render();
    `, 1500);

    // Shot 4: Street View Walkthrough (Tree-lined Avenue with Tents and High-Mast Lighting)
    await captureShot('samagam-realistic-street.png', `
      exitNavigation();
      streetMode = true;
      walker = [320, 2.5, 420];
      heading = 0.2; pitch = 0.08;
      document.getElementById('labels').checked = false;
      render();
    `, 1500);

    // Shot 5: Evening Mode (High-mast stadium floodlights illuminating grounds, golden glowing pandal)
    await captureShot('samagam-premium-preview.png', `
      exitNavigation();
      evening = true;
      document.getElementById('light').textContent = 'Daylight';
      document.getElementById('light').classList.add('active');
      go('pandal');
      yaw = 0.62; elevation = 0.58; distance = 850; target = [260, 10, 260];
      document.getElementById('labels').checked = false;
      render();
    `, 2000);

    // Update aliases
    fs.copyFileSync(path.join(out, 'samagam-realistic-street.png'), path.join(out, 'samagam-street-view.png'));
    fs.copyFileSync(path.join(out, 'samagam-overview-v2.png'), path.join(out, 'samagam-overview.png'));
    console.log('All photorealistic preview renders completed!');

    ws.close();
  } finally {
    chrome.kill();
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
