(function(){
  function fallbackCopy(text){var t=document.createElement('textarea');t.value=text;document.body.appendChild(t);t.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(t)}
  document.addEventListener('click',function(e){
    var b=e.target.closest('button.copy'); if(!b) return;
    var text=b.parentNode.querySelector('pre code').textContent;
    var done=function(){var o=b.textContent;b.textContent='コピーしました';setTimeout(function(){b.textContent=o},1200)};
    if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(done,function(){fallbackCopy(text);done()})}
    else{fallbackCopy(text);done()}
  });
  // 目次ページ: cd 用のパスを組み立てる。file:// で開いたときは、自分の clone 先の絶対パスにする
  var rows=document.querySelectorAll('code[data-rel]');
  if(rows.length){
    var abs=null;
    if(location.protocol==='file:'){
      try{
        abs=decodeURIComponent(location.pathname).replace(/\/index\.html$/,'').replace(/\/$/,'');
        if(/^\/[A-Za-z]:/.test(abs)) abs=abs.slice(1);
      }catch(e){abs=null}
    }
    rows.forEach(function(c){
      var path=(abs?abs+'/':'')+c.dataset.rel;
      // スペースなどを含むパスは、シェルで壊れないよう引用符で囲む
      if(/[^A-Za-z0-9_\/.:~-]/.test(path)) path='"'+path.replace(/(["$`\\])/g,'\\$1')+'"';
      c.textContent='cd '+path;
    });
    var mode=document.getElementById('path-mode');
    if(mode) mode.textContent=abs?'このコンピュータの絶対パスで表示しています（'+abs+'）':'リポジトリ直下からの相対パスで表示しています。ファイルを直接開く（file://）と、絶対パスになります';
  }
  var page=location.pathname;
  document.querySelectorAll('input[data-step]').forEach(function(c){
    var key='steps:'+page+':'+c.dataset.step;
    try{c.checked=localStorage.getItem(key)==='1'}catch(e){}
    c.addEventListener('change',function(){try{localStorage.setItem(key,c.checked?'1':'0')}catch(e){}});
  });
})();
