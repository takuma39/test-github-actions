(function(){
  function fallbackCopy(text){var t=document.createElement('textarea');t.value=text;document.body.appendChild(t);t.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(t)}
  document.addEventListener('click',function(e){
    var b=e.target.closest('button.copy'); if(!b) return;
    var text=b.parentNode.querySelector('pre code').textContent;
    var done=function(){var o=b.textContent;b.textContent='コピーしました';setTimeout(function(){b.textContent=o},1200)};
    if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(done,function(){fallbackCopy(text);done()})}
    else{fallbackCopy(text);done()}
  });
  var page=location.pathname;
  document.querySelectorAll('input[data-step]').forEach(function(c){
    var key='steps:'+page+':'+c.dataset.step;
    try{c.checked=localStorage.getItem(key)==='1'}catch(e){}
    c.addEventListener('change',function(){try{localStorage.setItem(key,c.checked?'1':'0')}catch(e){}});
  });
})();
