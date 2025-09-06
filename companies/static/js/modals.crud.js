


/* Extracted from script.js — app.modals.js */
/* ====== MODALS, ROUTING, ENTITY CRUD (UserProfile hard-nav + stable) ====== */
(function(){
  const qs  = window.qs  || ((s, r=document) => r.querySelector(s));
  const qsa = window.qsa || ((s, r=document) => Array.from(r.querySelectorAll(s)));
  const on  = window.on  || ((t, s, h, o=false) => document.addEventListener(t, e => { const m = s ? e.target.closest(s) : e.target; if (!m) return; h(e, m); }, o));

  let __FALLBACK_TIMER = null;
  window.__CANCEL_MODAL = false;
  const __DISABLE_ROUTER = !!(window.DISABLE_ENTITY_MODAL_ROUTER);

  function forceOpenModalDisplay(){ addStyleOnce('modal-force-open-style', '#entity-modal.force-open{display:flex!important}'); }
  function ensureModalSkeleton(){
    if (qs("#entity-modal")) return;
    const m = document.createElement("div"); m.id="entity-modal"; m.className="modal"; m.style.display="none";
    m.innerHTML = `
      <div class="modal-content">
        <div class="modal-header" style="margin-bottom:12px;">
          <h5 id="entity-modal-title" class="modal-title"></h5>
          <button type="button" class="close-btn" onclick="closeEntityModal()">&times;</button>
        </div>
        <div class="modal-body">
          <div id="form-errors" role="alert" aria-live="assertive"></div>
          <div id="entity-modal-body"></div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" onclick="closeEntityModal()">Close</button>
          <button id="modal-save-btn" class="btn btn-primary save-disabled" disabled>Save</button>
        </div>
      </div>`;
    document.body.appendChild(m);
  }
  function openLoadingShell(title){
    forceOpenModalDisplay(); ensureModalSkeleton();
    window.__CANCEL_MODAL = false;
    const modal=qs("#entity-modal"), titleEl=qs("#entity-modal-title"), body=qs("#entity-modal-body");
    if (modal && titleEl && body){ titleEl.innerText = title || "Loading"; body.innerHTML = '<div style="padding:8px;">Loading…</div>'; modal.classList.add("force-open"); modal.style.display="flex"; }
  }
  function prettyName(s){ return String(s||"").replace(/_/g," ").replace(/\b\w/g, c=>c.toUpperCase()); }
  function getEntityBase(entity){ const seg=String(entity||"").replace(/\s+/g,""); return `/${encodeURIComponent(seg.toLowerCase())}/`; }
  function applyCheckboxGrid(root){
    try{
      const scope = root || document, set=new Set();
      qsa('input[type="checkbox"], input[type="radio"], .perm-checkbox', scope).forEach(inp=>{
        const c = inp.closest('.form-group') || inp.closest('fieldset') || (inp.closest('.form-check') && inp.closest('.form-check').parentElement) || inp.parentElement;
        if (c) set.add(c);
      }); set.forEach(c=> c.classList.add('checkbox-grid'));
    }catch(e){ console.warn("applyCheckboxGrid:", e); }
  }
  function replaceModalWithHTML(html){
    window.__MODAL_GOT_RESPONSE = true;
try{ __markModalResponse && __markModalResponse(); }catch(_){ }
try{ __markModalResponse(); }catch(_){ }

    window.__MODAL_GOT_RESPONSE = true;

    if (window.__CANCEL_MODAL) return;
    const tmp=document.createElement("div"); tmp.innerHTML=html.trim();
    const fresh = tmp.querySelector("#entity-modal");
    const old = qs("#entity-modal"); if (old) old.remove();
    if (fresh){ document.body.appendChild(fresh); } else {
      ensureModalSkeleton(); qs("#entity-modal-body").innerHTML = html;
    }
    const m = qs("#entity-modal"); if (m){ m.style.display="flex"; m.classList.add("force-open"); }
    window.__HARD_NAV_ISSUED = false;
    window.__MODAL_LOADING   = false;
    ensureFormLayoutCSS(); applyCheckboxGrid(qs("#entity-modal")||document);
    initializeDatePickers(); setupPermissionSelectAll(); formatDateFields(); addMasks(); initPhoneInputs();
    ensureFormErrorBox(); window.setupSaveButtonHandler();
    const f=qs("#entity-form"), b=qs("#modal-save-btn"); prepareFormValidation(f,b);
    wirePasswordEyes(qs("#entity-modal")); dedupePasswordEyes(qs("#entity-modal")); reMaskPasswords(qs("#entity-modal"));
  }

  function fillAutoCode(entity){
    let t = qs('#entity-form input[name="code"]') ||
            qs('#entity-form input[name="voucher_no"]') ||
            qs('#entity-form input[name="smtcode"]') ||
            qs('#entity-form input[name="empcode"]') ||
            qs('#entity-form input[name="staffcode"]') ||
            qs('#entity-form input[name="VCode"]');
    if (!t || t.value) return;
    const seg = String(entity||"").replace(/\s+/g,"").toLowerCase();
    fetch("/next_code/", {
      method:"POST",
      headers:{"X-CSRFToken":getCsrfTokenSafe(),"X-Requested-With":"XMLHttpRequest","Content-Type":"application/x-www-form-urlencoded","Accept":"application/json"},
      body:`entity=${encodeURIComponent(seg)}`, credentials:"include", keepalive:true
    }).then(r=>r.json()).then(d=>{ if (d.code && t && !t.value) t.value=d.code; }).catch(e=> console.error("code-fetch:", e));
  }

  function insertEntityModal(entity, html, mode, id, baseOverride){
    window.__MODAL_GOT_RESPONSE = true;
try{ __markModalResponse && __markModalResponse(); }catch(_){ }
try{ __markModalResponse(); }catch(_){ }

    window.__MODAL_GOT_RESPONSE = true;

    if (window.__CANCEL_MODAL) return;
    const base = baseOverride || getEntityBase(entity);
    const tmp=document.createElement("div"); tmp.innerHTML=html.trim();
    const ret = tmp.querySelector("#entity-modal");
    const exist = qs("#entity-modal"); if (exist) exist.remove();
    if (ret){ document.body.appendChild(ret); } else { ensureModalSkeleton(); qs("#entity-modal-body").innerHTML = html; }
    const modal = qs("#entity-modal"); if (modal){ modal.style.display="flex"; modal.classList.add("force-open"); }
    const titleEl=qs("#entity-modal-title"); if (titleEl) titleEl.innerText = `${mode} ${prettyName(entity)}`;
    const form=qs("#entity-form"); if (form){ form.dataset.entity=entity; form.action = mode==="Create" ? `${base}create/` : `${base}update/${String(id||"").replace(/^:/,"")}/`; }
    window.__HARD_NAV_ISSUED = false;
    window.__MODAL_LOADING   = false;
    ensureFormErrorBox(); ensureFormLayoutCSS(); applyCheckboxGrid(qs("#entity-modal")||document);
    initializeDatePickers(); setupPermissionSelectAll(); formatDateFields(); addMasks(); initPhoneInputs(); fillAutoCode(entity);
    window.setupSaveButtonHandler(); const f=qs("#entity-form"), b=qs("#modal-save-btn"); prepareFormValidation(f,b);
    wirePasswordEyes(qs("#entity-modal")); dedupePasswordEyes(qs("#entity-modal")); reMaskPasswords(qs("#entity-modal"));
  }

  // find embedded HTML in JSON payloads
  function deepFindHtml(obj, depth=0){
    if (!obj || depth>4) return "";
    if (typeof obj === "string"){
      if (/<form[\s>]/i.test(obj) || /id=["']entity-modal["']/.test(obj)) return obj;
      return "";
    }
    if (Array.isArray(obj)){
      for (const it of obj){ const got = deepFindHtml(it, depth+1); if (got) return got; }
      return "";
    }
    if (typeof obj === "object"){
      const keys = Object.keys(obj);
      const priority = keys.filter(k=>/html|body|template|content/i.test(k));
      for (const k of [...priority,...keys]){
        const got = deepFindHtml(obj[k], depth+1); if (got) return got;
      }
    }
    return "";
  }

  async function tryFetch(url, opts){ try{ return await fetchWithTimeout(url, opts); }catch(e){ return null; } }

  function buildTryUrls(mode, entity, id){
    const raw = String(entity).replace(/\s+/g,"");
    const baseLower = `/${encodeURIComponent(raw.toLowerCase())}/`;
    const idClean   = String(id||"").replace(/^:/,'');
    const q = `_=${Date.now()}`;
    const qsOpts = ["", "?partial=1", "?modal=1", "?format=partial", "?ajax=1"].map(s=> s+(s?("&"+q):("?"+q)));
    const list = [];

    // Always use lowercase URLs for consistency
    if (mode==="Create"){
      qsOpts.forEach(qs=> list.push(baseLower+"get/"+qs));
    }else{
      qsOpts.forEach(qs=> list.push(`${baseLower}get/${encodeURIComponent(idClean)}/${qs}`));
    }
    
    return { list, baseLower, baseLower };
  }

  function loadEntityForm(mode, entity, id){
    const { list, baseLower } = buildTryUrls(mode, entity, id);

    // Debug logging for UserProfile
    if (isUserProfileEntity(entity)) {
      console.log('=== UserProfile Modal Debug ===');
      console.log('Mode:', mode);
      console.log('Entity:', entity);
      console.log('URLs to try:', list);
      console.log('Base URL:', baseLower);
    }

  // guard: modal response arrived
  function __markModalResponse(){
    window.__MODAL_GOT_RESPONSE = true;
    if (typeof __FALLBACK_TIMER !== "undefined" && __FALLBACK_TIMER){
      try{ clearTimeout(__FALLBACK_TIMER); }catch(_){}
      __FALLBACK_TIMER = null;
    }
  }
const opts = { headers:{ "X-Requested-With":"XMLHttpRequest","Accept":"application/json,text/html,*/*","X-Partial":"1","X-Modal":"1" }, credentials:"include", cache:"no-store", redirect:"follow", keepalive:true };

    openLoadingShell(`${mode} ${prettyName(entity)}`);
    window.__MODAL_LOADING = true;
    window.__MODAL_GOT_RESPONSE = false;

    if (__FALLBACK_TIMER) { clearTimeout(__FALLBACK_TIMER); __FALLBACK_TIMER = null; }
    __FALLBACK_TIMER = setTimeout(()=>{
      if (window.__CANCEL_MODAL) return;
      if (window.__MODAL_LOADING && !window.__MODAL_GOT_RESPONSE && !qs("#entity-modal .modal-body form") && !window.__HARD_NAV_ISSUED){
        window.__HARD_NAV_ISSUED = true;
        window.location.href = (mode==="Create" ? `${baseLower}get/` : `${baseLower}update/${encodeURIComponent(String(id).replace(/^:/,''))}/`);
      }
    }, 3500);

    abortInFlight();
    return (async ()=>{
      for (const u of list){
        if (window.__CANCEL_MODAL) break;
        
        // Debug logging for UserProfile
        if (isUserProfileEntity(entity)) {
          console.log('Trying URL:', u);
        }
        
        const res = await tryFetch(u, opts);
        if (!res) {
          if (isUserProfileEntity(entity)) {
            console.log('Fetch failed for URL:', u);
          }
          continue;
        }
        
        if (isUserProfileEntity(entity)) {
          console.log('Response for URL:', u, 'Status:', res.status);
        }
        
        window.__MODAL_GOT_RESPONSE = true;
        if (res.status===401 || res.status===403 || res.redirected){ window.__MODAL_LOADING=false; handleAuthFailure("Not authenticated."); return; }
        if (res.status===404) {
          if (isUserProfileEntity(entity)) {
            console.log('404 for URL:', u);
          }
          continue;
        }
        if (isJsonCt(res)){
          const d=await res.json().catch(()=>null);
          if (d){
            if (isUserProfileEntity(entity)) {
              console.log('JSON response for UserProfile:', d);
            }
            const h = (d && typeof d==='object' && (d.html || d.body || d.template)) ? (d.html||d.body||d.template) : (typeof d==='string'?d:deepFindHtml(d));
            if (h){
              if (isUserProfileEntity(entity)) {
                console.log('Found HTML in JSON response, inserting modal');
              }
              insertEntityModal(entity, h, mode, id, baseLower); return;
            }
            if (d.success && d.html){
              if (isUserProfileEntity(entity)) {
                console.log('Found success response with HTML, inserting modal');
              }
              insertEntityModal(entity, d.html, mode, id, baseLower); return;
            }
          }
        }else{
          let t=await res.text().catch(()=> "");
          if (t && t.trim().startsWith("{")){
            try{ const j=JSON.parse(t); const h2=deepFindHtml(j); if (h2){ t=h2; } }catch(_){}
          }
          if (t){
            if (isUserProfileEntity(entity)) {
              console.log('Found text response, inserting modal. Length:', t.length);
            }
            insertEntityModal(entity, t, mode, id, baseLower); return;
          }
        }
      }
      window.__MODAL_LOADING=false;
      if (!window.__CANCEL_MODAL) alert(`${mode} form endpoint not found.`);
    })().catch(err=>{
      window.__MODAL_LOADING=false;
      if (err?.name==="AbortError"){ abortModal("Request timed out. Please try again."); return; }
      console.error(`${mode} load error:`, err); alert(`Failed to load ${mode.toLowerCase()} form. Opening full page…`);
      window.location.href = (mode==="Create" ? `${baseLower}get/` : `${baseLower}update/${encodeURIComponent(String(id).replace(/^:/,''))}/`);
    }).finally(()=>{ if (__FALLBACK_TIMER){ clearTimeout(__FALLBACK_TIMER); __FALLBACK_TIMER=null; } });
  }

  function isUserPermEntity(ent){ return /^userpermissions?$/i.test(String(ent||"")); }
  function isUserProfileEntity(ent){ return /^userprofile$/i.test(String(ent||"")); }
  function openEntityModal(entityOrEvent){
    let entity;
    if (typeof entityOrEvent==="string") entity=entityOrEvent;
    else if (entityOrEvent?.currentTarget){ const el=entityOrEvent.currentTarget; entity = el.dataset.entity || el.getAttribute("data-entity") || ""; }
    if (!entity){ console.error("No entity for openEntityModal"); return; }
    if (isUserPermEntity(entity)){ const onUP = /\/userpermissions?\/?$/i.test(location.pathname); if (!onUP){ window.location.href="/UserPermission/"; return; } }
    const key = String(entity).replace(/\s+/g,"").toLowerCase(); if (window.__OPEN_MODAL_BUSY[key]) return; window.__OPEN_MODAL_BUSY[key]=true; const clear=()=>{ try{ delete window.__OPEN_MODAL_BUSY[key]; }catch(_){}}; const timer=setTimeout(clear,window.__FETCH_TIMEOUT_MS);
    loadEntityForm("Create", entity).finally(()=>{ clearTimeout(timer); clear(); });
  }
  function editEntity(entity, id){
    if (!entity || !id){ console.error("editEntity requires entity and id"); return; }
    return loadEntityForm("Edit", entity, String(id).replace(/^:/,''));
  }
  function closeEntityModal(){
    window.__CANCEL_MODAL = true;
    if (__FALLBACK_TIMER){ clearTimeout(__FALLBACK_TIMER); __FALLBACK_TIMER=null; }
    abortInFlight();
    const m=qs("#entity-modal");
    if (m){ m.classList.remove("force-open"); m.style.display="none"; }
    window.__HARD_NAV_ISSUED=false; window.__MODAL_LOADING=false;
    try{ Object.keys(window.__OPEN_MODAL_BUSY||{}).forEach(k=> delete window.__OPEN_MODAL_BUSY[k]); }catch(_){}
  }

  // delete
  function getCurrentRole(){ try{ return (document.body?.dataset?.role||"").toLowerCase(); }catch(_){ return ""; } }
  function deleteEntity(entity, id){
    try {
      const confirmed = confirm("Are you sure you want to delete this item?");
      if (!confirmed) {
        return;
      }
      
      id = String(id).replace(/^:/,''); 
      const seg = String(entity).replace(/\s+/g,"").toLowerCase();
      
      const csrfToken = getCsrfTokenSafe();
      if (!csrfToken) {
        alert("CSRF token not found. Please refresh the page and try again.");
        return;
      }
      
      fetch(`/${encodeURIComponent(seg)}/delete/${encodeURIComponent(id)}/`,{
        method:"POST", 
        headers:{ 
          "X-CSRFToken":csrfToken,
          "X-Requested-With":"XMLHttpRequest",
          "Accept":"application/json" 
        }, 
        credentials:"include"
    }).then(async res=>{
      console.log("=== DELETE RESPONSE RECEIVED ===");
      console.log("Response status:", res.status);
      console.log("Response headers:", res.headers);
      console.log("Response redirected:", res.redirected);
      
      const ct=(res.headers.get("content-type")||"").toLowerCase();
      if (res.status===401){ handleAuthFailure("Not authenticated."); return; }
      if (res.status===403 || res.redirected){ handleAuthFailure("Not authenticated."); return; }
      if (ct.includes("application/json")){
        console.log("=== PROCESSING JSON RESPONSE ===");
        const d=await res.json();
        console.log("Response data:", d);
        if (d.success){ 
          console.log("Delete successful, reloading page");
          location.reload(); 
          return; 
        }
        const msg=String(d.error||"").toLowerCase();
        console.log("Error message:", msg);
        const tblMissing=/no such table|does not exist|undefinedtable/.test(msg); const limited=(seg==="userprofile"||seg==="hrpm");
        alert(tblMissing && limited ? "Table missing. Run migrations, then retry delete." : (d.error||"Delete failed.")); return;
      }
      console.log("=== PROCESSING NON-JSON RESPONSE ===");
      const t = await res.text().catch(()=> "");
      console.log("Response text:", t);
      if (res.status===403 && /csrf|forgery/i.test(t)) alert("CSRF validation failed or session expired. Refresh and try again.");
      else { alert("Server returned unexpected response while deleting."); console.error("Delete non-JSON:", t.slice(0,500)); }
    }).catch(err=>{ 
      console.log("=== DELETE REQUEST FAILED ===");
      console.error("Delete error:", err); 
      alert("Delete request failed. Check console."); 
    });
    } catch (error) {
      console.log("=== DELETE FUNCTION ERROR ===");
      console.error("Function error:", error);
      alert("Delete function error: " + error.message);
    }
  }

  // entity button normalization + router
  const ENTITY_BTN_SEL = "[data-open-entity],[data-edit-entity],[data-delete-entity],.btn-add,.btn-edit,.btn-delete,[id^='create-'][id$='-btn']";
  function ensureEntityButtonsEnabled(){
    qsa(ENTITY_BTN_SEL).forEach(el=>{
      el.removeAttribute?.("disabled");
      if (el.getAttribute?.("aria-disabled")==="true") el.setAttribute("aria-disabled","false");
      el.classList?.remove("disabled");
      if (el.style){ el.style.pointerEvents="auto"; el.style.visibility="visible"; if (el.style.display==="none") el.style.display=""; }
      el.removeAttribute?.("hidden");
      if (!el.hasAttribute?.("tabindex")) el.setAttribute?.("tabindex","0");
      if (!el.hasAttribute?.("role")) el.setAttribute?.("role", el.tagName==="A"?"link":"button");
    });
  }
  function normalizeEntityButtons(scope){
    if (__DISABLE_ROUTER) return;
    qsa("a[href^='/']", scope||document).forEach(el=>{
      const href = el.getAttribute?.("href"); if (!href) return;
      const mAdd  = href.match(/^\/([^\/]+)\/get\/?(\?.*)?$/i);
      const mEdit = href.match(/^\/([^\/]+)\/update\/([^\/]+)\/?(\?.*)?$/i);
      const mDel  = href.match(/^\/([^\/]+)\/delete\/([^\/]+)\/?(\?.*)?$/i);
      if (mAdd){
        const ent = mAdd[1];

        if (!el.dataset.openEntity) el.dataset.openEntity = ent;
        if (!el.dataset.entity) el.dataset.entity = ent;
        el.classList.add("btn-add");
      }
      else if (mEdit){ if (!el.dataset.editEntity) el.dataset.editEntity = mEdit[1]; if (!el.dataset.entity) el.dataset.entity = mEdit[1]; if (!el.dataset.id) el.dataset.id = mEdit[2]; el.classList.add("btn-edit"); }
      else if (mDel){ if (!el.dataset.deleteEntity) el.dataset.deleteEntity = mDel[1]; if (!el.dataset.entity) el.dataset.entity = mDel[1]; if (!el.dataset.id) el.dataset.id = mDel[2]; el.classList.add("btn-delete"); }
    });
  }

  // debounce observer
  (function observeButtons(){
    let normalizing = false;
    let scheduled = false;
    const run = ()=> {
      scheduled = false;
      if (normalizing) return;
      normalizing = true;
      try {
        normalizeEntityButtons(document);
        ensureEntityButtonsEnabled();
      } finally {
        normalizing = false;
      }
    };
    const mo = new MutationObserver((muts)=>{
      const hasAddRem = muts.some(m => m.type==="childList" && (m.addedNodes.length || m.removedNodes.length));
      const hasHrefChange = muts.some(m => m.type==="attributes" && m.attributeName==="href");
      if (!hasAddRem && !hasHrefChange) return;
      if (!scheduled) { scheduled = true; setTimeout(run, 50); }
    });
    mo.observe(document.documentElement||document.body,{childList:true,subtree:true,attributes:true,attributeFilter:["href"]});
    run();
  })();

  function getEntityFromElement(el){
    if (!el) return "";
    let e = el.dataset.openEntity || el.dataset.editEntity || el.dataset.deleteEntity || el.dataset.entity || el.getAttribute("data-entity") || "";
    if (e) return e;
    const idAttr = el.id||""; if (/^create-.+-btn$/i.test(idAttr)) return idAttr.replace(/^create-/,"").replace(/-btn$/,"");
    const href = el.getAttribute("href")||""; if (href){ const m=href.match(/^\/([^\/]+)\/(get|create|update|delete)(\/|$)/i); if (m) return m[1]; }
    const wrap = el.closest("[data-entity]"); if (wrap) return wrap.getAttribute("data-entity")||"";
    return "";
  }
  function getIdFromElement(el){
    if (!el) return "";
    let id = el.dataset.id || el.getAttribute("data-id") || el.closest("[data-id]")?.getAttribute("data-id") || "";
    if (!id){ const href=el.getAttribute("href")||""; const m = href && href.match(/\/(update|get|delete)\/([^\/]+)\/?$/i); if (m) id=m[2]; }
    if (!id){ const tr=el.closest("tr"); const pk=tr?.dataset?.id||tr?.dataset?.pk||""; if (pk) id=pk; }
    return (id||"").replace(/^:/,"");
  }

  // routing: skip userprofile so it hard-navigates
  on("keydown", ENTITY_BTN_SEL, (e,t)=>{ if (e.key!=="Enter" && e.key!==" ") return; e.preventDefault(); t.click(); }, true);
  on("click", ENTITY_BTN_SEL, (e,t)=>{
    if (__DISABLE_ROUTER) return;
    const entity = getEntityFromElement(t);
    const id     = getIdFromElement(t);
    const href = t.getAttribute && t.getAttribute("href");

    if (href && /^mailto:|^tel:/i.test(href)) return;
if (!entity) return;

    e.preventDefault();
    e.stopImmediatePropagation();

    if (t.matches("[data-open-entity], .btn-add, [id^='create-'][id$='-btn']")) {
      openEntityModal(entity);
    } else if (t.matches("[data-edit-entity], .btn-edit")) {
      if (!id) return; editEntity(entity, id);
    } else if (t.matches("[data-delete-entity], .btn-delete")) {
      if (!id) return; deleteEntity(entity, id);
    }
  }, true);

  on("click", "a[href^='/'][href*='/get/'], a[href^='/'][href*='/update/']", (e,a)=>{
    if (__DISABLE_ROUTER) return;
    const href = a.getAttribute("href")||"";
    const mAdd = href.match(/^\/([^\/]+)\/get\/?(\?.*)?$/i);
    const mEdit= href.match(/^\/([^\/]+)\/update\/([^\/]+)\/?(\?.*)?$/i);
    if (!mAdd && !mEdit) return;
    if (a.closest("#entity-modal")) return;
    const ent = mAdd ? mAdd[1] : (mEdit ? mEdit[1] : "");

e.preventDefault(); e.stopImmediatePropagation();
    if (mAdd) openEntityModal(mAdd[1]);
    else if (mEdit) editEntity(mEdit[1], mEdit[2]);
  }, true);

  // close buttons
  on("click", ".close-btn,.btn-close,.close,[data-dismiss='modal']", (e,btn)=>{
    const m = btn.closest(".modal"); if (!m) return;
    if (m.id==="login-modal") closeLoginModal(); else if (m.id==="image-preview-modal") closeImageModal(); else closeEntityModal();
  }, true);
  on("keydown", ".close-btn,.btn-close,.close,[data-dismiss='modal']", (e,btn)=>{
    if (e.key!=="Enter" && e.key!==" ") return;
    const m = btn.closest(".modal"); if (!m) return;
    if (m.id==="login-modal") closeLoginModal(); else if (m.id==="image-preview-modal") closeImageModal(); else closeEntityModal();
  }, true);

  [["entity-modal", ()=>closeEntityModal()], ["login-modal", ()=>closeLoginModal()]].forEach(([id, fn])=>{
    document.addEventListener("click", e=>{ const m=qs("#"+id); if (!m) return; if (e.target===m){ fn(); }}, true);
  });

  document.addEventListener("keydown", e=>{
    if (e.key!=="Escape") return;
    const im=qs("#image-preview-modal"), lm=qs("#login-modal"), em=qs("#entity-modal");
    if (im && im.style.display==="flex") closeImageModal(); else if (lm && lm.style.display==="flex") closeLoginModal(); else if (em && em.style.display==="flex") closeEntityModal();
  });

  // sidebar dropdown toggle
  function setupSidebarDropdownToggle(){
    const dds = Array.from(document.querySelectorAll(".sidebar .dropdown"));
    dds.forEach(dd=>{ const link = dd.querySelector(":scope > a"); if (!link) return;
      link.addEventListener("click", e=>{ e.preventDefault(); dds.forEach(d=>{ if (d!==dd) d.classList.remove("open"); }); dd.classList.toggle("open"); });
    });
    document.addEventListener("click", e=>{ if (!e.target.closest(".sidebar")) dds.forEach(d=> d.classList.remove("open")); });
  }

  // exports
  window.ensureModalSkeleton = ensureModalSkeleton;
  window.openLoadingShell = openLoadingShell;
  window.replaceModalWithHTML = replaceModalWithHTML;
  window.insertEntityModal = insertEntityModal;
  window.openEntityModal = openEntityModal;
  window.editEntity = editEntity;
  window.deleteEntity = deleteEntity;
  window.closeEntityModal = closeEntityModal;
  window.applyCheckboxGrid = applyCheckboxGrid;
  window.setupSidebarDropdownToggle = setupSidebarDropdownToggle;
  window.ensureEntityButtonsEnabled = ensureEntityButtonsEnabled;
  window.normalizeEntityButtons = normalizeEntityButtons;
  window.getEntityBase = getEntityBase;

  document.addEventListener("DOMContentLoaded", function(){
    ensureEntityButtonsEnabled(); normalizeEntityButtons(document); setupSidebarDropdownToggle();
    const toggleBtn  = document.getElementById("sidebar-toggle");
    const sidebar    = document.getElementById("sidebar");
    if (toggleBtn && sidebar){
      toggleBtn.addEventListener("click", function(){
        sidebar.classList.toggle("collapsed");
        const content = document.querySelector(".admin-main-content");
        if (content) content.style.marginLeft = sidebar.classList.contains("collapsed") ? "0" : "250px";
      });
    }
  });
})();
