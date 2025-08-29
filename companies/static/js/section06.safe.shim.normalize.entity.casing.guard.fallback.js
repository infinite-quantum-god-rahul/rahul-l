/* section06: normalize entity casing + guard fallback */
(function(){
  function lower(s){ return String(s||'').toLowerCase(); }
  if (typeof window.openEntityModal === "function" && !window.openEntityModal.__lowerShim){
    const _open = window.openEntityModal;
    window.openEntityModal = function(entityOrEvent){
      if (typeof entityOrEvent === "string"){
        return _open.call(this, lower(entityOrEvent));
      } else if (entityOrEvent && entityOrEvent.currentTarget){
        const el = entityOrEvent.currentTarget;
        const ent = el.getAttribute("data-entity") || el.dataset.entity || "";
        if (ent) return _open.call(this, lower(ent));
      }
      return _open.apply(this, arguments);
    }; window.openEntityModal.__lowerShim = true;
  }
  if (typeof window.editEntity === "function" && !window.editEntity.__lowerShim){
    const _edit = window.editEntity;
    window.editEntity = function(entity, id){ return _edit.call(this, lower(entity), id); };
    window.editEntity.__lowerShim = true;
  }
  ["replaceModalWithHTML","insertEntityModal"].forEach(function(fn){
    if (typeof window[fn]==="function" && !window[fn].__guardShim){
      const o = window[fn];
      window[fn] = function(){
        try{ window.__MODAL_GOT_RESPONSE = true; if(window.__FALLBACK_TIMER){ clearTimeout(window.__FALLBACK_TIMER); window.__FALLBACK_TIMER=null; } }catch(_){}
        return o.apply(this, arguments);
      }; window[fn].__guardShim = true;
    }
  });
})();
