/* Extracted from script.js — app.core.js */
/* ====== ADMIN APP CORE (stable APIs, with targeted fixes) ====== */
(function () {
  // tiny helpers
  const qs  = (s, r=document) => r.querySelector(s);
  const qsa = (s, r=document) => Array.from(r.querySelectorAll(s));
  const on  = (t, s, h, o=false) => document.addEventListener(t, e => {
    const m = s ? e.target.closest(s) : e.target; if (!m) return; h(e, m);
  }, o);
  const addStyleOnce = (id, css) => { if (qs('#'+id)) return; const s=document.createElement('style'); s.id=id; s.textContent=css; document.head.appendChild(s); };
  const isJsonCt = r => ((r && r.headers && (r.headers.get('content-type')||'').toLowerCase().includes('application/json')));

  // date selector shared
  const DATE_SEL = [
    "input.date-field",
    'input[placeholder="dd/mm/yyyy"]',
    'input[placeholder="DD/MM/YYYY"]',
    "input[data-type='date']",
    "input[name*='date']",
    "input[name*='dob']"
  ].join(",");

  // globals
  window.__OPEN_MODAL_BUSY = window.__OPEN_MODAL_BUSY || {};
  window.__HARD_NAV_ISSUED = false;
  window.__MODAL_LOADING   = false;
  window.__MODAL_GOT_RESPONSE = false;
  window.__FETCH_TIMEOUT_MS = window.__FETCH_TIMEOUT_MS || 30000;

  // ===== CSS guards =====
  function ensureSidebarClickCSS(){
    addStyleOnce("force-sidebar-open-css", `
      .sidebar .dropdown.open > .dropdown-menu{display:block!important;}
      .sidebar .dropdown > a{cursor:pointer}
    `);
  }
  function ensureFormLayoutCSS(){
    addStyleOnce("no-scroll-grid-form-css", `
      #entity-modal{align-items:flex-start;overflow-y:auto}
      #entity-modal .modal-content{max-height:none!important}
      #entity-modal .modal-body{max-height:none!important;overflow:visible!important}
      #entity-modal .modal-body form{display:grid;grid-template-columns:repeat(2,minmax(260px,1fr));gap:12px 24px}
      #entity-modal .modal-body form .form-group,#entity-modal .modal-body form .form-row,#entity-modal .modal-body form fieldset,#entity-modal .modal-body form .field,#entity-modal .modal-body form .input-group{break-inside:avoid;page-break-inside:avoid}
      .checkbox-grid{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:flex-start}
      .checkbox-grid .form-check,.checkbox-grid label,.checkbox-grid .form-check-label{display:inline-flex;align-items:center;gap:6px;width:calc(50% - 16px)}
      #entity-modal select[multiple]{min-height:140px}
      .invalid{outline:2px solid #e00!important;background:#fff5f5}.save-disabled{opacity:.6;pointer-events:none}
      @media (max-width:768px){#entity-modal .modal-body form{grid-template-columns:1fr}.checkbox-grid .form-check,.checkbox-grid label,.checkbox-grid .form-check-label{width:100%}}
    `);
    addStyleOnce("entity-btn-visibility", `
      .btn-add,.btn-edit,.btn-delete,[data-open-entity],[data-edit-entity],[data-delete-entity]{visibility:visible!important;pointer-events:auto!important}
    `);
  }
  function ensureModalCloseCSS(){
    addStyleOnce("close-btn-clickable-css", `
      .modal .close-btn,.modal .btn-close,.modal [data-dismiss="modal"],.modal button.close,.modal .close{
        position:absolute;right:10px;top:8px;cursor:pointer;z-index:1001;pointer-events:auto;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
      }
      .modal{pointer-events:auto}
    `);
  }

  // ===== Image Preview Modal with hard overlay fix =====
  function ensureImagePreviewModal(){
    if (qs("#image-preview-modal")) return;
    addStyleOnce("image-preview-overlay-css", `
      body.image-modal-open{overflow:hidden}
      #image-preview-modal{background:transparent!important;z-index:2147483000;position:fixed;inset:0;display:none;align-items:center;justify-content:center}
      #image-preview-modal .modal-content.image-modal{box-shadow:0 8px 24px rgba(0,0,0,.18);z-index:2147483646;max-width:min(96vw,900px);width:100%}
      #image-preview-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:2147483600;display:none}
    `);
    const backdrop = document.createElement("div");
    backdrop.id="image-preview-backdrop";
    document.body.appendChild(backdrop);

    const m = document.createElement("div");
    m.id="image-preview-modal"; m.className="modal"; m.style.display="none";
    m.innerHTML = `
      <div class="modal-content image-modal" style="background:#fff;">
        <div class="modal-header d-flex justify-content-between align-items-center mb-2">
          <h5 class="modal-title">Image Preview</h5>
          <button type="button" class="close-btn" data-close-image>&times;</button>
        </div>
        <div class="modal-body" role="dialog" aria-modal="true">
          <div id="image-spinner" style="text-align:center;margin:0 0 12px 0;display:none;">Loading…</div>
          <img id="image-preview" src="" alt="Preview" style="max-width:100%;max-height:70vh;display:none;margin:0 auto 12px;background:transparent;">
          <div id="image-meta-fields"></div>
          <div class="d-flex justify-content-end mt-3"><button class="btn btn-secondary" data-close-image>Close</button></div>
        </div>
      </div>`;
    document.body.appendChild(m);

    // close wiring stays inside modal only
    on("click", "#image-preview-modal [data-close-image], #image-preview-backdrop", ()=> closeImageModal());
  }

  // ===== Auth + CSRF =====
  function getCookie(name){
    let v=null; if (!document.cookie) return v;
    for (let c of document.cookie.split(";")){ c=c.trim(); if (c.startsWith(name+"=")){ v=decodeURIComponent(c.substring(name.length+1)); break; } }
    return v;
  }
  function getCsrfTokenSafe(){
    const el = qs('#entity-form input[name="csrfmiddlewaretoken"]') ||
               qs('form input[name="csrfmiddlewaretoken"]') ||
               qs('input[name="csrfmiddlewaretoken"]') ||
               qs('meta[name="csrf-token"]');
    return el ? (el.content || el.value || '') : (getCookie('csrftoken') || '');
  }
  function showInlineLoginError(msg){
    const d = qs("#login-error"); if (!d) { alert(msg||"Invalid credentials."); return; }
    d.textContent = msg || "Invalid credentials."; d.hidden=false; d.style.display="block"; d.setAttribute("role","alert"); d.setAttribute("aria-live","assertive");
  }
  function handleAuthFailure(msg){
    if (typeof window.openLoginModal === "function") window.openLoginModal();
    showInlineLoginError(msg || "Not authenticated.");
    try{ console.warn("Auth required"); }catch(_){}
  }

  // ===== Abortable fetch with timeout =====
  let __modalAbortController = null;
  function fetchWithTimeout(url, options={}, timeoutMs){
    const ms = timeoutMs || window.__FETCH_TIMEOUT_MS;
    const controller = new AbortController(); const merged = { keepalive:true, ...options, signal: controller.signal };
    __modalAbortController = controller;
    const t = setTimeout(()=>{ try{controller.abort();}catch(_){} }, ms);
    return fetch(url, merged).finally(()=>{ clearTimeout(t); if (__modalAbortController===controller) __modalAbortController=null; });
  }
  function abortInFlight(){ try{ __modalAbortController?.abort(); }catch(_){} __modalAbortController=null; }
  function abortModal(message){
    abortInFlight();
    try{ closeEntityModal(); }catch(_){}
    if (window.__HARD_NAV_ISSUED || window.__SUPPRESS_TIMEOUT_ALERTS || document.visibilityState!=="visible") return;
    alert(message || "Request timed out. Please try again.");
  }

  // ===== Password eye =====
  function addEyeCSSGuard(){
    addStyleOnce("eye-guard-style", `
      .pro-passwrap :is([data-toggle-pass],.eye-icon,.toggle-password,.js-eye,[data-toggle="password"]){display:inline-flex;align-items:center;justify-content:center}
      .pro-passwrap :is([data-toggle-pass],.eye-icon,.toggle-password,.js-eye,[data-toggle="password"]):not(:first-of-type){display:none!important;visibility:hidden!important;pointer-events:none!important}
    `);
  }
  function reMaskPasswords(scope=document){
    qsa('input.password-input, input[type="text"].password-input, .pro-passwrap input[type="text"][autocomplete="new-password"], .pro-passwrap input[type="text"][data-password]', scope)
      .forEach(inp=>{ try{ inp.type='password'; }catch(_){}});
  }
  function setupGlobalEyeToggles(){
    on("click", ".js-eye,[data-toggle='password'],.toggle-password,.eye-icon,[data-toggle-pass]", (e, btn)=>{
      e.preventDefault();
      const wrap = btn.closest(".pro-passwrap") || btn.closest(".input-group") || btn.parentElement;
      const selRaw = btn.getAttribute("data-target") || btn.getAttribute("aria-controls");
      let input = selRaw ? qs(selRaw.startsWith("#")? selRaw : "#"+selRaw.replace(/^#/,"")) : null;
      if (!input && wrap) input = wrap.querySelector("input[type='password'], input[type='text'].password, input[type='text'][data-password], input.password-input");
      if (!input) return;
      input.type = (input.type === "password" ? "text" : "password");
      btn.dataset.visible = String(input.type==="text");
    });
  }
  function wirePasswordEyes(root=document){
    const scope = root || document, TOGGLE_SEL = ".js-eye,[data-toggle='password'],.toggle-password,.eye-icon,[data-toggle-pass]";
    const isDecoyOrHidden = inp => {
      if (inp.matches('[autocomplete="current-password"], [tabindex="-1"], [aria-hidden="true"]')) return true;
      const s = getComputedStyle(inp); if (s.display==="none" || s.visibility==="hidden") return true;
      const r = inp.getBoundingClientRect(); if (r.width<=1 && r.height<=1) return true;
      if (r.right<0 || r.bottom<0 || r.top>(innerHeight||0) || r.left>(innerWidth||0)) return true;
      return false;
    };
    qsa('input[type="password"]', scope).forEach(inp=>{
      if (inp.dataset.eyeWired==="1") return;
      if (isDecoyOrHidden(inp)) { inp.dataset.eyeWired="1"; return; }
      let container = inp.closest('.pro-passwrap') || inp.closest('.input-group') || inp.closest('.form-group') || inp.parentElement;
      if (!inp.closest('.pro-passwrap')) {
        const wrap = document.createElement("div"); wrap.className="pro-passwrap"; inp.parentNode.insertBefore(wrap, inp); wrap.appendChild(inp); container = wrap;
      } else { container = inp.closest('.pro-passwrap'); }
      if (container.querySelector(TOGGLE_SEL)) { inp.dataset.eyeWired="1"; return; }
      if (!inp.id) inp.id = "pw_" + Math.random().toString(36).slice(2);
      const btn = document.createElement("button"); btn.type="button"; btn.className="eye-icon"; btn.setAttribute("aria-label","Toggle password visibility");
      btn.setAttribute("aria-controls", "#"+inp.id); btn.dataset.visible="false";
      Object.assign(btn.style,{position:"absolute",right:"8px",top:"50%",transform:"translateY(-50%)",border:"none",background:"transparent",cursor:"pointer",padding:"4px",lineHeight:"1"});
      container.appendChild(btn); inp.dataset.eyeWired="1";
    });
    dedupePasswordEyes(scope);
  }
  function dedupePasswordEyes(root=document){
    const scope = root || document, TOGGLE_SEL = ".js-eye,[data-toggle='password'],.toggle-password,.eye-icon,[data-toggle-pass]";
    qsa('input[type="password"], input[type="text"].password, input[type="text"][data-password], input.password-input', scope).forEach(inp=>{
      const c = inp.closest('.pro-passwrap') || inp.closest('.input-group') || inp.closest('.form-group') || inp.parentElement; if (!c) return;
      const t = qsa(TOGGLE_SEL, c); if (t.length<=1) return;
      const keep = t.find(b => b.matches('[data-toggle-pass]')) || t.find(b => b.previousElementSibling===inp || b.nextElementSibling===inp) || t[0];
      t.forEach(b=>{ if (b!==keep) b.remove(); });
    });
    qsa('.toggle-password, .password-eye, .show-pass', scope).forEach(el=>{ if (!el.closest('.pro-passwrap')) el.remove(); });
  }
  let _eyeObserverStarted=false;
  function startEyeObserver(){
    if (_eyeObserverStarted) return; _eyeObserverStarted=true;
    const enforce = (node)=>{ if (!node?.querySelectorAll) return; wirePasswordEyes(node); dedupePasswordEyes(node); reMaskPasswords(node); };
    const mo = new MutationObserver(muts=>{
      let touched=false;
      for (const m of muts){
        if (m.type==="childList"){
          m.addedNodes.forEach(n=>{ if (n.nodeType===1 && (n.matches?.('input[type="password"], .pro-passwrap, form') || n.querySelector?.('input[type="password"], .pro-passwrap'))) { touched=true; enforce(n); } });
        } else if (m.type==="attributes" && m.target?.matches?.('input[type="password"]')) { touched=true; enforce(m.target.closest('.pro-passwrap')||m.target.parentElement||document); }
      }
      if (!touched && muts.length>10) enforce(document);
    });
    mo.observe(document.documentElement||document.body,{childList:true,subtree:true,attributes:true,attributeFilter:["class","type"]});
    setTimeout(()=>{ wirePasswordEyes(document); dedupePasswordEyes(document); reMaskPasswords(document); },0);
  }

  // ===== Expose core helpers
  window.qs = window.qs || qs;
  window.qsa = window.qsa || qsa;
  window.on = window.on || on;
  window.addStyleOnce = addStyleOnce;
  window.isJsonCt = isJsonCt;
  window.DATE_SEL = DATE_SEL;
  window.getCsrfTokenSafe = getCsrfTokenSafe;
  window.fetchWithTimeout = fetchWithTimeout;
  window.abortModal = abortModal;
  window.abortInFlight = abortInFlight;
  window.showInlineLoginError = showInlineLoginError;

  window.addEyeCSSGuard = addEyeCSSGuard;
  window.setupGlobalEyeToggles = setupGlobalEyeToggles;
  window.wirePasswordEyes = wirePasswordEyes;
  window.dedupePasswordEyes = dedupePasswordEyes;
  window.reMaskPasswords = reMaskPasswords;
  window.startEyeObserver = startEyeObserver;

  function ensureModalCloseCSSGuard(){ ensureModalCloseCSS(); } // alias
  window.ensureSidebarClickCSS = ensureSidebarClickCSS;
  window.ensureFormLayoutCSS   = ensureFormLayoutCSS;
  window.ensureModalCloseCSS   = ensureModalCloseCSS;
  window.ensureModalCloseCSSGuard = ensureModalCloseCSSGuard;
  window.ensureImagePreviewModal = ensureImagePreviewModal;

  // DOM READY boot
  document.addEventListener("DOMContentLoaded", function () {
    ensureSidebarClickCSS();
    ensureImagePreviewModal();
    ensureFormLayoutCSS();
    ensureModalCloseCSS();

    addEyeCSSGuard();
    setupGlobalEyeToggles();
    wirePasswordEyes(document);
    dedupePasswordEyes(document);
    reMaskPasswords(document);
    startEyeObserver();
  });
})();
