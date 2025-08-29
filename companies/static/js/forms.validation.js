/* Extracted from script.js — app.forms.js */
/* ====== DATES, VALIDATION, SAVE HANDLER ====== */
(function(){
  const qs  = window.qs  || ((s, r=document) => r.querySelector(s));

  function isValidDateDDMMYYYY(s){
    if (!/^\d{2}\/\d{2}\/\d{4}$/.test(s)) return false;
    const [d,m,y] = s.split('/').map(Number);
    if (y < 1900 || y > 9999) return false;
    if (m < 1 || m > 12) return false;
    const dim = new Date(y, m, 0).getDate();
    return d >= 1 && d <= dim;
  }
  function attachDateMask(el){
    if (!el || el.dataset.maskBound) return; el.dataset.maskBound="1";
    el.setAttribute("maxlength","10"); el.setAttribute("inputmode","numeric");
    el.addEventListener("input", e=>{
      let v = e.target.value.replace(/[^\d]/g,'').slice(0,8);
      if (v.length>=5) v = v.slice(0,2)+"/"+v.slice(2,4)+"/"+v.slice(4);
      else if (v.length>=3) v = v.slice(0,2)+"/"+v.slice(2);
      e.target.value=v;
      if (v.length===10 && !isValidDateDDMMYYYY(v)) e.target.setCustomValidity("Enter date as dd/mm/yyyy"); else e.target.setCustomValidity("");
      const form = e.target.form; if (form) { const saveBtn = document.getElementById("modal-save-btn"); recomputeSaveEnabled(form, saveBtn); }
    });
    el.addEventListener("blur", e=>{
      const v = (e.target.value||"").trim();
      if (v && !isValidDateDDMMYYYY(v)) e.target.setCustomValidity("Enter date as dd/mm/yyyy"); else e.target.setCustomValidity("");
    });
  }
  function initializeDatePickers(){ if (typeof flatpickr!=="undefined") flatpickr(".date-field",{dateFormat:"d/m/Y",allowInput:true,altInput:false}); }
  function formatDateFields(){
    document.querySelectorAll(window.DATE_SEL).forEach(input=>{
      if (input.value && /^\d{4}-\d{2}-\d{2}$/.test(input.value)) {
        const [y,m,d] = input.value.split("-"); input.value = `${d}/${m}/${y}`;
      }
      input.pattern = "\\d{2}/\\d{2}/\\d{4}"; input.placeholder="dd/mm/yyyy"; input.type="text";
      attachDateMask(input); input.addEventListener("input", ()=> input.setCustomValidity(""));
    });
  }

  // masks
  function addMasks(){
    document.querySelectorAll('input[name="phone"]').forEach(el=>{
      el.addEventListener("input", ()=>{ el.value = el.value.replace(/\D/g,'').slice(0,10); });
    });
    document.querySelectorAll('input[name="aadhar"], #id_aadhar_number').forEach(el=>{
      el.addEventListener('input', ()=>{
        const v = el.value.replace(/\D/g,'').slice(0,12);
        el.value = v.replace(/(\d{4})(?=\d)/g, "$1 ").trim();
      });
    });
  }
  function initPhoneInputs(){
    if (typeof window.intlTelInput === "undefined") return;
    document.querySelectorAll('input[name="phone"]').forEach(inp=>{
      if (inp.dataset.itiAttached) return;
      window.intlTelInput(inp,{separateDialCode:true,initialCountry:"in",preferredCountries:["in","us","ae","gb"]});
      inp.dataset.itiAttached="1";
      inp.addEventListener("input", ()=>{ inp.value=inp.value.replace(/\D/g,'').slice(0,10); });
    });
  }

  // permissions
  function setupPermissionSelectAll(){
    document.querySelectorAll('.check-all').forEach(sel=>{
      const group = sel.dataset.group; const boxes = document.querySelectorAll(`.form-check-input.${group}`);
      sel.addEventListener('change', function(){ boxes.forEach(cb=> cb.checked=this.checked); });
      boxes.forEach(cb=> cb.addEventListener('change', ()=>{ sel.checked = Array.from(boxes).every(c=>c.checked); }));
    });
  }
  function setupRoleSwitches(){
    const master=qs('#role-master-switch'), staff=qs('#role-staff-switch'), report=qs('#role-report-switch');
    if (!master || !staff || !report) return;
    const cbs = Array.from(document.querySelectorAll('.perm-checkbox'));
    const loan = cbs.filter(cb=> cb.dataset.perm?.includes('loanapplication'));
    const fs   = cbs.filter(cb=> cb.dataset.perm?.includes('fieldschedule'));
    const fr   = cbs.filter(cb=> cb.dataset.perm?.includes('fieldreport'));
    const clear = ()=>{ cbs.forEach(cb=>{ cb.checked=false; cb.disabled=false; }); };
    master.addEventListener('change', ()=>{ clear(); if (master.checked){ cbs.forEach(cb=> cb.checked=true); staff.checked=report.checked=false; }});
    staff.addEventListener('change',  ()=>{ clear(); if (staff.checked){ loan.forEach(cb=>{ cb.checked=true; cb.disabled=true; }); master.checked=report.checked=false; }});
    report.addEventListener('change', ()=>{ clear(); if (report.checked){ [...fs,...fr].forEach(cb=>{ cb.checked=true; cb.disabled=true; }); master.checked=staff.checked=false; }});
  }

  // validation helpers
  const isVisible = el => !!(el && (el.offsetParent || el.getClientRects().length));
  function isGroupChecked(form, el){
    const t=(el.type||"").toLowerCase(); if (!/checkbox|radio/.test(t)) return true;
    const name=el.name; if (!name) return true;
    const group=form.querySelectorAll(`input[type="${t}"][name="${CSS.escape(name)}"]`);
    return Array.from(group).some(g=> g.checked);
  }
  function areAllVisibleFieldsFilled(form){
    const formEntity = (form?.dataset?.entity || document.body?.dataset?.entity || "").toLowerCase();
    const upStrict = formEntity === "userprofile"; // strict mode for UserProfile

    const fields = form.querySelectorAll("input, select, textarea");
    for (const el of fields){
      if (!isVisible(el) || el.disabled || el.type==="hidden") continue;
      const t=(el.type||"").toLowerCase(); if (t==="button" || t==="submit") continue;

      const req = upStrict
        ? (el.dataset.optional!=="true" && !el.closest(".optional"))
        : ((el.hasAttribute("required") || el.dataset.required==="true" || el.getAttribute("aria-required")==="true") && el.dataset.optional!=="true");

      if (!req) continue;

      if (/checkbox|radio/.test(t)){ if (!isGroupChecked(form, el)) return false; continue; }
      if (!String(el.value||"").trim()) return false;
    }
    return true;
  }
  function allDatesValid(form){
    for (const el of form.querySelectorAll(window.DATE_SEL)){
      if (!isVisible(el) || el.disabled) continue;
      const v=String(el.value||"").trim(); if (v && (v.length!==10 || !isValidDateDDMMYYYY(v))) return false;
    }
    return true;
  }
  function clearInvalids(root){
    root?.querySelectorAll(".invalid,.is-invalid").forEach(x=> x.classList.remove("invalid","is-invalid"));
    root?.querySelectorAll(".invalid-feedback").forEach(x=>{ x.textContent=""; x.style.display="none"; });
  }
  function validateForm(form){
    const r={valid:true,firstEl:null,msg:""}; const fields=form.querySelectorAll("input, select, textarea");
    for (const el of fields){
      if (el.closest("[hidden]") || el.type==="hidden" || el.disabled) continue;
      const req = el.hasAttribute("required") || el.dataset.required==="true" || el.getAttribute("aria-required")==="true";
      const val = String(el.value||"").trim();
      if (req && !val)  return fail(el,"Please fill the required field.");
      if (el.type==="email" && val && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) return fail(el,"Invalid email address.");
      if ((el.classList.contains("date-field") || el.dataset.type==="date" || /date|dob/i.test(el.name||"")) && val && !isValidDateDDMMYYYY(val)) return fail(el,"Date must be dd/mm/yyyy.");
      if (el.name && /aadhar/i.test(el.name) && val && !/^\d{4}\s\d{4}\s\d{4}$/.test(val)) return fail(el,"Invalid Aadhaar format.");
    }
    return r;
    function fail(el,msg){ mark(el,msg); r.valid=false; r.firstEl=el; r.msg=msg; return r; }
    function mark(el){ el.classList.add("invalid"); }
  }
  function focusAndClear(el){ if (!el) return; try{ el.focus({preventScroll:false}); }catch(_){} if ("select" in el) try{ el.select(); }catch(_){} el.value=""; el.scrollIntoView({block:"center",behavior:"smooth"}); }

  // errors
  function ensureFormErrorBox(){
    let box = qs("#form-errors");
    if (!box){ const mb = qs("#entity-modal .modal-body"); if (mb){ box=document.createElement("div"); box.id="form-errors"; box.setAttribute("role","alert"); box.setAttribute("aria-live","assertive"); mb.prepend(box);} }
    return box;
  }
  function showFormErrors(errors){
    const div = ensureFormErrorBox(); if (div) div.innerHTML="";
    for (let f in errors){
      const msgs = Array.isArray(errors[f]) ? errors[f].join(", ") : errors[f];
      if (div) div.innerHTML += `<p><strong>${f}:</strong> ${msgs}</p>`;
      markFieldInvalid(f, msgs);
    }
  }
  function markFieldInvalid(field, msg){
    const form = qs("#entity-form"); if (!form) return;
    let input = locateField(form, field); if (!input) return;
    input.classList.add("is-invalid");
    let fb = input.closest(".form-group,.field,.input-group,div")?.querySelector(".invalid-feedback");
    if (!fb){ fb=document.createElement("div"); fb.className="invalid-feedback"; input.after(fb); }
    fb.textContent = String(msg||""); fb.style.display="block";
  }
  function clearFieldErrors(form){ form.querySelectorAll(".is-invalid").forEach(el=> el.classList.remove("is-invalid")); form.querySelectorAll(".invalid-feedback").forEach(el=>{ el.textContent=""; el.style.display="none"; }); }
  function locateField(form, name){
    if (!name) return null;
    return form.querySelector(`[name="${CSS.escape(name)}"]`) ||
           form.querySelector(`[name="${CSS.escape(name)}[]"]`) ||
           form.querySelector(`#id_${CSS.escape(name)}`) ||
           form.querySelector(`[id$="${CSS.escape(name)}"]`);
  }

  // enable/disable Save
  function recomputeSaveEnabled(form, btn){
    if (!form || !btn) return;
    const enable = areAllVisibleFieldsFilled(form) && allDatesValid(form) && validateForm(form).valid;
    btn.disabled = !enable; btn.classList.toggle("save-disabled", !enable);
  }
  function prepareFormValidation(form, saveBtn){
    if (!form || !saveBtn) return;
    form.querySelectorAll(window.DATE_SEL).forEach(attachDateMask);
    const toggle = ()=> recomputeSaveEnabled(form, saveBtn);
    saveBtn.disabled = true; saveBtn.classList.add("save-disabled");
    const onChange = ()=>{ clearInvalids(form); toggle(); };
    form.querySelectorAll("input,select,textarea").forEach(el=>{
      el.addEventListener("input", onChange); el.addEventListener("change", onChange); el.addEventListener("blur", onChange);
    });
    toggle();
  }

  // save
  function setupSaveButtonHandler(){
    const btn = qs("#modal-save-btn"); if (!btn || btn.dataset.boundAjax==="1") return; btn.dataset.boundAjax="1";
    btn.addEventListener("click", e=>{
      e.preventDefault();
      const form = qs("#entity-form"); if (!form) return;
      clearFieldErrors(form); clearInvalids(form);
      const v = validateForm(form); if (!v.valid){ alert(v.msg||"Please correct highlighted fields."); focusAndClear(v.firstEl); return; }
      if (!areAllVisibleFieldsFilled(form) || !allDatesValid(form)){ alert("Please complete all fields and enter valid dates (dd/mm/yyyy)."); return; }

      const url=form.action; const fd = new FormData(form); const err = ensureFormErrorBox(); if (err) err.innerHTML="";
      form.querySelectorAll(window.DATE_SEL).forEach(inp=>{
        const m = String(inp.value||"").trim().match(/^(\d{2})\/(\d{2})\/(\d{4})$/); if (m) fd.set(inp.name, `${m[3]}-${m[2]}-${m[1]}`);
      });

      const prev = btn.textContent; btn.disabled=true; btn.classList.add("save-disabled"); btn.textContent="Saving...";
      fetch(url,{
        method:"POST",
        headers:{"X-CSRFToken":getCsrfTokenSafe(),"X-Requested-With":"XMLHttpRequest","Accept":"application/json,text/html"},
        body:fd, credentials:"include", redirect:"follow", keepalive:true
      })
      .then(async res=>{
        const ct = (res.headers.get("content-type")||"").toLowerCase();
        if (res.status===401 || res.status===403 || res.redirected) { handleAuthFailure("Not authenticated."); return; }
        if (ct.includes("application/json")){
          const data = await res.json();
          if (data.success){ closeEntityModal(); location.reload(); return; }
          if (data.errors){ showFormErrors(data.errors); const [f,msgs]=Object.entries(data.errors)[0]||[]; const el=locateField(qs("#entity-form"),f); if (el){ el.classList.add("invalid"); focusAndClear(el);} alert(Array.isArray(msgs)?msgs[0]:String(msgs||"Fix errors.")); return; }
          if (data.html){ replaceModalWithHTML(data.html); const f2=qs("#entity-form"), b2=qs("#modal-save-btn"); prepareFormValidation(f2,b2); wirePasswordEyes(qs("#entity-modal")); dedupePasswordEyes(qs("#entity-modal")); reMaskPasswords(qs("#entity-modal")); return; }
          alert("Validation failed."); return;
        }
        const text = await res.text().catch(()=> "");
        if (text && /id=["']entity-modal["']/.test(text)){
          replaceModalWithHTML(text); const f2=qs("#entity-form"), b2=qs("#modal-save-btn"); prepareFormValidation(f2,b2); wirePasswordEyes(qs("#entity-modal")); dedupePasswordEyes(qs("#entity-modal")); reMaskPasswords(qs("#entity-modal")); return;
        }
        alert("Server returned unexpected response. Reloading..."); location.reload();
      })
      .catch(err=>{ console.error("Submission failed:", err); alert("Submission failed. Check console."); })
      .finally(()=>{ btn.disabled=false; btn.classList.remove("save-disabled"); btn.textContent=prev||"Save"; });
    });
  }

  // exports
  window.isValidDateDDMMYYYY = isValidDateDDMMYYYY;
  window.attachDateMask = attachDateMask;
  window.initializeDatePickers = initializeDatePickers;
  window.formatDateFields = formatDateFields;
  window.addMasks = addMasks;
  window.initPhoneInputs = initPhoneInputs;
  window.setupPermissionSelectAll = setupPermissionSelectAll;
  window.setupRoleSwitches = setupRoleSwitches;
  window.ensureFormErrorBox = ensureFormErrorBox;
  window.showFormErrors = showFormErrors;
  window.markFieldInvalid = markFieldInvalid;
  window.clearFieldErrors = clearFieldErrors;
  window.locateField = locateField;
  window.prepareFormValidation = prepareFormValidation;
  window.recomputeSaveEnabled = recomputeSaveEnabled;
  window.setupSaveButtonHandler = setupSaveButtonHandler;

  // DOM READY phase 2
  document.addEventListener("DOMContentLoaded", function (){
    initializeDatePickers(); setupPermissionSelectAll(); formatDateFields(); addMasks(); initPhoneInputs();
    setupSaveButtonHandler();
    const f=qs("#entity-form"), b=qs("#modal-save-btn"); if (f && b) prepareFormValidation(f,b);
  });
})();
