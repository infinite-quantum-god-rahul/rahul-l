/* Extracted from script.js — app.images.js */
/* ====== IMAGE PREVIEW, LOGIN, USERPROFILE PATCH, CREDIT MODAL ====== */
(function(){
  const qs  = window.qs  || ((s, r=document) => r.querySelector(s));
  const qsa = window.qsa || ((s, r=document) => Array.from(r.querySelectorAll(s)));
  const on  = window.on  || ((t, s, h, o=false) => document.addEventListener(t, e => { const m = s ? e.target.closest(s) : e.target; if (!m) return; h(e, m); }, o));
  const getEntityBase = window.getEntityBase || (e => `/${encodeURIComponent(String(e||"").toLowerCase())}/`);
  const handleAuthFailure = window.handleAuthFailure || (m=> alert(m||"Not authenticated."));

  // ---------- Image preview helpers + overlay control ----------
  function normalizeMediaPath(src){
    if (!src) return "";
    src = String(src).replace(/^['"]|['"]$/g,"");
    if (/^data:image\//i.test(src)) return src;
    if (/^https?:\/\//i.test(src) || /^\/\//.test(src)) return src;
    if (src.startsWith("/")) return src;
    const low = src.toLowerCase();
    if (low.startsWith("media/")) return "/"+src.replace(/^\/+/, "");
    return "/media/"+src.replace(/^\/+/, "");
  }
  function bestFromStyle(el){
    try{
      const bg = getComputedStyle(el).backgroundImage||"";
      const m = bg.match(/url\(["\']?(.+?)["\']?\)/i); return m? m[1] : "";
    }catch(_){ return ""; }
  }
  function getFromSrcset(el){
    const ss = el && el.getAttribute && (el.getAttribute("srcset") || el.getAttribute("data-srcset") || el.getAttribute("data-lazy-srcset"));
    if (!ss) return "";
    const first = ss.split(",")[0]?.trim().split(" ")[0]?.trim();
    return first || "";
  }
  function getFromData(el){
    if (!el) return "";
    const attrs = [
      "data-src","data-original","data-lazy-src","data-url","data-image","data-href","data-file","data-photo","data-thumb","data-thumbnail","data-path","data-filename","data-placeholder",
      "data-srcset","data-lazy-srcset","data-bg","data-background","data-background-image"
    ];
    for (const a of attrs){ const v = el.getAttribute && el.getAttribute(a); if (v) return v; }
    const host = el.closest("[data-image],[data-src],[data-lazy-src],[data-url],[data-photo],[data-thumb],[data-thumbnail],[data-path],[data-srcset],[data-bg],[data-background],[data-background-image]");
    if (host){
      for (const a of attrs){ const v = host.getAttribute && host.getAttribute(a); if (v) return v; }
      const bg = bestFromStyle(host); if (bg) return bg;
    }
    return "";
  }
  function getBestImageSrc(el){
    if (!el) return "";
    const img = el.tagName==="IMG" ? el : el.querySelector && el.querySelector("img");
    const current = img?.currentSrc || "";
    const picture = el.closest("picture")?.querySelector("source[srcset]")?.getAttribute("srcset")||"";
    const href = el.closest("a")?.getAttribute("href") || "";
    const hrefLooksEntity = /^\/[^\/]+\/(get|update|create)\//i.test(href);
    return (
      getFromData(el) ||
      (img && (img.getAttribute("src") || current)) ||
      getFromSrcset(img||el) ||
      (picture && picture.split(",")[0].trim().split(" ")[0]) ||
      (!hrefLooksEntity && href) ||
      bestFromStyle(el) ||
      ""
    );
  }

  function deepFindImageUrl(obj, depth=0){
    if (!obj || depth>4) return "";
    if (typeof obj === "string"){
      const s = obj.trim();
      if (/^data:image\//i.test(s)) return s;
      if (/\.(png|jpe?g|webp|gif|bmp|svg)(\?|#|$)/i.test(s)) return s;
      if (/\/media\//i.test(s)) return s;
      return "";
    }
    if (typeof obj === "object"){
      const keys = Object.keys(obj);
      const priority = keys.filter(k=>/image|img|photo|avatar|thumbnail|thumb|picture|logo|url|path/i.test(k));
      for (const k of [...priority, ...keys]){
        const got = deepFindImageUrl(obj[k], depth+1);
        if (got) return got;
      }
    }
    if (Array.isArray(obj)){
      for (const it of obj){ const got = deepFindImageUrl(it, depth+1); if (got) return got; }
    }
    return "";
  }

  function setImageLoading(on){
    const sp = qs("#image-spinner");
    const img = qs("#image-preview");
    if (sp) sp.style.display = on ? "block" : "none";
    if (img) img.style.display = on ? "none" : "block";
  }
  function setMinimalMeta(entity, id, extra){
    const meta=qs("#image-meta-fields");
    if (!meta) return;
    const bits=[];
    if (entity) bits.push(`<p><strong>Entity:</strong> ${entity}</p>`);
    if (id)     bits.push(`<p><strong>ID:</strong> ${id}</p>`);
    if (extra && typeof extra==='object'){
      const pick = (k)=> extra[k]!=null && String(extra[k]).trim() ? String(extra[k]).trim() : "";
      const code = pick("code"); const name = pick("name"); const status = pick("status");
      if (code)   bits.push(`<p><strong>Code:</strong> ${code}</p>`);
      if (name)   bits.push(`<p><strong>Name:</strong> ${name}</p>`);
      if (status) bits.push(`<p><strong>Status:</strong> ${status}</p>`);
    }
    if (!bits.length) bits.push(`<p><em>No extra details</em></p>`);
    meta.innerHTML = bits.join("");
  }

  function showImageLayer(){
    const modal = qs("#image-preview-modal");
    const backdrop = qs("#image-preview-backdrop");
    if (!modal || !backdrop) return;
    // Kill bootstrap backdrops that may be lingering
    qsa(".modal-backdrop").forEach(b => b.remove());
    document.body.classList.add("image-modal-open");
    backdrop.style.display="block";
    modal.style.display="flex";
  }
  function hideImageLayer(){
    const modal = qs("#image-preview-modal");
    const backdrop = qs("#image-preview-backdrop");
    if (!modal || !backdrop) return;
    modal.style.display="none";
    backdrop.style.display="none";
    document.body.classList.remove("image-modal-open");
  }

  function openLocalImagePreview(file){
    ensureImagePreviewModal();
    const img=qs("#image-preview");
    if (!file || !img) return;
    setMinimalMeta(null, null);
    setImageLoading(true);
    const url = URL.createObjectURL(file);
    img.onload=()=>{ setImageLoading(false); try{ URL.revokeObjectURL(url); }catch(_){ } };
    img.onerror=()=>{ setImageLoading(false); alert("Could not preview this image."); };
    img.src = url;
    showImageLayer();
  }
  function openImageModal(id, entity, field){
    ensureImagePreviewModal();
    const img=qs("#image-preview");
    const meta=qs("#image-meta-fields");
    if (!img) return;
    if (meta) meta.innerHTML="";
    setMinimalMeta(entity, id);
    setImageLoading(true);
    img.removeAttribute("src");

    id=String(id||"").replace(/^:/,''); if (!entity){ setImageLoading(false); alert("Missing entity for image preview."); return; }
    const base=getEntityBase(entity); const url = `${base}get/${encodeURIComponent(id)}/?_=${Date.now()}`;
    fetch(url,{headers:{ "X-Requested-With":"XMLHttpRequest","Accept":"application/json,text/html,*/*" }, credentials:"include", cache:"no-store", redirect:"follow", keepalive:true})
    .then(async res=>{
      if (res.status===401 || res.status===403 || res.redirected){ setImageLoading(false); handleAuthFailure("Not authenticated."); return; }
      let data={};
      if (isJsonCt(res)) data=await res.json();
      else { const t=await res.text(); data[field||"image"]=t.trim(); }
      let p = field && data ? (data[field] || "") : "";
      if (!p){
        const commonKey = Object.keys(data).find(k=>/image|img|photo|picture|avatar|thumbnail|thumb|logo/i.test(k));
        p = commonKey ? data[commonKey] : "";
        if (!p) p = deepFindImageUrl(data);
      }
      if (p && typeof p==="object") p=p.url||p.path||deepFindImageUrl(p)||"";
      if (!p || !String(p).trim()){ setImageLoading(false); alert("Image not available."); setMinimalMeta(entity, id, data); return; }

      setMinimalMeta(entity, id, data);
      img.onload = ()=> setImageLoading(false);
      img.onerror = ()=>{ setImageLoading(false); alert("Failed to load image."); };
      img.src = normalizeMediaPath(p);
      showImageLayer();
    }).catch(e=>{ setImageLoading(false); console.error("Image preview:", e); alert("Failed to load image preview."); });
  }
  function closeImageModal(){ hideImageLayer(); }

  // Prevent internal clicks from closing image preview
  on("click", "#image-preview-modal .modal-content, #image-preview-modal .modal-content *", (ev)=>{ ev.stopPropagation(); }, true);

  // grid image and link support
  on("click", "table img, .grid img, img.thumbnail, img[data-preview], [data-preview='image'] img, .thumb, .thumb img, [data-preview='image'], td[data-image], .grid-cell[data-image]", (e, el)=>{
    e.preventDefault();
    ensureImagePreviewModal();
    const {entity,id} = (function(){ try{
      const row = el.closest("tr, [data-id], [data-pk], [data-rowkey], [data-key]") || el;
      let rid = (row?.dataset?.id || row?.dataset?.pk || row?.dataset?.rowkey || row?.dataset?.key || "").replace(/^:/,"");
      if (!rid){
        const cell = row?.querySelector?.('td[data-id],th[data-id]') || row?.querySelector?.('td,th');
        const txt = (cell?.textContent||"").trim();
        if (/^\d+$/.test(txt)) rid = txt;
      }
      let ent = el.dataset?.entity || row?.dataset?.entity || "";
      if (!ent){
        const t = el.closest("table,[data-entity]"); if (t?.dataset?.entity) ent = t.dataset.entity;
      }
      if (!ent){
        const href = el.closest("a")?.getAttribute("href") || "";
        const m = href.match(/^\/([^\/]+)\//); if (m) ent = m[1];
      }
      return { entity: ent, id: rid };
    }catch(_){ return {entity:null,id:null}; }})();

    const src = (function(){
      const img = el.tagName==="IMG" ? el : el.querySelector && el.querySelector("img");
      const current = img?.currentSrc || "";
      const picture = el.closest("picture")?.querySelector("source[srcset]")?.getAttribute("srcset")||"";
      const href = el.closest("a")?.getAttribute("href") || "";
      const hrefLooksEntity = /^\/[^\/]+\/(get|update|create)\//i.test(href);
      return (
        el.getAttribute && (el.getAttribute("data-image")||el.getAttribute("data-src")||el.getAttribute("href")||"") ||
        (img && (img.getAttribute("src") || current)) ||
        (img && getFromSrcset(img)) ||
        (picture && picture.split(",")[0].trim().split(" ")[0]) ||
        (!hrefLooksEntity && href) ||
        bestFromStyle(el) ||
        ""
      );
    })();

    if (src){
      const img=qs("#image-preview");
      if (!img) return;
      setMinimalMeta(entity, id);
      setImageLoading(true);
      img.onload  = ()=> setImageLoading(false);
      img.onerror = ()=>{ setImageLoading(false); alert("Failed to load image."); };
      img.src = normalizeMediaPath(src);
      showImageLayer();
      return;
    }
    if (entity && id){ openImageModal(id, entity); }
  }, true);

  on("click", ".image-link,.image-lk,[data-image-link],[data-view-image],[data-image-id]", (e,link)=>{
    e.preventDefault();
    const fileInputSel = link.dataset.input;
    const cand = fileInputSel ? qs(fileInputSel) : link.closest("form")?.querySelector('input[type="file"]');
    const file = cand?.files?.[0];
    if (file && /^image\//i.test(file.type)) { openLocalImagePreview(file); return; }

    const entity = link.dataset.entity;
    const id     = (link.dataset.id||"").replace(/^:/,"");
    const href   = getBestImageSrc(link) || link.getAttribute("href") || link.getAttribute("data-src") || link.getAttribute("data-image") || "";

    if (entity && id){ openImageModal(id, entity, link.dataset.field); return; }
    if (href){
      ensureImagePreviewModal();
      const img=qs("#image-preview");
      setMinimalMeta(null, null);
      setImageLoading(true);
      img.onload  = ()=> setImageLoading(false);
      img.onerror = ()=>{ setImageLoading(false); alert("Failed to load image."); };
      img.src = normalizeMediaPath(href);
      showImageLayer();
    }
  }, true);

  document.addEventListener("change", e=>{
    const input=e.target; if (!input || input.tagName!=="INPUT" || input.type!=="file" || !input.files || !input.files[0]) return;
    const f=input.files[0]; const looks = /^image\//i.test(f.type) || /image|photo|picture|avatar|img/i.test(input.name||"") || /image/i.test(input.accept||"");
    if (looks) openLocalImagePreview(f);
  });

  // ---------- Login modal (robust open wiring) ----------
  function resetLoginModalState(){
    const u=qs("#login-username"), p=qs("#login-password"), otp=qs("#otp-block"), err=qs("#login-error"), submit=qs("#login-submit");
    if (u){ u.value=""; u.removeAttribute("readonly"); }
    if (p){ p.value=""; p.removeAttribute("readonly"); }
    if (otp) otp.hidden=true;
    if (err){ err.hidden=true; err.style.display=""; err.textContent=""; }
    if (submit) submit.removeAttribute("disabled");
  }
  function openLoginModal(){
    const m=qs("#login-modal");
    if (m){
      resetLoginModalState();
      m.classList.add("show");
      m.style.display="flex";
      wirePasswordEyes(m); dedupePasswordEyes(m); reMaskPasswords(m);
      const u=qs("#login-username"); if (u) setTimeout(()=>u.focus(),0);
      return;
    }
    alert("Not authenticated.");
  }
  function closeLoginModal(){
    const m=qs("#login-modal");
    if (m){ m.classList.remove("show"); m.style.display="none"; resetLoginModalState(); }
  }
  window.openLoginModal = openLoginModal;
  window.closeLoginModal = closeLoginModal;

  // buttons that should open login
  document.addEventListener("DOMContentLoaded", function(){
    const adminLink = document.getElementById("admin-login-toggle");
    if (adminLink && !adminLink.dataset.bound){
      adminLink.dataset.bound="1";
      adminLink.addEventListener("click", e=>{
        e.preventDefault();
        openLoginModal();
      });
    }
    qsa("[data-open-login]").forEach(btn=>{
      if (btn.dataset.boundLogin) return;
      btn.dataset.boundLogin="1";
      btn.addEventListener("click", e=>{ e.preventDefault(); openLoginModal(); });
    });
  });

  on("input", "#login-username, #login-password", (_e)=>{
    const u=qs("#login-username"), p=qs("#login-password"), sub=qs("#login-submit"), errDiv=qs("#login-error");
    const ok=!!(u?.value.trim() && p?.value.trim());
    if (sub) ok ? sub.removeAttribute("disabled") : sub.setAttribute("disabled","disabled");
    if (document.activeElement===u || document.activeElement===p){ if (errDiv){ errDiv.hidden=true; errDiv.style.display=""; errDiv.textContent=""; } }
  });

  on("submit", "#admin-login-form", async (e, form)=>{
    e.preventDefault();
    const fd=new FormData(form);
    try{
      const res = await fetchWithTimeout(form.action,{
        method:"POST",
        headers:{ "X-CSRFToken":getCsrfTokenSafe(),"X-Requested-With":"XMLHttpRequest","Accept":"application/json,text/html" },
        body:fd, credentials:"include", redirect:"follow", keepalive:true
      },15000);

      const ct=(res.headers.get("content-type")||"").toLowerCase();

      if (res.redirected && (!ct || !ct.includes("application/json"))) {
        closeLoginModal(); location.href = res.url || "/dashboard/"; return;
      }

      if ([400,401,403].includes(res.status)){ showInlineLoginError("Invalid credentials."); return; }

      if (ct.includes("application/json")){
        const d=await res.json();
        if (d.success){ closeLoginModal(); location.href = d.redirect_url || "/dashboard/"; return; }
        if (d.require_otp){ const b=qs("#otp-block"); if (b) b.hidden=false; }
        showInlineLoginError(d.error||"Invalid credentials."); return;
      }

      showInlineLoginError("Invalid credentials.");
    }catch(_){
      showInlineLoginError("Network error. Please try again.");
    }
  });

  // ---------- USERPROFILE page robust Add/Edit (hard navigate) ----------
  (function userProfilePatch(){
    // Activate strictly on real UserProfile routes only
    const isUP = /(^|\/)userprofile(\/|$)/i.test(location.pathname);
    if (!isUP) return;

    addStyleOnce('userprofile-button-unlock', `
      a[href^="/userprofile/"], a[href^="/UserProfile/"] { pointer-events:auto!important; opacity:1!important; }
      a[href^="/userprofile/"].disabled, a[href^="/UserProfile/"].disabled { pointer-events:auto!important; opacity:1!important; }
      .up-force-pointer{pointer-events:auto!important;opacity:1!important}
    `);

    const enable = el => { if (!el) return; el.removeAttribute("disabled"); el.setAttribute("aria-disabled","false"); el.classList.remove("disabled"); el.classList.add("up-force-pointer"); el.style.pointerEvents="auto"; if (!el.hasAttribute("tabindex")) el.tabIndex=0; if (!el.hasAttribute("role")) el.setAttribute("role", el.tagName==="A"?"link":"button"); };
    const idFromHref = (href, op)=> { const m=String(href||"").match(new RegExp(`${op}/([^/]+)/?$`,"i")); return m? m[1].replace(/^:/,'') : ""; };
    const idFromRow  = el => { const tr=el.closest('tr'); if (!tr) return ""; const pk=tr.dataset.id||tr.dataset.pk||tr.getAttribute('data-id')||tr.getAttribute('data-pk')||""; if (pk) return pk.replace(/^:/,''); const cell=tr.querySelector('td,th'); const v=(cell?.textContent||"").trim(); return /^\d+$/.test(v)?v:""; };

    function hardNavTo(url){ window.location.href = url; }

    function bindAdd(){
      const nodes = new Set([
        ...qsa('a[href^="/userprofile/get"]'),
        ...qsa('a[href^="/UserProfile/get"]'),
        ...qsa('[data-open-entity="UserProfile"], [data-open-entity="userprofile"]'),
        ...qsa('#create-UserProfile-btn, #create-userprofile-btn, #create-userprofile')
      ]);
      if (nodes.size===0){ qsa('.grid-container .btn, .grid-header .btn, .page-actions .btn').forEach(b=>{ if (/^add|create$/i.test((b.textContent||"").trim())) nodes.add(b); }); }
      nodes.forEach(a=>{
        if (a.dataset.boundUserProfileAdd) return; a.dataset.boundUserProfileAdd="1"; enable(a);
        a.addEventListener('click', e=>{
          e.preventDefault(); e.stopPropagation();
          const href=a.getAttribute('href')||'';
          const target = /\/(userprofile|UserProfile)\/get\/?/.test(href) ? href : "/UserProfile/get/";
          hardNavTo(target);
        });
      });
    }
    function bindEdit(){
      const anchors = [...qsa('a[href*="/userprofile/update/"]'), ...qsa('a[href*="/UserProfile/update/"]'), ...qsa('[data-edit-entity="UserProfile"], [data-edit-entity="userprofile"]')];
      anchors.forEach(a=>{
        if (a.dataset.boundUserProfileEdit) return; a.dataset.boundUserProfileEdit="1"; enable(a);
        a.addEventListener('click', e=>{
          e.preventDefault(); e.stopPropagation();
          const raw=a.getAttribute('href')||''; const id=idFromHref(raw,'update') || idFromRow(a); if (!id) return;
          const base=/\/UserProfile\//.test(raw)?"/UserProfile/":"/userprofile/";
          hardNavTo(`${base}update/${encodeURIComponent(id)}/`);
        });
      });
    }
    function bindDelete(){
      const anchors = [...qsa('a[href*="/userprofile/delete/"]'), ...qsa('a[href*="/UserProfile/delete/"]'), ...qsa('[data-delete-entity="UserProfile"], [data-delete-entity="userprofile"]')];
      anchors.forEach(a=>{
        if (a.dataset.boundUserProfileDelete) return; a.dataset.boundUserProfileDelete="1"; enable(a);
        a.addEventListener("click", e=>{
          e.preventDefault(); e.stopPropagation();
          const raw=a.getAttribute('href')||'';
          const id=idFromHref(raw,'delete') || idFromRow(a);
          if (!id) return;
          try{ deleteEntity('UserProfile', id); }catch(_){ console.error('deleteEntity missing'); }
        });
      });
    }
    function bindAll(){ bindAdd(); bindEdit(); bindDelete(); }
    bindAll(); const mo=new MutationObserver(()=> bindAll()); mo.observe(document.body,{childList:true,subtree:true});
    document.addEventListener("click", e=>{ const a=e.target?.closest?.('a[href*="/UserProfile/get"], a[href*="/userprofile/get"]'); if (!a) return; /* allow default now handled above */ }, true);
  })();

  // ---------- Credit modal ----------
  function openCreditPullModal(){
    let modal=qs("#credit-modal"); if (modal) modal.remove();
    modal=document.createElement("div"); modal.id="credit-modal"; modal.className="modal"; modal.style.display="flex";
    modal.innerHTML = `
      <div class="modal-content" style="max-width:520px;">
        <div class="modal-header d-flex justify-content-between align-items-center mb-2">
          <h5 class="modal-title">Credit Bureau Check</h5>
          <button type="button" class="close-btn" onclick="document.getElementById('credit-modal').remove()">&times;</button>
        </div>
        <div class="modal-body">
          <div class="mb-2"><input id="cb-name" class="form-control" placeholder="Full Name"></div>
          <div class="mb-2"><input id="cb-dob" class="form-control" placeholder="DOB dd/mm/yyyy"></div>
          <div class="mb-2"><input id="cb-pan" class="form-control" placeholder="PAN"></div>
          <div class="mb-2"><input id="cb-aadhar" class="form-control" placeholder="Aadhaar (0000 0000 0000)"></div>
          <div class="d-flex justify-content-end gap-2 mt-3">
            <button class="btn btn-secondary" onclick="document.getElementById('credit-modal').remove()">Close</button>
            <button class="btn btn-primary" id="cb-submit">Check</button>
          </div>
          <pre id="cb-result" class="mt-3" style="white-space:pre-wrap;max-height:260px;overflow:auto;"></pre>
        </div>
      </div>`;
    document.body.appendChild(modal);

    const aad = modal.querySelector("#cb-aadhar");
    if (aad){
      aad.addEventListener("input", ()=>{
        const v = aad.value.replace(/\D/g,"").slice(0,12);
        aad.value = v.replace(/(\d{4})(?=\d)/g, "$1 ").trim();
      });
    }
    const btn = modal.querySelector("#cb-submit");
    if (btn) btn.addEventListener("click", submitCreditPull);
  }

  async function submitCreditPull(){
    const modal = qs("#credit-modal"); if (!modal) return;
    const payload = {
      name:   (modal.querySelector("#cb-name")?.value || "").trim(),
      dob:    (modal.querySelector("#cb-dob")?.value || "").trim(),
      pan:    (modal.querySelector("#cb-pan")?.value || "").trim(),
      aadhar: (modal.querySelector("#cb-aadhar")?.value || "").replace(/\s+/g,"")
    };
    const out = modal.querySelector("#cb-result"); if (out) out.textContent = "Checking…";
    try{
      const res = await fetch("/api/credit-bureau/pull/", {
        method:"POST",
        headers:{
          "Content-Type":"application/json",
          "X-Requested-With":"XMLHttpRequest",
          "X-CSRFToken":getCsrfTokenSafe(),
          "Accept":"application/json"
        },
        credentials:"include",
        body: JSON.stringify(payload),
        redirect:"follow",
        keepalive:true
      });
      const ct = (res.headers.get("content-type")||"").toLowerCase();
      if (res.status===401 || res.status===403 || res.redirected){ handleAuthFailure("Not authenticated."); return; }
      if (!ct.includes("application/json")){
        const txt = await res.text().catch(()=> "");
        if (out) out.textContent = "Unexpected server response.\n" + txt.slice(0,300);
        return;
      }
      const data = await res.json();
      if (out) out.textContent = JSON.stringify(data, null, 2);
    }catch(e){
      console.error("credit pull error", e);
      if (out) out.textContent = "Network error. Please try again.";
    }
  }

  // expose
  window.openImageModal = openImageModal;
  window.closeImageModal = closeImageModal;
  window.openCreditPullModal = openCreditPullModal;
})();

/* ====== STABLE OVERRIDE BLOCK: modal flow + image preview (syntactically clean) ====== */
(function(){
  // Helpers that don't assume existing ones
  const qs  = (s, r=document) => r.querySelector(s);
  const qsa = (s, r=document) => Array.from(r.querySelectorAll(s));
  const on  = (t, s, h, o=false) => document.addEventListener(t, e => {
    const m = s ? (e.target.closest ? e.target.closest(s) : null) : e.target;
    if (!m) return; try { h(e, m); } catch(_){}
  }, o);
  const isJsonCt = r => !!(r && r.headers && String(r.headers.get("content-type")||"").toLowerCase().includes("application/json"));
  const deepFindHtml = (obj)=>{
    try{
      if (!obj || typeof obj!=="object") return "";
      if (obj.html || obj.body || obj.template) return obj.html||obj.body||obj.template;
      for (const k of Object.keys(obj)){
        const v = obj[k];
        const found = typeof v==="object" ? deepFindHtml(v) : "";
        if (found) return found;
      }
    }catch(_){}
    return "";
  };

  function normalizeMediaPath(src){
    if (!src) return "";
    src = String(src).replace(/^['"]|['"]$/g,"").trim();
    const low = src.toLowerCase();
    if (!src || low==="img" || low==="image" || low==="#" || low==="/img" || low==="/image") return "";
    if (/^data:image\//i.test(src)) return src;
    if (/^https?:\/\//i.test(src) || /^\/\//.test(src)) return src;
    if (src.startsWith("/")) return src;
    if (low.startsWith("media/")) return "/"+src.replace(/^\//, "");
    return "/media/"+src.replace(/^\//, "");
  }
  function isPlaceholderSrc(src){
    if (!src) return true;
    const s = String(src).trim();
    return !s || s==="#" || /^img$/i.test(s) || /^image$/i.test(s);
  }

  // Insert into existing modal using app's function if present
  function insertModal(entity, html, mode, id, base){
    if (typeof window.insertEntityModal === "function"){
      return window.insertEntityModal(entity, html, mode, id, base);
    }
    // Fallback minimal injector
    let wrap = qs("#entity-modal"); if (!wrap){ wrap = document.createElement("div"); wrap.id="entity-modal"; document.body.appendChild(wrap); }
    wrap.innerHTML = String(html||"");
    wrap.style.display="block";
  }

  // Build fallbacks if app helper missing
  function buildTryUrls(mode, entity, id){
    if (typeof window.buildTryUrls === "function"){
      return window.buildTryUrls(mode, entity, id);
    }
    const baseLower = "/"+String(entity||"").toLowerCase()+"/";
    const baseOrig  = "/"+String(entity||"")+"/";
    const list = mode==="Create"
      ? [ baseLower+"create/", baseLower+"get/" ]
      : [ baseLower+"update/"+encodeURIComponent(String(id||"")).replace(/^%3A/,"")+"/",
          baseLower+"get/"+encodeURIComponent(String(id||"")).replace(/^%3A/,"")+"/" ];
    return { list, baseLower, baseOrig };
  }

  async function loadEntityFormSafe(mode, entity, id){
    const { list, baseLower, baseOrig } = buildTryUrls(mode, entity, id);
    const opts = { headers:{ "X-Requested-With":"XMLHttpRequest" }, credentials:"include", cache:"no-store", redirect:"follow", keepalive:true };

    try{ if (typeof window.openLoadingShell==="function") window.openLoadingShell(`${mode} ${String(entity||"")}`); }catch(_){}
    window.__MODAL_LOADING = true; window.__MODAL_GOT_RESPONSE=false; window.__HARD_NAV_ISSUED=false;

    if (window.__FALLBACK_TIMER) { clearTimeout(window.__FALLBACK_TIMER); window.__FALLBACK_TIMER=null; }
    window.__FALLBACK_TIMER = setTimeout(()=>{
      if (window.__CANCEL_MODAL) return;
      if (window.__MODAL_LOADING && !window.__MODAL_GOT_RESPONSE && !qs("#entity-modal .modal-body form") && !window.__HARD_NAV_ISSUED){
        window.__HARD_NAV_ISSUED = true;
        const dest = (mode==="Create"
          ? `${baseOrig}get/`
          : `${baseOrig}update/${encodeURIComponent(String(id||"")).replace(/^:/,"")}/`);
        window.location.href = dest;
      }
    }, 3500);

    for (const u of list){
      let res; try{ res = await fetch(u, opts); }catch(_){ continue; }
      if (!res) continue;
      if (res.status===401 || res.status===403 || res.redirected){
        // auth failure – keep login intact
        try{
          if (typeof window.handleAuthFailure==="function") window.handleAuthFailure("Not authenticated.");
          if (res.url) window.location.href = res.url;
        }catch(_){}
        return;
      }
      window.__MODAL_GOT_RESPONSE = true;

      if (isJsonCt(res)){
        const d = await res.json().catch(()=>null);
        if (d){
          const jump = d.redirect || d.url || d.location;
          if (typeof jump === "string" && jump){ window.location.href = jump; return; }
          // Special-case login: keep legacy behavior
          if (/^login$/i.test(String(entity||"")) && d.html){
            insertModal(entity, d.html, mode, id, baseLower);
            window.__MODAL_LOADING=false; clearTimeout(window.__FALLBACK_TIMER); window.__FALLBACK_TIMER=null;
            return;
          }
          let h = (d.html || d.body || d.template);
          if (!h) h = deepFindHtml(d);
          if (h){
            insertModal(entity, h, mode, id, u.startsWith(baseOrig)?baseOrig:baseLower);
            window.__MODAL_LOADING=false; clearTimeout(window.__FALLBACK_TIMER); window.__FALLBACK_TIMER=null;
            return;
          }
        }
      } else {
        let t = await res.text().catch(()=> "");
        if (t && t.trim().startsWith("{")){
          try{ const j=JSON.parse(t); const h2 = deepFindHtml(j); if (h2) t = h2; }catch(_){}
        }
        if (t){
          insertModal(entity, t, mode, id, u.startsWith(baseOrig)?baseOrig:baseLower);
          window.__MODAL_LOADING=false; clearTimeout(window.__FALLBACK_TIMER); window.__FALLBACK_TIMER=null;
          return;
        }
      }
    }

    // Nothing worked; let fallback timer redirect
  }

  // Override only the loader. Keep openEntityModal/editEntity wiring intact.
  window.loadEntityForm = loadEntityFormSafe;

  // Image preview: robust guard + normalized load
  on("click", "img.thumbnail, .grid img, [data-preview='image']", (e, el)=>{
    const imgEl = el.tagName==="IMG" ? el : el.querySelector("img");
    const raw = imgEl ? (imgEl.getAttribute("src") || imgEl.getAttribute("data-src") || "") : "";
    if (isPlaceholderSrc(raw)){ alert("No image available."); return; }
    const src = normalizeMediaPath(raw);
    if (!src){ alert("No image available."); return; }

    const img = qs("#image-preview");
    if (!img) return;
    try{ if (typeof window.setMinimalMeta==="function"){ const row=el.closest("[data-id],[data-entity]"); const id=row?.getAttribute?.("data-id")||""; const entity=row?.getAttribute?.("data-entity")||""; window.setMinimalMeta(entity, id); } }catch(_){}
    try{ if (typeof window.setImageLoading==="function") window.setImageLoading(true); }catch(_){}
    img.onload  = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){} };
    img.onerror = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){} alert("Failed to load image."); };
    img.src = src;
    try{ if (typeof window.showImageLayer==="function") window.showImageLayer(); }catch(_){}
  }, true);
})();

/* === Final one-pass patch: UserProfile hard-nav + safe image preview === */
(function(){
  const qs = window.qs || ((s,r=document)=>r.querySelector(s));
  const on = window.on || ((t,s,h,o=false)=>document.addEventListener(t,e=>{const m=s?e.target.closest(s):e.target;if(!m)return;try{h(e,m);}catch(_){}} ,o));

  function normalizeMediaPath(src){
    if (!src) return "";
    src = String(src).replace(/^['"]|['"]$/g,"").trim();
    const low = src.toLowerCase();
    if (!src || low==="img" || low==="image" || low==="#" ) return "";
    if (/^data:image\//i.test(src)) return src;
    if (/^https?:\/\//i.test(src) || /^\/\//.test(src)) return src;
    if (src.startsWith("/")) return src;
    if (low.startsWith("media/")) return "/"+src.replace(/^\/+/, "");
    return "/media/"+src.replace(/^\/+/, "");
  }

  // ---- 1) Hard navigation for UserProfile Add/Edit to avoid JSON modal dumps
  (function(){
    const _open = window.openEntityModal;
    window.openEntityModal = function(arg){
      let entity = typeof arg==="string" ? arg : (arg?.currentTarget?.dataset?.entity || arg?.dataset?.entity || "");
      if (/^userprofile$/i.test(String(entity||""))){
        window.location.href = "/UserProfile/get/";
        return;
      }
      return typeof _open==="function" ? _open.apply(this, arguments) : undefined;
    };

    const _edit = window.editEntity;
    window.editEntity = function(entity, id){
      if (/^userprofile$/i.test(String(entity||"")) && id){
        window.location.href = "/UserProfile/update/"+encodeURIComponent(String(id).replace(/^:/,""))+"/";
        return;
      }
      return typeof _edit==="function" ? _edit.apply(this, arguments) : undefined;
    };
  })();

  // ---- 2) Image preview guard: block placeholders and only preview valid URLs
  on("click", "table img, .grid img, img.thumbnail, [data-preview='image'], [data-preview='image'] img", (e, el)=>{
    const imgEl = el.tagName==="IMG" ? el : (el.querySelector && el.querySelector("img"));
    const raw = (imgEl && (imgEl.getAttribute("src") || imgEl.currentSrc)) ||
                el.getAttribute?.("data-src") || el.getAttribute?.("data-image") || el.getAttribute?.("href") || "";
    const norm = normalizeMediaPath(raw);
    // Try to infer entity/id for fallback
    const row = el.closest && el.closest("[data-entity][data-id]");
    const entity = row?.getAttribute?.("data-entity") || "";
    const id = (row?.getAttribute?.("data-id") || "").replace(/^:/,"");

    if (!norm){
      if (entity && id && typeof window.openImageModal==="function"){
        e.preventDefault(); e.stopImmediatePropagation();
        window.openImageModal(id, entity);
        return;
      }
      e.preventDefault(); e.stopImmediatePropagation();
      alert("No image available.");
      return;
    }

    // valid URL -> open overlay
    const modalImg = qs("#image-preview");
    if (!modalImg) return;
    e.preventDefault(); e.stopImmediatePropagation();
    try{ window.setMinimalMeta && window.setMinimalMeta(entity, id); }catch(_){}
    try{ window.setImageLoading && window.setImageLoading(true); }catch(_){}
    modalImg.onload  = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){}};
    modalImg.onerror = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){} alert("Failed to load image."); };
    modalImg.src = norm;
    try{ window.showImageLayer && window.showImageLayer(); }catch(_){}
  }, true);
})();

/* === FINAL ENFORCER: UserProfile hard-nav at router + safe image preview === */
(function(){
  const qs = (s,r=document)=>r.querySelector(s);
  const on = (t,s,h,o=false)=>document.addEventListener(t,e=>{const m=s?e.target.closest(s):e.target;if(!m)return;try{h(e,m);}catch(_){ }},o);

  function normalizeMediaPath(src){
    if(!src) return "";
    src=String(src).replace(/^['"]|['"]$/g,"").trim();
    const low=src.toLowerCase();
    if(!src || low==="img" || low==="image" || low==="#") return "";
    if(/^data:image\//i.test(src)) return src;
    if(/^https?:\/\//i.test(src)||/^\/\//.test(src)) return src;
    if(src.startsWith("/")) return src;
    if(low.startsWith("media/")) return "/"+src.replace(/^\/+/, "");
    return "/media/"+src.replace(/^\/+/, "");
  }

  function userProfileHardNav(mode, id){
    if(mode==="add") { window.location.href="/UserProfile/get/"; return true; }
    if(mode==="edit" && id){ window.location.href="/UserProfile/update/"+encodeURIComponent(String(id).replace(/^:/,""))+"/"; return true; }
    return false;
  }

  // 1) Intercept any Add/Edit click for UserProfile at the earliest router layer
  on("click", "[data-open-entity],[data-edit-entity], .btn-add, .btn-edit, a[href^='/UserProfile/']", (e, el)=>{
    const ent = (el.dataset.openEntity||el.dataset.editEntity||el.dataset.entity||"").toLowerCase() ||
                ((el.getAttribute("href")||"").toLowerCase().startsWith("/userprofile/") ? "userprofile" : "");
    if(ent!=="userprofile") return;

    e.preventDefault(); e.stopImmediatePropagation();
    const href = el.getAttribute("href")||"";
    const mAdd  = /^\/userprofile\/get\/?/i.test(href);
    const mEdit = href.match(/^\/userprofile\/update\/([^\/]+)\/?/i);
    if (mAdd || el.classList.contains("btn-add") || el.hasAttribute("data-open-entity")) { userProfileHardNav("add"); return; }
    if (mEdit || el.classList.contains("btn-edit") || el.hasAttribute("data-edit-entity")) {
      const id = (el.dataset.id || (mEdit?mEdit[1]:"") || "").replace(/^:/,"");
      userProfileHardNav("edit", id); return;
    }
  }, true);

  // 2) Make openEntityModal/editEntity also hard-nav for defense in depth
  try{
    const _open = window.openEntityModal;
    window.openEntityModal = function(arg){
      let entity = typeof arg==="string" ? arg : (arg?.currentTarget?.dataset?.entity || arg?.dataset?.entity || "");
      if (/^userprofile$/i.test(String(entity||""))) { userProfileHardNav("add"); return; }
      return typeof _open==="function" ? _open.apply(this, arguments) : undefined;
    };
  }catch(_){}
  try{
    const _edit = window.editEntity;
    window.editEntity = function(entity, id){
      if (/^userprofile$/i.test(String(entity||""))) { userProfileHardNav("edit", id); return; }
      return typeof _edit==="function" ? _edit.apply(this, arguments) : undefined;
    };
  }catch(_){}

  // 3) Image preview: strict guard and fallback
  on("click", "table img, .grid img, img.thumbnail, [data-preview='image'], [data-preview='image'] img", (e, el)=>{
    const imgEl = el.tagName==="IMG" ? el : (el.querySelector && el.querySelector("img"));
    const raw = (imgEl && (imgEl.getAttribute("src") || imgEl.currentSrc)) ||
                el.getAttribute?.("data-src") || el.getAttribute?.("data-image") || el.getAttribute?.("href") || "";
    const norm = normalizeMediaPath(raw);
    const row = el.closest && el.closest("[data-entity][data-id]");
    const entity = row?.getAttribute?.("data-entity") || "";
    const id = (row?.getAttribute?.("data-id") || "").replace(/^:/,"");

    e.preventDefault(); e.stopImmediatePropagation();
    if (!norm){
      if (entity && id && typeof window.openImageModal==="function"){ window.openImageModal(id, entity); return; }
      alert("No image available."); return;
    }

    const modalImg = qs("#image-preview");
    if (!modalImg) { if (entity && id && typeof window.openImageModal==="function"){ window.openImageModal(id, entity); } else { alert("No image modal found."); } return; }
    try{ window.setMinimalMeta && window.setMinimalMeta(entity, id); }catch(_){}
    try{ window.setImageLoading && window.setImageLoading(true); }catch(_){}
    modalImg.onload  = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){}};
    modalImg.onerror = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){} alert("Failed to load image."); };
    modalImg.src = norm;
    try{ window.showImageLayer && window.showImageLayer(); }catch(_){}
  }, true);
})();

/* === STRICT OVERRIDE: make UserProfile Add/Edit hard-navigate; force image preview modal === */
(function(){
  // 1) UserProfile: always navigate full page. Avoid any modal interception.
  document.addEventListener("click", function(ev){
    const a = ev.target.closest && ev.target.closest("a,button,[data-open-entity],[data-edit-entity]");
    if (!a) return;
    const href = (a.getAttribute && a.getAttribute("href")) || "";
    const ent  = (a.dataset && (a.dataset.entity || a.dataset.openEntity || a.dataset.editEntity)) || "";
    const isUP = /^userprofile$/i.test(ent) || /^\/userprofile\//i.test(href||"");
    if (!isUP) return;
    // compute destination
    let dest = href || "";
    if (!dest){
      const id = (a.dataset && a.dataset.id) ? String(a.dataset.id).replace(/^:/,"") : "";
      dest = a.hasAttribute("data-edit-entity") && id ? ("/UserProfile/update/"+encodeURIComponent(id)+"/")
           : "/UserProfile/get/";
    }
    ev.preventDefault(); ev.stopImmediatePropagation();
    window.location.href = dest;
  }, true);

  // 2) Image preview: capture-phase handler that prefers normalized URL, else fetch via openImageModal
  document.addEventListener("click", function(ev){
    const el = ev.target.closest && ev.target.closest("table img, .grid img, img.thumbnail, [data-preview='image'], [data-preview='image'] img");
    if (!el) return;
    const qs = (s,r=document)=>r.querySelector(s);
    const srcRaw = (el.getAttribute && (el.getAttribute("src") || el.getAttribute("data-src"))) || el.currentSrc || "";
    const norm = (function(src){
      if(!src) return "";
      src = String(src).replace(/^['"]|['"]$/g,"").trim();
      const low = src.toLowerCase();
      if (!src || low==="img" || low==="image" || low==="#") return "";
      if (/^data:image\//i.test(src)) return src;
      if (/^https?:\/\//i.test(src) || /^\/\//.test(src)) return src;
      if (src.startsWith("/")) return src;
      if (low.startsWith("media/")) return "/"+src.replace(/^\/+/, "");
      return "/media/"+src.replace(/^\/+/, "");
    })(srcRaw);

    const row = el.closest && el.closest("[data-entity][data-id]");
    const entity = row && row.getAttribute("data-entity") || "";
    const id = row && row.getAttribute("data-id") ? row.getAttribute("data-id").replace(/^:/,"") : "";

    ev.preventDefault(); ev.stopImmediatePropagation();

    // Ensure modal shell exists
    (function ensureImagePreviewModal(){
      if (document.querySelector("#image-preview-modal")) return;
      const backdrop = document.createElement("div");
      backdrop.id="image-preview-backdrop"; backdrop.style.cssText="position:fixed;inset:0;background:rgba(0,0,0,.5);display:none;z-index:2147483600";
      document.body.appendChild(backdrop);
      const m = document.createElement("div");
      m.id="image-preview-modal"; m.className="modal"; m.style.cssText="position:fixed;inset:0;display:none;align-items:center;justify-content:center;z-index:2147483646";
      m.innerHTML = '<div class="modal-content image-modal" style="background:#fff;max-width:min(96vw,900px);width:100%"><div class="modal-header d-flex justify-content-between align-items-center mb-2"><h5 class="modal-title">Image Preview</h5><button type="button" class="close-btn" data-close-image>&times;</button></div><div class="modal-body"><div id="image-spinner" style="text-align:center;margin:0 0 12px 0;display:none;">Loading…</div><img id="image-preview" src="" alt="Preview" style="max-width:100%;max-height:70vh;display:none;margin:0 auto 12px;background:transparent;"><div id="image-meta-fields"></div><div class="d-flex justify-content-end mt-3"><button class="btn btn-secondary" data-close-image>Close</button></div></div></div>';
      document.body.appendChild(m);
      document.addEventListener("click", function(e2){ if (e2.target.closest("[data-close-image]")) close(); }, true);
      document.addEventListener("click", function(e2){ const im=document.querySelector("#image-preview-modal"); if (e2.target===im) close(); }, true);
      function close(){ const im=document.querySelector("#image-preview-modal"), bd=document.querySelector("#image-preview-backdrop"); if (im) im.style.display="none"; if (bd) bd.style.display="none"; document.body.classList.remove("image-modal-open"); }
      window.closeImageModal = close;
    })();

    const im = qs("#image-preview-modal"), bd = qs("#image-preview-backdrop"), img = qs("#image-preview");
    const spinner = qs("#image-spinner");
    if (!im || !bd || !img) return;

    function setLoading(on){ if (spinner) spinner.style.display = on?"block":"none"; if (img) img.style.display = on?"none":"block"; }
    function show(){ document.body.classList.add("image-modal-open"); bd.style.display="block"; im.style.display="flex"; }

    if (norm){
      setLoading(true);
      img.onload=()=> setLoading(false);
      img.onerror=()=>{ setLoading(false); alert("Failed to load image."); };
      img.src = norm; show(); return;
    }

    // Fallback to server fetch if we have entity+id
    if (entity && id && typeof window.openImageModal==="function"){ window.openImageModal(id, entity); return; }

    alert("No image available.");
  }, true);
})();

/* === FINAL SAFE OVERRIDE: Restore buttons, force UserProfile nav, fix image preview === */
(function(){
  // Safe helpers
  const qs = (s,r=document)=>r.querySelector(s);
  const on = (t,s,h,o=false)=>document.addEventListener(t,e=>{const m=s?e.target.closest(s):e.target;if(!m)return;try{h(e,m);}catch(_){ }},o);

  // 1) Ensure entity buttons are clickable regardless of earlier patches
  (function ensureButtons(){
    const sel = "[data-open-entity],[data-edit-entity],[data-delete-entity],.btn-add,.btn-edit,.btn-delete,a[href^='/']";
    document.querySelectorAll(sel).forEach(el=>{
      el.removeAttribute?.("disabled");
      el.classList?.remove("disabled");
      if (el.style){ el.style.pointerEvents="auto"; el.style.visibility="visible"; if (el.style.display==="none") el.style.display=""; }
    });
  })();

  // 2) UserProfile: allow native navigation for Add/Edit so it never hangs
  document.addEventListener("click", function(ev){
    const a = ev.target.closest && ev.target.closest("a[href^='/UserProfile/']");
    if (!a) return;
    const href = a.getAttribute("href")||"";
    if (!/^\/UserProfile\/(get|update)\//i.test(href)) return;
    // Let the browser handle it cleanly
    ev.stopImmediatePropagation();
    // Do NOT preventDefault; we want native navigation
  }, true);

  // 3) Image preview: guard placeholders, open modal only when valid URL
  function normMedia(src){
    if(!src) return "";
    src = String(src).replace(/^['"]|['"]$/g,"").trim();
    const low = src.toLowerCase();
    if (!src || low==="img" || low==="image" || low==="#") return "";
    if (/^data:image\//i.test(src)) return src;
    if (/^https?:\/\//i.test(src) || /^\/\//.test(src)) return src;
    if (src.startsWith("/")) return src;
    if (low.startsWith("media/")) return "/"+src.replace(/^\/+/, "");
    return "/media/"+src.replace(/^\/+/, "");
  }
  function ensureImagePreviewModal(){
    if (qs("#image-preview-modal")) return;
    const bd = document.createElement("div"); bd.id="image-preview-backdrop"; bd.style.cssText="position:fixed;inset:0;background:rgba(0,0,0,.5);display:none;z-index:2147483600"; document.body.appendChild(bd);
    const m = document.createElement("div"); m.id="image-preview-modal"; m.className="modal"; m.style.cssText="position:fixed;inset:0;display:none;align-items:center;justify-content:center;z-index:2147483640";
    m.innerHTML = '<div class="modal-content image-modal" style="background:#fff;max-width:min(96vw,900px);width:100%"><div class="modal-header d-flex justify-content-between align-items-center mb-2"><h5 class="modal-title">Image Preview</h5><button type="button" class="close-btn" data-close-image>&times;</button></div><div class="modal-body"><div id="image-spinner" style="text-align:center;margin:0 0 12px 0;display:none;">Loading…</div><img id="image-preview" src="" alt="Preview" style="max-width:100%;max-height:70vh;display:none;margin:0 auto 12px;"><div id="image-meta-fields"></div><div class="d-flex justify-content-end mt-3"><button class="btn btn-secondary" data-close-image>Close</button></div></div></div>';
    document.body.appendChild(m);
    document.addEventListener("click", e=>{ if (e.target.closest("[data-close-image]")) close(); }, true);
    document.addEventListener("click", e=>{ const im=qs("#image-preview-modal"); if (e.target===im) close(); }, true);
    function close(){ const im=qs("#image-preview-modal"), bd=qs("#image-preview-backdrop"); if (im) im.style.display="none"; if (bd) bd.style.display="none"; document.body.classList.remove("image-modal-open"); }
    window.closeImageModal = close;
  }
  function showLayer(){ const im=qs("#image-preview-modal"), bd=qs("#image-preview-backdrop"); if (!im||!bd) return; document.body.classList.add("image-modal-open"); bd.style.display="block"; im.style.display="flex"; }
  function setLoading(on){ const sp=qs("#image-spinner"), img=qs("#image-preview"); if (sp) sp.style.display=on?"block":"none"; if (img) img.style.display=on?"none":"block"; }

  document.addEventListener("click", function(ev){
    const el = ev.target.closest && ev.target.closest("table img, .grid img, img.thumbnail, [data-preview='image'], [data-preview='image'] img");
    if (!el) return;
    ensureImagePreviewModal();
    const imgEl = el.tagName==="IMG" ? el : (el.querySelector && el.querySelector("img"));
    const raw = (imgEl && (imgEl.getAttribute("src") || imgEl.currentSrc)) ||
                el.getAttribute?.("data-src") || el.getAttribute?.("data-image") || el.getAttribute?.("href") || "";
    const url = normMedia(raw);
    const row = el.closest && el.closest("[data-entity][data-id]");
    const entity = row?.getAttribute?.("data-entity") || "";
    const id = (row?.getAttribute?.("data-id") || "").replace(/^:/,"");

    ev.preventDefault(); ev.stopImmediatePropagation();
    if (url){
      const img = qs("#image-preview"); if (!img) return;
      setLoading(true);
      img.onload = ()=> setLoading(false);
      img.onerror= ()=>{ setLoading(false); alert("Failed to load image."); };
      img.src = url;
      showLayer();
      return;
    }
    if (entity && id && typeof window.openImageModal==="function"){ window.openImageModal(id, entity); return; }
    alert("No image available.");
  }, true);
})();

/* === FINAL PATCH: UserProfile hard-nav + guarded image preview (capture-phase, non-invasive) === */
(function(){
  // Minimal helpers
  const qs  = (s,r=document)=>r.querySelector(s);
  const qsa = (s,r=document)=>Array.from(r.querySelectorAll(s));
  const on  = (t,s,h,o=false)=>document.addEventListener(t,e=>{const m=s? (e.target.closest?e.target.closest(s):null):e.target;if(!m)return;try{h(e,m);}catch(_){ }},o);

  // -------- UserProfile: force hard navigation --------
  // Works even if other handlers exist, because we capture and stop only for UserProfile.
  on("click",
     "[data-open-entity],[data-edit-entity],.btn-add,.btn-edit,a[href^='/UserProfile/']",
     (e, el)=>{
       // Resolve entity and id
       let entity = (el.dataset?.entity || el.dataset?.openEntity || el.dataset?.editEntity || "").toLowerCase();
       const href = (el.getAttribute && el.getAttribute("href")) || "";
       if (!entity && /^\/userprofile\//i.test(href)) entity = "userprofile";
       if (entity !== "userprofile") return; // do not interfere with other entities

       const id = (el.dataset?.id || el.getAttribute?.("data-id") || "").replace(/^:/,"");

       // Decide add vs edit
       const isAdd  = el.matches?.("[data-open-entity], .btn-add, [id^='create-'][id$='-btn']") || /\/get\/?$/i.test(href);
       const isEdit = el.matches?.("[data-edit-entity], .btn-edit") || /\/update\/[^/]+\/?$/i.test(href);

       e.preventDefault(); e.stopImmediatePropagation();

       if (isEdit) {
         if (!id && href) {
           // try parse from href /update/<id>/
           const m = href.match(/\/update\/([^/]+)\//i);
           if (m) { window.location.href = "/UserProfile/update/"+encodeURIComponent(m[1])+"/"; return; }
         }
         if (!id) return;
         window.location.href = "/UserProfile/update/"+encodeURIComponent(id)+"/";
         return;
       }
       // default to Add
       window.location.href = "/UserProfile/get/";
     },
     true);

  // -------- Image preview: guard placeholders, fallback to server, else modal --------
  function normalizeMediaPath(src){
    if (!src) return "";
    src = String(src).replace(/^['"]|['"]$/g,"").trim();
    const low = src.toLowerCase();
    if (!src || low==="img" || low==="image" || low==="#" ) return "";
    if (/^data:image\//i.test(src)) return src;
    if (/^https?:\/\//i.test(src) || /^\/\//.test(src)) return src;
    if (src.startsWith("/")) return src;
    if (low.startsWith("media/")) return "/"+src.replace(/^\/+/, "");
    return "/media/"+src.replace(/^\/+/, "");
  }
  function findEntityContext(el){
    const row = el.closest && el.closest("[data-entity][data-id]");
    const entity = row?.getAttribute?.("data-entity") || "";
    const id = (row?.getAttribute?.("data-id") || "").replace(/^:/,"");
    return {entity,id};
  }

  on("click",
     "table img, .grid img, img.thumbnail, [data-preview='image'], [data-preview='image'] img",
     (e, el)=>{
       const imgEl = el.tagName==="IMG" ? el : (el.querySelector && el.querySelector("img"));
       const raw = (imgEl && (imgEl.getAttribute("src") || imgEl.currentSrc)) ||
                   el.getAttribute?.("data-src") || el.getAttribute?.("data-image") || el.getAttribute?.("href") || "";
       const norm = normalizeMediaPath(raw);
       const {entity,id} = findEntityContext(el);

       // Always handle here to avoid broken previews from other handlers
       e.preventDefault(); e.stopImmediatePropagation();

       if (!norm){
         if (entity && id && typeof window.openImageModal==="function"){
           window.openImageModal(id, entity);
           return;
         }
         alert("No image available.");
         return;
       }

       const modalImg = qs("#image-preview");
       if (!modalImg){
         // If app did not render preview modal yet, fall back to server fetch
         if (entity && id && typeof window.openImageModal==="function"){ window.openImageModal(id, entity); return; }
         alert("Image preview modal not found.");
         return;
       }
       try{ window.setMinimalMeta && window.setMinimalMeta(entity, id); }catch(_){}
       try{ window.setImageLoading && window.setImageLoading(true); }catch(_){}
       modalImg.onload  = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){}};
       modalImg.onerror = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){ } alert("Failed to load image."); };
       modalImg.src = norm;
       try{ window.showImageLayer && window.showImageLayer(); }catch(_){}
     },
     true);
})();

/* === One-pass fix: keep UserProfile modal (cancel hard-nav) + safe image preview === */
(function(){
  // --- Cancel any hard-navigation fallback once modal HTML arrives
  function stopFallbackIfModalReady(){
    try{
      const hasModal = !!document.querySelector("#entity-modal .modal-body form, #entity-modal form");
      if (hasModal && window.__FALLBACK_TIMER){
        clearTimeout(window.__FALLBACK_TIMER);
        window.__FALLBACK_TIMER = null;
        window.__HARD_NAV_ISSUED = false;
        window.__MODAL_LOADING = false;
      }
    }catch(_){}
  }
  // Watchdog to neutralize premature hard-nav (runs for ~10s after page ready)
  (function(){
    const start = Date.now();
    const iv = setInterval(()=>{
      stopFallbackIfModalReady();
      if (Date.now() - start > 10000) clearInterval(iv);
    }, 200);
    document.addEventListener("DOMContentLoaded", stopFallbackIfModalReady, {once:false});
  })();

  // --- Safer normalizeMediaPath that treats placeholders as empty
  function normalizeMediaPathSafe(src){
    if (!src) return "";
    src = String(src).replace(/^['"]|['"]$/g,"").trim();
    const low = src.toLowerCase();
    if (!src || low==="img" || low==="image" || low==="#" ) return "";
    if (/^data:image\//i.test(src)) return src;
    if (/^https?:\/\//i.test(src) || /^\/\//.test(src)) return src;
    if (src.startsWith("/")) return src;
    if (low.startsWith("media/")) return "/"+src.replace(/^\/+/, "");
    return "/media/"+src.replace(/^\/+/, "");
  }

  // --- Image preview: capture-phase guard and normalized preview
  document.addEventListener("click", function(ev){
    const el = ev.target.closest && ev.target.closest("table img, .grid img, img.thumbnail, [data-preview='image'], [data-preview='image'] img");
    if (!el) return;

    const qs = (s,r=document)=>r.querySelector(s);
    const imgEl = el.tagName==="IMG" ? el : (el.querySelector && el.querySelector("img"));
    const raw = (imgEl && (imgEl.getAttribute("src") || imgEl.currentSrc)) ||
                el.getAttribute?.("data-src") || el.getAttribute?.("data-image") || el.getAttribute?.("href") || "";
    const norm = normalizeMediaPathSafe(raw);

    const row = el.closest && el.closest("[data-entity][data-id]");
    const entity = row?.getAttribute?.("data-entity") || "";
    const id = (row?.getAttribute?.("data-id") || "").replace(/^:/,"");

    ev.preventDefault(); ev.stopImmediatePropagation();

    if (!norm){
      if (entity && id && typeof window.openImageModal==="function"){
        window.openImageModal(id, entity);
        return;
      }
      alert("No image available.");
      return;
    }

    const modalImg = qs("#image-preview");
    if (!modalImg){
      if (entity && id && typeof window.openImageModal==="function"){ window.openImageModal(id, entity); return; }
      alert("Image preview modal not found."); return;
    }
    try{ window.setMinimalMeta && window.setMinimalMeta(entity, id); }catch(_){}
    try{ window.setImageLoading && window.setImageLoading(true); }catch(_){}
    modalImg.onload  = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){}};
    modalImg.onerror = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){} alert("Failed to load image."); };
    modalImg.src = norm;
    try{ window.showImageLayer && window.showImageLayer(); }catch(_){}
  }, true);
})();

/* === Override: Force hard navigation for UserProfile (capture-phase, highest priority) === */
(function(){
  function getAttr(el, name){ try{ return el.getAttribute(name) || ""; }catch(_){ return ""; } }
  function getData(el, name){ try{ return el.dataset ? (el.dataset[name] || "") : ""; }catch(_){ return ""; } }
  function getIdFrom(el){
    let id = getData(el, "id") || getAttr(el, "data-id") || "";
    if (!id){
      const href = getAttr(el, "href");
      const m = href && href.match(/\/update\/([^\/]+)\/?$/i);
      if (m) id = m[1];
    }
    if (!id){
      const row = el.closest && el.closest("[data-id]");
      if (row) id = getAttr(row, "data-id") || "";
    }
    return String(id||"").replace(/^:/,"");
  }
  document.addEventListener("click", function(ev){
    const el = ev.target.closest && ev.target.closest("[data-open-entity],[data-edit-entity],[data-entity],.btn-add,.btn-edit,a[href^='/UserProfile/']");
    if (!el) return;
    let entity = (getData(el,"openEntity") || getData(el,"editEntity") || getData(el,"entity")).toLowerCase();
    const href = getAttr(el, "href");
    if (!entity && /^\/userprofile\//i.test(href)) entity = "userprofile";
    if (entity !== "userprofile") return;

    ev.preventDefault(); ev.stopImmediatePropagation();

    const id = getIdFrom(el);
    const isEdit = el.matches && el.matches("[data-edit-entity], .btn-edit") || /\/update\//i.test(href);
    const dest = isEdit
      ? (id ? `/UserProfile/update/${encodeURIComponent(id)}/` : "/UserProfile/get/")
      : "/UserProfile/get/";
    window.location.href = dest;
  }, true);
})();

/* === FINAL PATCH: UserProfile hard-nav + robust image preview URL normalizer === */
(function(){
  const on = (t,s,h,o=false)=>document.addEventListener(t,e=>{const m=s?(e.target.closest?e.target.closest(s):null):e.target;if(!m)return;try{h(e,m);}catch(_){ }},o);

  // 1) Force navigation for any UserProfile click, including sidebar
  on("click","a[href*='/UserProfile'],a[href*='/userprofile'],[data-entity='UserProfile'],[data-open-entity='UserProfile'],[data-edit-entity='UserProfile'],.btn-add,.btn-edit",(e,el)=>{
    // Decide if this click is about UserProfile
    const href = el.getAttribute && el.getAttribute("href") || "";
    const ent  = (el.dataset && (el.dataset.entity || el.dataset.openEntity || el.dataset.editEntity)) || "";
    const isUP = /\/userprofile/i.test(href) || /^userprofile$/i.test(ent);
    if (!isUP) return;

    // Resolve id for edit
    let id = (el.dataset && (el.dataset.id || "")) || el.getAttribute && el.getAttribute("data-id") || "";
    if (!id){
      const m = href && href.match(/\/update\/([^\/]+)\/?/i);
      if (m) id = m[1];
    }
    if (!id){
      const row = el.closest && el.closest("[data-id]");
      if (row) id = row.getAttribute("data-id") || "";
    }
    id = String(id||"").replace(/^:/,"");

    // Route: if href exists and already points to UserProfile, go there
    e.preventDefault(); e.stopImmediatePropagation();
    if (href && /\/userprofile/i.test(href)){ window.location.href = href; return; }

    const isEdit = el.matches && el.matches("[data-edit-entity='UserProfile'], .btn-edit") || /\/update\//i.test(href);
    window.location.href = isEdit && id ? `/UserProfile/update/${encodeURIComponent(id)}/` : "/UserProfile/get/";
  }, true);

  // 2) Robust normalizer: handle placeholders and relative media like "Company/company_logos/..."
  function normalizeMediaPathStrict(src){
    if (!src) return "";
    src = String(src).replace(/^['"]|['"]$/g,"").trim();
    const low = src.toLowerCase();
    if (!src || low==="img" || low==="image" || low==="#" ) return "";
    if (/^data:image\//i.test(src)) return src;
    if (/^(https?:)?\/\//i.test(src)) return src;
    if (src.startsWith("/")) return src;
    // Relative paths: if they already include known media dirs, prefix with /media/
    if (/^(company\/company_logos|company_logos|media|static|uploads)\//i.test(src)) return "/media/" + src.replace(/^\/+/, "");
    // Default: assume it's a relative media file
    return "/media/" + src.replace(/^\/+/, "");
  }

  // 3) Capture-phase image preview handler that uses the strict normalizer
  on("click","table img,.grid img,img.thumbnail,[data-preview='image'],[data-preview='image'] img,.thumb,.thumb img",(e,el)=>{
    const imgEl = el.tagName==="IMG" ? el : (el.querySelector && el.querySelector("img"));
    const raw = (imgEl && (imgEl.getAttribute("src") || imgEl.currentSrc)) ||
                el.getAttribute?.("data-src") || el.getAttribute?.("data-image") || el.getAttribute?.("href") || "";
    const url = normalizeMediaPathStrict(raw);

    // derive context
    const row = el.closest && el.closest("[data-entity][data-id]");
    const entity = row?.getAttribute?.("data-entity") || "";
    const id = (row?.getAttribute?.("data-id") || "").replace(/^:/,"");

    e.preventDefault(); e.stopImmediatePropagation();

    // if no good URL, try server-side preview
    if (!url){
      if (entity && id && typeof window.openImageModal==="function"){ window.openImageModal(id, entity); return; }
      alert("No image available."); return;
    }

    const modalImg = document.querySelector("#image-preview");
    if (!modalImg){
      if (entity && id && typeof window.openImageModal==="function"){ window.openImageModal(id, entity); return; }
      alert("Image preview modal not found."); return;
    }
    try{ window.setMinimalMeta && window.setMinimalMeta(entity, id); }catch(_){}
    try{ window.setImageLoading && window.setImageLoading(true); }catch(_){}
    modalImg.onload  = ()=>{ try{ window.setImageLoading && window.setImageLoading(false); }catch(_){}};
    modalImg.onerror = ()=>{
      try{ window.setImageLoading && window.setImageLoading(false); }catch(_){}
      // If the normalized URL 404s, fall back to server modal
      if (entity && id && typeof window.openImageModal==="function"){ window.openImageModal(id, entity); return; }
      alert("Failed to load image.");
    };
    modalImg.src = url;
    try{ window.showImageLayer && window.showImageLayer(); }catch(_){}
  }, true);
})();



/* === Hard Intercept for UserProfile Add === */
(function(){
  if (window.__UP_INTERCEPT_INSTALLED__) return;
  window.__UP_INTERCEPT_INSTALLED__ = true;
  const on = window.on || ((t, s, h, o=false) => document.addEventListener(t, e => { const m = s ? e.target.closest(s) : e.target; if (!m) return; h(e, m); }, o));
  const qs = window.qs || (s=>document.querySelector(s));

  function matchesUserProfileGet(v){
    if (!v) return false;
    return /\/UserProfile\/get\/?(\?|$)/i.test(String(v));
  }
  function openUP(){
    if (typeof window.openEntityModal === "function"){ window.openEntityModal("UserProfile"); return; }
    // fallback full nav
    window.location.href="/UserProfile/get/";
  }

  on("click", "a[href]", (e,a)=>{
    const href = a.getAttribute("href")||"";
    if (!matchesUserProfileGet(href)) return;
    if (a.closest("#entity-modal")) return;
    e.preventDefault(); e.stopImmediatePropagation();
    openUP();
  }, true);

  on("submit", "form[action]", (e,f)=>{
    const action = f.getAttribute("action")||"";
    if (!matchesUserProfileGet(action)) return;
    if (f.closest("#entity-modal")) return;
    e.preventDefault(); e.stopImmediatePropagation();
    openUP();
  }, true);

  document.addEventListener("click", function(e){
    let n = e.target;
    while (n && n !== document){
      const h = n.getAttribute && (n.getAttribute("href") || n.getAttribute("data-href") || n.getAttribute("onclick") || "");
      if (matchesUserProfileGet(h)){
        e.preventDefault(); e.stopImmediatePropagation(); openUP(); return;
      }
      n = n.parentElement;
    }
  }, true);

  try{
    const _open = window.open;
    window.open = function(url,name,spec){
      if (typeof url === "string" && matchesUserProfileGet(url)){ openUP(); return null; }
      return _open.apply(this, arguments);
    };
  }catch(_){}
})();


/* ====== SAFE SHIM: normalize entity casing + guard fallback ====== */
(function(){
  function lower(s){ return String(s||'').toLowerCase(); }

  // Wrap openEntityModal to force lowercase entity name
  if (typeof window.openEntityModal === "function" && !window.openEntityModal.__lowerShim){
    const _open = window.openEntityModal;
    window.openEntityModal = function(entityOrEvent){
      // Support both direct entity string and delegated event
      if (typeof entityOrEvent === "string") {
        return _open.call(this, lower(entityOrEvent));
      } else if (entityOrEvent && entityOrEvent.currentTarget) {
        const el = entityOrEvent.currentTarget;
        const ent = el.getAttribute("data-entity") || el.dataset.entity || "";
        if (ent) return _open.call(this, lower(ent));
      }
      return _open.apply(this, arguments);
    };
    window.openEntityModal.__lowerShim = true;
  }

  // Wrap editEntity to force lowercase entity name
  if (typeof window.editEntity === "function" && !window.editEntity.__lowerShim){
    const _edit = window.editEntity;
    window.editEntity = function(entity, id){
      return _edit.call(this, lower(entity), id);
    };
    window.editEntity.__lowerShim = true;
  }

  // Ensure any modal HTML arrival sets a flag used by timeout fallbacks
  (function markOnDomInsert(){
    const mark = function(){
      try { window.__MODAL_GOT_RESPONSE = true; } catch(_){}
    };
    if (document.getElementById("entity-modal")) mark();
    const mo = new MutationObserver((muts)=>{
      for (const m of muts){
        for (const n of m.addedNodes){
          if (n.nodeType === 1 && (n.id === "entity-modal" || (n.querySelector && n.querySelector("#entity-modal")))) { mark(); return; }
        }
      }
    });
    mo.observe(document.documentElement || document.body, { childList: true, subtree: true });
  })();
})();


/* ====== FINAL UI UNLOCK SHIM (append-only, preserves existing logic) ====== */
(function(){
  function unlock(){
    try{
      window.__MODAL_GOT_RESPONSE = true;
      if (window.__FALLBACK_TIMER){ clearTimeout(window.__FALLBACK_TIMER); window.__FALLBACK_TIMER = null; }
    }catch(_){}

    // Remove common overlays/backdrops/spinners that block clicks
    var sel = [
      ".modal-backdrop",".loading-overlay",".preloader",".global-loader",".page-loader",
      ".blockUI",".blockOverlay",".blockMsg",".ui-dimmer",".screen-lock",".prevent-click",
      "#loading","#loader","#overlay","#preloader","#ajaxLoading","#page-loader","#spinner"
    ].join(",");
    document.querySelectorAll(sel).forEach(function(n){
      try{ n.remove(); }catch(_){ n.style.display="none"; n.style.pointerEvents="none"; }
    });

    // Re-enable interaction on <body>
    var b=document.body;
    if (b){
      ["loading","disabled","busy","blocked"].forEach(function(c){ b.classList.remove(c); });
      b.removeAttribute("inert");
      b.removeAttribute("aria-busy");
      b.style.pointerEvents="auto";
      if (b.style.overflow === "hidden") b.style.overflow = "";
    }

    // Ensure modal remains interactive
    if (!document.getElementById("force-unfreeze-style")){
      var s = document.createElement("style");
      s.id = "force-unfreeze-style";
      s.textContent = ".modal, .modal *{pointer-events:auto!important}";
      document.head.appendChild(s);
    }
  }

  // Call unlock when modal content functions run
  ["replaceModalWithHTML","insertEntityModal","openLoadingShell"].forEach(function(fn){
    if (typeof window[fn] === "function" && !window[fn].__unlockShim){
      var orig = window[fn];
      window[fn] = function(){
        var out = orig.apply(this, arguments);
        try{ unlock(); }catch(_){}
        return out;
      };
      window[fn].__unlockShim = true;
    }
  });

  // Also unlock when #entity-modal is inserted
  try{
    var mo = new MutationObserver(function(muts){
      for (var i=0;i<muts.length;i++){
        var m = muts[i];
        for (var j=0;j<m.addedNodes.length;j++){
          var n = m.addedNodes[j];
          if (n.nodeType===1 && (n.id==="entity-modal" || (n.querySelector && n.querySelector("#entity-modal")))){
            unlock(); return;
          }
        }
      }
    });
    mo.observe(document.documentElement||document.body,{childList:true,subtree:true});
  }catch(_){}

  // Run once now and on DOM ready
  try{ unlock(); }catch(_){}
  document.addEventListener("DOMContentLoaded", function(){ try{ unlock(); }catch(_){ } });
})();
