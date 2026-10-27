// 0003 填空题答案容错回归
const fs = require('fs');
const src = fs.readFileSync('0003-七年级(上).html', 'utf8');

const js = src.slice(src.indexOf('<script>') + 8, src.indexOf('</script>'));
eval(js.slice(js.indexOf('function norm(s)'), js.indexOf('/* ---------- 选择题')));

const re = /<input class="bi" data-answers="([^"]*)"/g;
const answers = [];
let m;
while ((m = re.exec(src)) !== null) answers.push(m[1]);
console.log('共提取空数：', answers.length, '(应为 6)');

const cases = [
  ['10', 0, true], [' 10 ', 0, true], ['-10', 0, false],
  ['3.142', 1, true], ['3.14', 1, false], ['3.1416', 1, false],
  ['8', 2, true], ['8.0', 2, false], ['6', 2, false],
  ['-5', 3, true], ['（-5）', 3, true], ['−5', 3, true], ['5', 3, false],
  ['20', 4, true], ['20°', 4, true], ['20度', 4, true], ['60', 4, false],
  ['4x+16', 5, true], ['16+4x', 5, true], ['4(x+4)', 5, true], ['4X+16', 5, true], ['4x+6', 5, false],
];

let pass = 0, fail = 0;
for (const [input, idx, expect] of cases) {
  const got = answers[idx].split('|').some(a => keyOf(a) === keyOf(input));
  const ok = got === expect;
  ok ? pass++ : fail++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  "${input}"  vs [${answers[idx]}] => ${got} (exp ${expect})`);
}
console.log(`\n${pass} PASS / ${fail} FAIL`);
process.exit(fail ? 1 : 0);
