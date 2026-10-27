# -*- coding: utf-8 -*-
"""交互探针：注入脚本模拟作答，把结果写进 document.title，再用 --dump-dom 读回。"""
import io, sys

src, out = sys.argv[1], sys.argv[2]
s = io.open(src, encoding='utf-8').read()

PROBE = '''
<script>
window.addEventListener("load", function(){
  setTimeout(function(){
    var qs = document.querySelectorAll(".q[data-type=choice]");
    var a1 = qs[0].dataset.answer;
    qs[0].querySelector('.opt[data-opt="' + a1 + '"]').click();
    var a2 = qs[1].dataset.answer;
    var wrong = ["A","B","C","D"].filter(function(x){ return x !== a2; })[0];
    qs[1].querySelector('.opt[data-opt="' + wrong + '"]').click();
    var bi = document.querySelectorAll(".bi");
    bi[0].value = bi[0].dataset.answers.split("|")[0];
    bi[0].dispatchEvent(new Event("blur"));
    bi[1].value = "zzz";
    bi[1].dispatchEvent(new Event("blur"));
    document.getElementById("btn-judge").click();
    var sd = document.querySelector(".selfscore");
    if(sd){ sd.value = 3; sd.dispatchEvent(new Event("input")); }
    var t = document.getElementById("total-score");
    var o = document.getElementById("obj-score");
    var sf = document.getElementById("self-score");
    var foot = document.getElementById("sum-check");
    document.title = "PROBE|obj=" + o.textContent + "|self=" + sf.textContent +
      "|total=" + t.textContent + "|ok=" + document.querySelectorAll(".q.ok").length +
      "|bad=" + document.querySelectorAll(".q.bad").length +
      "|shownAns=" + document.querySelectorAll(".ans.show").length +
      "|correctMark=" + document.querySelectorAll(".opt.correct").length +
      "|wrongMark=" + document.querySelectorAll(".opt.wrong").length +
      "|foot=" + (foot ? foot.textContent.replace(/\\s+/g,"") : "NONE");
  }, 300);
});
</script>
'''
s = s.replace('</body>', PROBE + '</body>', 1)
io.open(out, 'w', encoding='utf-8').write(s)
print('probe written:', out)
