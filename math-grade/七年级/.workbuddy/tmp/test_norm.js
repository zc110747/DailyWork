// 用页面里真实的 norm()/keyOf() 源码做答案容错回归
const fs = require('fs');
const src = fs.readFileSync('.workbuddy/tmp/app.js', 'utf8');
const start = src.indexOf('function norm(s)');
const end = src.indexOf('/* ---------- 选择题');
const code = src.slice(start, end);
eval(code);

let pass = 0, fail = 0;
function t(input, answers, expect) {
  const list = answers.split('|');
  const got = list.some(a => keyOf(a) === keyOf(input));
  const ok = got === expect;
  ok ? pass++ : fail++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  "${input}"  vs [${answers}]  => ${got} (exp ${expect})`);
}

// 第 11 题
t('5', '5', true);
t(' 5 ', '5', true);
t('６', '5', false);
t('-9', '-9|（-9）|(-9)', true);
t('（-9）', '-9|（-9）|(-9)', true);
t('−9', '-9|（-9）|(-9)', true);   // U+2212 减号
t('9', '-9|（-9）|(-9)', false);
// 第 12 题
t('4', '4', true);
t('±2', '±2|+-2|2或-2|-2或2', true);
t('2或-2', '±2|+-2|2或-2|-2或2', true);
t('-2或2', '±2|+-2|2或-2|-2或2', true);
t('±4', '±2|+-2|2或-2|-2或2', false);
// 第 13 / 16 题
t('5', '5', true);
t('156', '156', true);
// 第 14 题
t('115°18′', '115°18′|115度18分', true);
t("115°18'", '115°18′|115度18分', true);
t('115度18分', '115°18′|115度18分', true);
t('115°18', '115°18′|115度18分', false);
// 第 15 题
t('3或7', '3或7|7或3|3,7|7,3', true);
t('7或3', '3或7|7或3|3,7|7,3', true);
t('3、7', '3或7|7或3|3,7|7,3', true);
t('7cm和3cm', '3或7|7或3|3,7|7,3', true);
t('3', '3或7|7或3|3,7|7,3', false);
t('3或5', '3或7|7或3|3,7|7,3', false);
// 空值
t('', '5', false);

console.log(`\n${pass} PASS / ${fail} FAIL`);
process.exit(fail ? 1 : 0);
