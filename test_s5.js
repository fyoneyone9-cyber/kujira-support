const fs = require('fs');
const c = fs.readFileSync('C:/AI/ComfyUI/dashboard.html','utf8');
const m = c.match(/<script[^>]*>([\s\S]*?)<\/script>/g) || [];
let ok = 0, ng = 0;
m.forEach((s, i) => {
  try {
    new Function(s.replace(/<\/?script[^>]*>/g, ''));
    ok++;
  } catch(e) {
    ng++;
    if (ng <= 3) console.log('ERR block', i, e.message.slice(0, 80));
  }
});
console.log('ok:', ok, 'ng:', ng);
