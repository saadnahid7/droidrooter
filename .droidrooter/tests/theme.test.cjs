const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
assert.ok(fs.existsSync(path.join(root,'assets/theme/init.js')), 'Theme initialization must exist');
const code=fs.readFileSync(path.join(root,'assets/theme/init.js'),'utf8');
for(const [saved,blocked,expected] of [[null,false,'dark'],['light',false,'light'],['dark',false,'dark'],['invalid',false,'dark'],[null,true,'dark']]) {
 const html={dataset:{},style:{}};
 vm.runInNewContext(code,{document:{documentElement:html},localStorage:{getItem(){if(blocked)throw Error('blocked');return saved;}}});
 assert.equal(html.dataset.colorMode,expected);
 assert.equal(html.style.colorScheme,expected);
}
console.log('PASS: dark default, saved preference, invalid preference, blocked storage');
