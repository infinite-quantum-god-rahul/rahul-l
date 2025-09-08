(()=>{
  const S=['.modal-backdrop','.loading-overlay','.preloader','.global-loader','.page-loader','.blockUI','.blockOverlay','.blockMsg','.ui-dimmer','.screen-lock','.prevent-click','#loading','#loader','#overlay','#preloader','#ajaxLoading','#page-loader','#spinner'];
  function u(){
    try{window.__MODAL_GOT_RESPONSE=true;if(window.__FALLBACK_TIMER){clearTimeout(window.__FALLBACK_TIMER);window.__FALLBACK_TIMER=null}}catch(e){}
    S.forEach(s=>document.querySelectorAll(s).forEach(n=>{try{n.remove()}catch(e){n.style.display='none';n.style.pointerEvents='none'}}));
    const b=document.body;
    if(b){
      ['loading','disabled','busy','blocked','modal-open'].forEach(c=>b.classList.remove(c));
      b.removeAttribute('inert'); b.removeAttribute('aria-busy');
      b.style.pointerEvents='auto';
      if(b.style.overflow==='hidden') b.style.overflow='';
    }
  }
  try{u()}catch(_){}
  document.addEventListener('DOMContentLoaded', u);
  try{
    new MutationObserver(m=>{
      for(const x of m){
        for(const n of x.addedNodes){
          if(n.nodeType===1 && (n.id==='entity-modal' || n.classList?.contains('modal-backdrop'))){ u(); return; }
        }
      }
    }).observe(document.documentElement||document.body,{childList:true,subtree:true});
  }catch(_){}
})();
