/* modal_hotfix.js — hard patch for re-opening and duplicate Close */
(function(){
  'use strict';

  // Soft-kill any stale modal on load
  function kill(){
    var m = document.getElementById('entity-modal');
    if (m && m.parentNode) m.parentNode.removeChild(m);
    var b = document.getElementById('modal-backdrop');
    if (b && b.parentNode) b.parentNode.removeChild(b);
    document.body.removeAttribute('inert');
  }
  kill();

  // Guard to prevent immediate re-open after close (caused by lingering click callbacks)
  var lastCloseAt = 0;
  var SILENCE_MS = 600;

  // Patch close function
  var _close = window.closeEntityModal;
  window.closeEntityModal = function(forceRefresh){
    lastCloseAt = Date.now();
    try{ if (typeof _close === 'function') _close(forceRefresh); } finally {
      kill();
    }
  };

  // Centralized open wrappers with silence window
  function openGuarded(fn){
    return function(){
      var now = Date.now();
      if (now - lastCloseAt < SILENCE_MS) return; // ignore stray opens
      kill(); // always start clean
      return fn.apply(this, arguments);
    };
  }

  if (typeof window.openEntityModal === 'function'){
    window.openEntityModal = openGuarded(window.openEntityModal);
  }
  if (typeof window.editEntity === 'function'){
    window.editEntity = openGuarded(window.editEntity);
  }

  // De-dupe any close buttons that are not in header
  document.addEventListener('click', function(){
    var modal = document.getElementById('entity-modal');
    if (!modal) return;
    var headerClose = modal.querySelector('.modal-header .close-btn, .modal-header .modal-close');
    // hide other closes in body/footer
    modal.querySelectorAll('.modal-body .close-btn, .modal-footer .close-btn, .modal-body .modal-close, .modal-footer .modal-close')
      .forEach(function(n){ n.style.display = 'none'; });
    // ensure header close exists
    if (!headerClose){
      var h = modal.querySelector('.modal-header');
      if (h){
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'close-btn';
        btn.innerText = '✕';
        btn.onclick = function(){ window.closeEntityModal(false); };
        h.appendChild(btn);
      }
    }
  }, true);

  // Close modal on any top-level nav click before handler runs
  document.addEventListener('click', function(e){
    var t = e.target.closest && e.target.closest('a, [data-entity], [data-nav], button');
    if (!t) return;
    if (document.getElementById('entity-modal')) kill();
  }, true);

  // Keep Save gated to required fields only
  document.addEventListener('input', function(e){
    var form = e.target && e.target.closest && e.target.closest('#entity-form');
    if (!form) return;
    var btn = document.getElementById('modal-save-btn');
    if (!btn) return;
    var ok = true;
    form.querySelectorAll('[required]').forEach(function(el){
      if (el.type === 'checkbox' || el.type === 'radio'){
        var group = form.querySelectorAll('[name="'+el.name+'"]');
        if (![...group].some(x=>x.checked)) ok = false;
      } else if (!String(el.value||'').trim()) ok = false;
    });
    btn.disabled = !ok;
  }, true);

})();