// 0002 填空题答案容错回归：直接从页面里抽 data-answers 来测
const fs = require('fs');
const src = fs.readFileSync('0002-七年级(上).html', 'utf8');

// 抽脚本里的 norm/keyOf
const js = src.slice(src.indexOf('<script>') + 8, src.indexOf('</script>'));
const code = js.slice(js.indexOf('function norm(s)'), js.indexOf('/* ---------- 选择题'));
eval(code);

// 抽每道填空题的 data-answers
const re = /<input class="bi" data-answers="([^"]*)"/g;
const answers = [];
let m;
while ((m = re.exec(src)) !== null) answers.push(m[1]);
console.log('共提取空数：', answers.length, '(应为 7)');

const cases = [
  // [用户输入, 空序号(0起), 期望]
  ['9', 0, true],
  ['±4', 1, true], ['4', 1, false], ['-4或4', 1, true], ['+4或-4', 1, true],
  ['-3/5', 2, true], ['−3/5', 2, true], ['- 3/5', 2, true], ['-0.6', 2, true], ['3/5', 2, false],
  ['3', 3, true], ['2', 3, false],
  ['-1', 4, true], ['（-1）', 4, true], ['−(1)', 4, false],
  ['75', 5, true], ['75°', 5, true], ['75度', 5, true], ['60', 5, false],
  ['5/26', 6, true], ['5／26', 6, true], ['5/24', 6, false],
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
