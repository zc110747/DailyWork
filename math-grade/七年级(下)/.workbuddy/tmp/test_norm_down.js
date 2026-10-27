// 七下三套卷 填空题答案容错回归
const fs = require('fs');

function load(file) {
  const src = fs.readFileSync(file, 'utf8');
  const js = src.slice(src.indexOf('<script>') + 8, src.indexOf('</script>'));
  const f = new Function(js.slice(js.indexOf('function norm(s)'), js.indexOf('/* ---------- 选择题'))
    + '; return {norm: norm, keyOf: keyOf};');
  const { keyOf } = f();
  const re = /<input class="bi" data-answers="([^"]*)"/g;
  const answers = [];
  let m;
  while ((m = re.exec(src)) !== null) answers.push(m[1]);
  return { keyOf, answers };
}

const CASES = {
  '1001-七年级(下).html': [
    ['11', 0, false], ['-11', 0, true], ['（-11）', 0, true], ['-(-11)', 0, false], ['−11', 0, true],
    ['±6', 1, true], ['6或-6', 1, true], ['-6或6', 1, true], ['+6或-6', 1, true], ['6', 1, false],
    ['2', 2, true], ['2组', 2, true], ['3', 2, false],
    ['20', 3, true], ['20%', 3, true], ['20％', 3, true], ['百分之二十', 3, true], ['72', 3, false],
    ['19', 4, true], ['25', 4, false],
    ['10', 5, true], ['0.25', 5, false],
  ],
  '1002-七年级(下).html': [
    ['3', 0, true], ['1', 0, false],
    ['12', 1, true], ['16', 1, false],
    ['1', 2, true], ['-1', 2, false],
    ['50或130', 3, true], ['130或50', 3, true], ['50,130', 3, true], ['50°或130°', 3, true], ['50', 3, false],
    ['3', 4, true], ['1/3', 4, false],
    ['60', 5, true], ['240', 5, false],
  ],
  '1003-七年级(下).html': [
    ['2', 0, true], ['0', 0, false],
    ['3', 1, true], ['-3', 1, false],
    ['1', 2, true], ['2', 2, false],
    ['-2', 3, true], ['（-2）', 3, true], ['2', 3, false],
    ['75', 4, true], ['15', 4, false],
    ['32', 5, true], ['12', 5, false],
  ],
};

let pass = 0, fail = 0;
for (const [file, cases] of Object.entries(CASES)) {
  const { keyOf, answers } = load(file);
  console.log(`--- ${file}：提取 ${answers.length} 个空 ---`);
  for (const [input, idx, expect] of cases) {
    const got = answers[idx].split('|').some(a => keyOf(a) === keyOf(input));
    const ok = got === expect;
    ok ? pass++ : fail++;
    if (!ok) console.log(`FAIL  "${input}" vs [${answers[idx]}] => ${got} (exp ${expect})`);
  }
}
console.log(`\n${pass} PASS / ${fail} FAIL`);
process.exit(fail ? 1 : 0);
