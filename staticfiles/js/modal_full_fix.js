/* modal_full_fix.js — one-file modal behavior replacement
   Goals:
   - Prevent UserProfile modal reappearing after close
   - Only one Close button (header)
   - Footer has Close + Save like other forms (handled by template)
   - Save disabled until required fields valid
*/
(function(){
  'use strict';

  // --- Utilities ---
  var doc = document;
  function $(s, c){ return (c||doc).querySelector(s); }
  function $all(s, c){ return Array.prototype.slice.call((c||doc).querySelectorAll(s)); }
  function remove(n){ if(n && n.parentNode) n.parentNode.removeChild(n); }

  // --- Global state ---
  var BUSY = false;
  var lastCloseAt = 0;
  var SILENCE_MS = 600;
  var escHandler = null;

  // --- Core teardown ---
  function teardown(){
    BUSY = false;
    lastCloseAt = Date.now();
    try{ doc.body.removeAttribute('inert'); }catch(_){}
    if (escHandler){ window.removeEventListener('keydown', escHandler); escHandler=null; }
    remove($('#entity-modal'));
    remove($('#modal-backdrop'));
    // kill any legacy overlays
    $all('.modal-backdrop,.lightbox-backdrop').forEach(remove);
  }

  // Expose close
  window.closeEntityModal = function(forceRefresh){
    teardown();
    if (forceRefresh && typeof window.reloadCurrentGrid === 'function'){
      try{ window.reloadCurrentGrid(); }catch(_){}
    }
  };

  // Install ESC-to-close after each open
  function installEsc(){
    if (escHandler) return;
    escHandler = function(e){ if (e.key === 'Escape') window.closeEntityModal(false); };
    window.addEventListener('keydown', escHandler);
  }

  // --- Guarded wrappers for open/edit ---
  function guard(fn){
    return function(){
      var now = Date.now();
      if (now - lastCloseAt < SILENCE_MS) return; // ignore accidental reopen
      teardown(); // always start clean
      if (BUSY) return;
      BUSY = true;
      try { return fn.apply(this, arguments); }
      finally { BUSY = false; setTimeout(postOpen, 0); }
    };
  }

  if (typeof window.openEntityModal === 'function'){
    window.openEntityModal = guard(window.openEntityModal);
  }
  if (typeof window.editEntity === 'function'){
    window.editEntity = guard(window.editEntity);
  }

  // Close before any nav click handler triggers
  doc.addEventListener('click', function(e){
    var t = e.target.closest && e.target.closest('a,button,[data-nav],[data-entity],[data-action]');
    if (!t) return;
    if ($('#entity-modal')) teardown();
  }, true);

  // --- After modal HTML is injected ---
  function postOpen(){
    var modal = $('#entity-modal');
    if (!modal) return;

    // Ensure single Close in header; hide others
    var headerClose = modal.querySelector('.modal-header .close-btn, .modal-header .modal-close');
    if (!headerClose){
      var h = modal.querySelector('.modal-header');
      if (h){
        var b = doc.createElement('button');
        b.type = 'button'; b.className = 'close-btn'; b.textContent = '✕';
        b.addEventListener('click', function(){ window.closeEntityModal(false); }, { once: true });
        h.appendChild(b);
      }
    }
    $all('.modal-body .close-btn, .modal-footer .close-btn, .modal-body .modal-close, .modal-footer .modal-close', modal)
      .forEach(function(n){ n.style.display='none'; });

    // Wire footer buttons
    var cancel = modal.querySelector('.modal-footer .btn.btn-secondary');
    if (cancel){
      cancel.addEventListener('click', function(){ window.closeEntityModal(false); }, { once: true });
    }
    var saveBtn = $('#modal-save-btn', modal);

    // Required-only gating
    function gate(){
      if (!saveBtn) return;
      var form = $('#entity-form', modal);
      if (!form){ saveBtn.disabled = true; return; }
      var ok = true;
      $all('[required]', form).forEach(function(el){
        if (el.type === 'checkbox' || el.type === 'radio'){
          var any = $all('[name="'+el.name+'"]', form).some(function(x){ return x.checked; });
          if (!any) ok = false;
        } else if (!String(el.value||'').trim()){ ok = false; }
      });
      saveBtn.disabled = !ok;
    }
    var form = $('#entity-form', modal);
    if (form){
      form.addEventListener('input', gate);
      form.addEventListener('change', gate);
      // Enter submits except textarea
      form.addEventListener('keydown', function(e){
        if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA'){
          e.preventDefault();
          if (typeof window._modalSave === 'function') window._modalSave();
        }
      });
      // initial
      setTimeout(gate, 0);
    }

    // Aadhaar and phone validation hooks preserved
    function markInvalid(input, msg){
      if (!input) return;
      input.classList.add('is-invalid');
      if (!input.parentElement.querySelector('.small-error')){
        var d = doc.createElement('div');
        d.className = 'text-danger small-error';
        d.textContent = msg || 'Invalid value.';
        input.parentElement.appendChild(d);
      }
    }
    function formatAadhaarPretty(v){
      var d=(v||'').replace(/\D/g,'').slice(0,12);
      return d.replace(/(\d{4})(\d{0,4})(\d{0,4}).*/,function(_,a,b,c){return [a,b,c].filter(Boolean).join(' ');});
    }
    function isValidAadhaar(num12){
      if(!/^\d{12}$/.test(num12)) return false;
      var d=[[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,0,6,7,8,9,5],[2,3,4,0,1,7,8,9,5,6],[3,4,0,1,2,8,9,5,6,7],[4,0,1,2,3,9,5,6,7,8],[5,9,8,7,6,0,4,3,2,1],[6,5,9,8,7,1,0,4,3,2],[7,6,5,9,8,2,1,0,4,3],[8,7,6,5,9,3,2,1,0,4],[9,8,7,6,5,4,3,2,1,0]];
      var p=[[0,1,2,3,4,5,6,7,8,9],[1,5,7,6,2,8,3,0,9,4],[5,8,0,3,7,9,6,1,4,2],[8,9,1,6,0,4,3,5,2,7],[9,4,5,3,1,2,6,8,7,0],[4,2,8,6,5,7,3,9,0,1],[2,7,9,3,8,0,6,4,1,5],[7,0,4,6,9,1,3,2,5,8]];
      var c=0, r=num12.split('').reverse().map(Number);
      for (var i=0;i<r.length;i++){ c = d[c][p[i%8][r[i]]]; }
      return c===0;
    }
    $all('input[name="aadhar"], input[name="adharno"]', form).forEach(function(inp){
      inp.classList.add('aadhar-input');
      inp.setAttribute('maxlength','14');
      inp.setAttribute('inputmode','numeric');
      inp.setAttribute('pattern','\\d{4}\\s\\d{4}\\s\\d{4}');
      inp.addEventListener('input', function(e){
        var c=e.target; var prev=c.selectionStart;
        c.value = formatAadhaarPretty(c.value);
        try{ c.setSelectionRange(prev, prev); }catch(_){}
        gate();
      });
      inp.addEventListener('blur', function(e){
        var v=e.target.value.replace(/\s/g,'');
        if(v && !isValidAadhaar(v)){ markInvalid(e.target,'Invalid Aadhaar number.'); }
      });
    });
    $all('input[name="phone"], input[name="mobile"], input[name="contact1"], input[name="contactno"], input[name="housecontactno"]', form).forEach(function(inp){
      inp.setAttribute('maxlength','10');
      inp.setAttribute('inputmode','numeric');
      inp.addEventListener('input', function(e){ e.target.value=e.target.value.replace(/\D/g,'').slice(0,10); gate(); });
      inp.addEventListener('blur', function(e){ if(e.target.value && !/^\d{10}$/.test(e.target.value)){ markInvalid(e.target,'Phone must be exactly 10 digits.'); } });
    });

    // default status/active hidden true
    ['status','is_active','active'].forEach(function(name){
      var el = form && form.querySelector('[name="'+name+'"]');
      if (!el) return;
      if (name==='status'){
        if (el.tagName==='SELECT'){
          var opt = Array.from(el.options).find(function(o){return /^(active|1|true)$/i.test(String(o.value));});
          if (opt) el.value = opt.value;
        } else el.value='active';
      } else {
        if (el.type==='checkbox') el.checked=true; else el.value='1';
      }
      var wrap = el.closest('.mb-3, .col-md-6, .form-group') || el.parentElement;
      if (wrap) wrap.style.display='none';
    });

    // ESC ready
    installEsc();
  }

  // When template is delivered with inline script, run postOpen once
  if (doc.readyState !== 'loading') setTimeout(postOpen, 0);
  else doc.addEventListener('DOMContentLoaded', function(){ setTimeout(postOpen, 0); });

})();