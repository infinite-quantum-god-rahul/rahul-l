/* modal_core.js — safe modal lifecycle, no external deps */
(function () {
  'use strict';

  // Global state
  var BUSY = false;
  var ESC_HANDLER = null;

  function $(sel, ctx){ return (ctx||document).querySelector(sel); }
  function $all(sel, ctx){ return Array.prototype.slice.call((ctx||document).querySelectorAll(sel)); }

  function removeNode(n){ if(n && n.parentNode){ n.parentNode.removeChild(n); } }

  function unlockBody(){
    try { document.body.removeAttribute('inert'); } catch(_){}
  }

  function teardownModal(){
    BUSY = false;
    unlockBody();
    if (ESC_HANDLER){ window.removeEventListener('keydown', ESC_HANDLER); ESC_HANDLER = null; }
    removeNode($('#entity-modal'));
    removeNode($('#modal-backdrop'));
    // defensive: clear any stray overlays
    $all('.lightbox-backdrop,.modal-backdrop').forEach(removeNode);
  }

  // Expose close for template buttons
  window.closeEntityModal = function(forceRefresh){
    teardownModal();
    // Optional grid refresh hook
    if (forceRefresh && typeof window.reloadCurrentGrid === 'function'){
      try { window.reloadCurrentGrid(); } catch(_){}
    }
  };

  // Wrap existing open/edit to guarantee clean slate before every show
  var _origOpen = window.openEntityModal;
  window.openEntityModal = function(entity){
    if (BUSY) return;
    BUSY = true;
    teardownModal();
    try { if (typeof _origOpen === 'function') _origOpen(entity); } finally { BUSY = false; }
  };

  var _origEdit = window.editEntity;
  window.editEntity = function(entity, pk){
    if (BUSY) return;
    BUSY = true;
    teardownModal();
    try { if (typeof _origEdit === 'function') _origEdit(entity, pk); } finally { BUSY = false; }
  };

  // One-time global nav guard: any primary nav click closes modal first
  document.addEventListener('click', function(e){
    var t = e.target.closest('a,button,[data-nav],[data-entity],[data-action]');
    if (!t) return;
    if (!$('#entity-modal')) return;
    teardownModal();
  }, true);

  // Provide an ESC handler installer that template code can reuse
  window.__installEscToClose = function(){
    if (ESC_HANDLER) return;
    ESC_HANDLER = function(e){ if (e.key === 'Escape'){ window.closeEntityModal(false); } };
    window.addEventListener('keydown', ESC_HANDLER);
  };

  // De-dupe any accidental duplicate Close buttons inserted elsewhere
  function dedupeCloses(){
    var modal = $('#entity-modal'); if (!modal) return;
    var closes = $all('.close-btn, .modal-close, [data-dismiss="modal"]', modal);
    if (closes.length <= 1) return;
    // Keep the first appearance in header
    for (var i=1;i<closes.length;i++) removeNode(closes[i]);
  }

  // Run de-dupe shortly after DOM mutations inside the modal
  var mo = new MutationObserver(function(){
    dedupeCloses();
  });
  var startMO = function(){
    var m = $('#entity-modal');
    if (!m) return;
    try { mo.disconnect(); mo.observe(m, { childList: true, subtree: true }); } catch(_){}
    dedupeCloses();
  };
  document.addEventListener('DOMContentLoaded', startMO);
  document.addEventListener('click', function(){ setTimeout(startMO, 0); });

  // Export for template hook
  window.__modalCore = {
    teardownModal: teardownModal,
    startObserver: startMO
  };
})();
