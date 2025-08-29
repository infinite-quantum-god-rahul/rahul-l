/* section07: final UI unlock shim (append-only) */
(function(){
  function unlock(){
    try{
      window.__MODAL_GOT_RESPONSE = true;
      if (window.__FALLBACK_TIMER){ clearTimeout(window.__FALLBACK_TIMER); window.__FALLBACK_TIMER=null; }
    }catch(_){}
    var sel=[
      ".modal-backdrop",".loading-overlay",".preloader",".global-loader",".page-loader",
      ".blockUI",".blockOverlay",".blockMsg",".ui-dimmer",".screen-lock",".prevent-click",
      "#loading","#loader","#overlay","#preloader","#ajaxLoading","#page-loader","#spinner"
    ].join(",");
    document.querySelectorAll(sel).forEach(function(n){ try{ n.remove(); }catch(_){ n.style.display="none"; n.style.pointerEvents="none"; } });
    var b=document.body; if (b){ ["loading","disabled","busy","blocked","modal-open"].forEach(function(c){ b.classList.remove(c); }); b.removeAttribute("inert"); b.removeAttribute("aria-busy"); b.style.pointerEvents="auto"; if (b.style.overflow==="hidden") b.style.overflow=""; }
    if (!document.getElementById("force-unfreeze-style")){
      var s = document.createElement("style"); s.id="force-unfreeze-style"; s.textContent=".modal, .modal *{pointer-events:auto!important}";
      document.head.appendChild(s);
    }
  }
  ["replaceModalWithHTML","insertEntityModal","openLoadingShell"].forEach(function(fn){
    if (typeof window[fn]==="function" && !window[fn].__unlockShim){
      var o = window[fn];
      window[fn] = function(){ var r=o.apply(this,arguments); try{ unlock(); }catch(_){ } return r; };
      window[fn].__unlockShim = true;
    }
  });
  try{
    new MutationObserver(function(m){
      for (var i=0;i<m.length;i++){ var r=m[i]; for (var j=0;j<r.addedNodes.length;j++){ var n=r.addedNodes[j]; if (n.nodeType===1 && (n.id==="entity-modal" || n.classList?.contains("modal-backdrop"))){ unlock(); return; } } }
    }).observe(document.documentElement||document.body,{childList:true,subtree:true});
  }catch(_){}
  try{ unlock(); }catch(_){}
})();
