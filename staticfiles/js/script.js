// ========== DOM READY ========== //
document.addEventListener("DOMContentLoaded", function () {
    ensureSidebarClickCSS();     // ← keeps click-only sidebar behaviour
    ensureImagePreviewModal();   // 🔄 make sure preview modal exists

    const toggleBtn  = document.getElementById("sidebar-toggle");
    const sidebar    = document.getElementById("sidebar");
    const adminLink  = document.getElementById("admin-login-toggle");
    const loginModal = document.getElementById("login-modal");

    let loginClickedOnce = false;

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", function () {
            sidebar.classList.toggle("collapsed");
            const content = document.querySelector(".admin-main-content");
            if (content) {
                content.style.marginLeft = sidebar.classList.contains("collapsed") ? "0" : "250px";
            }
        });
    }

    if (adminLink) {
        // robust text check (icons/whitespace safe)
        adminLink.addEventListener("click", function (e) {
            e.preventDefault();
            const currentText = (adminLink.textContent || "").trim().toLowerCase();

            if (!loginClickedOnce && currentText.includes("admin")) {
                adminLink.textContent = "Login";
                loginClickedOnce = true;
            } else {
                openLoginModal();
            }
        });
    }

    // Generic open entity binding (data-open-entity)
    document.querySelectorAll("[data-open-entity]").forEach(btn => {
        btn.addEventListener("click", function () {
            const ent = btn.dataset.entity;
            if (ent) openEntityModal(ent);
        });
    });

    // Delegated edit entity binding
    document.body.addEventListener("click", function (e) {
        const target = e.target.closest("[data-edit-entity]");
        if (!target) return;
        const entity = target.dataset.editEntity;
        let id = target.dataset.id || target.getAttribute("data-id");
        console.log("Delegated edit click detected:", { entity, id, target });
        if (entity && id) {
            id = String(id).replace(/^:/, ""); // normalize stray colon
            editEntity(entity, id);
        }
    });

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeLoginModal();
    });

    if (loginModal) {
        loginModal.addEventListener("click", function (e) {
            if (e.target === loginModal) closeLoginModal();
        });
    }

    const loginForm = document.querySelector('#admin-login-form');
    if (loginForm && !loginForm.dataset.boundAjaxHandler) {
        // Guard so we don't double-bind later
        loginForm.dataset.boundAjaxHandler = "1";

        // enable/disable Sign in & hide error while typing
        const u = document.getElementById("login-username");
        const p = document.getElementById("login-password");
        const errDiv = document.getElementById("login-error");
        const submitBtn = document.getElementById("login-submit");
        const updateSubmitState = () => {
            const ok = (u && u.value.trim().length > 0) && (p && p.value.trim().length > 0);
            if (submitBtn) ok ? submitBtn.removeAttribute("disabled") : submitBtn.setAttribute("disabled","disabled");
            // Only hide while typing (not immediately after we just showed an error from submit)
            if (document.activeElement === u || document.activeElement === p) {
                if (errDiv) { errDiv.hidden = true; errDiv.style.display = ""; errDiv.textContent = ""; }
            }
        };
        u && u.addEventListener("input", updateSubmitState);
        p && p.addEventListener("input", updateSubmitState);
        updateSubmitState();

        // ===== Primary AJAX submit (hardened to always show error on failure) =====
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(loginForm);

            fetch(loginForm.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData,
                credentials: "include",
                redirect: "follow"
            })
            .then(async res => {
                const ct = (res.headers.get("content-type") || "").toLowerCase();

                // If server redirected (common on auth failure), treat as invalid creds
                if (res.redirected && !ct.includes("application/json")) {
                    console.warn("Redirected response on login (likely invalid creds).");
                    showInlineLoginError("Invalid credentials.");
                    return;
                }

                // Treat 401/400/403 as auth failure with a clear message
                if (res.status === 401 || res.status === 400 || res.status === 403) {
                    showInlineLoginError("Invalid credentials.");
                    return;
                }

                if (ct.includes("application/json")) {
                    const data = await res.json();

                    if (data.success) {
                        closeLoginModal();
                        window.location.href = data.redirect_url || "/dashboard/";
                        return;
                    }

                    // Show OTP if requested
                    if (data.require_otp) {
                        const otpBlock = document.getElementById("otp-block");
                        if (otpBlock) otpBlock.hidden = false;
                    }

                    // Show backend error or fallback
                    showInlineLoginError(data.error || "Invalid credentials.");
                    return;
                }

                // Non-JSON fallback (e.g., Django template HTML on failure)
                const text = await res.text().catch(() => "");
                console.warn("Non-JSON response received (showing inline error):", text.slice(0,200));
                showInlineLoginError("Invalid credentials.");
            })
            .catch(err => {
                console.error("Login error:", err);
                showInlineLoginError("Network error. Please try again.");
            });
        });
    }

    // helpers needed right away
    setupSidebarDropdownToggle();
    setupRoleSwitches();

    // initial helpers (also re-run after loading forms)
    initializeDatePickers();
    setupPermissionSelectAll();
    formatDateFields();
    addMasks();                // ← phone & aadhaar masks
    setupAadharTypeahead();    // ← search-aadhar live filter
    initPhoneInputs();         // ← NEW
    setupSaveButtonHandler();
});

// ===== Helper: force-show login error reliably (JSON/HTML/401/400/403/redirect) ===== //
function showInlineLoginError(msg) {
  const errDiv = document.getElementById("login-error");
  if (!errDiv) return;
  errDiv.textContent = msg || "Invalid credentials.";
  errDiv.hidden = false;          // remove [hidden]
  errDiv.style.display = "block"; // in case CSS tries to hide it
  errDiv.setAttribute("role", "alert");
  errDiv.setAttribute("aria-live", "assertive");
}

// ===== NEW helper: make sure the click-only CSS rule is present ===== //
function ensureSidebarClickCSS() {
    if (document.getElementById("force-sidebar-open-css")) return;
    const style = document.createElement("style");
    style.id = "force-sidebar-open-css";
    style.textContent = ".sidebar .dropdown.open > .dropdown-menu{display:block!important;}";
    document.head.appendChild(style);
}

/* intercept <a class="image-link"> so we open the preview instantly */
document.body.addEventListener("click", function (e) {
    const link = e.target.closest(".image-link");
    if (!link) return;
    e.preventDefault();

    let src = link.getAttribute("href") || "";
    if (src && !src.startsWith("/") && !src.startsWith("http")) src = "/media/" + src;

    const meta = {
        code:   link.dataset.code   || "",
        name:   link.dataset.name   || "",
        status: link.dataset.status || ""
    };

    const modal = document.getElementById("image-preview-modal");
    const img   = document.getElementById("image-preview");
    const info  = document.getElementById("image-meta-fields");

    if (img)  img.src = src;
    if (info) {
        const out = [];
        if (meta.code)   out.push(`<p><strong>Code:</strong> ${meta.code}</p>`);
        if (meta.name)   out.push(`<p><strong>Name:</strong> ${meta.name}</p>`);
        if (meta.status) out.push(`<p><strong>Status:</strong> ${meta.status}</p>`);
        info.innerHTML = out.join("");
    }
    if (modal) modal.style.display = "flex";
});


// ===== ensure the preview modal HTML exists ===== //
function ensureImagePreviewModal() {
    if (document.getElementById("image-preview-modal")) return;
    const modal = document.createElement("div");
    modal.id = "image-preview-modal";
    modal.className = "modal";
    modal.style.display = "none";
    modal.innerHTML = `
      <div class="modal-content image-modal">
        <div class="modal-header d-flex justify-content-between align-items-center mb-2">
          <h5 class="modal-title">Image Preview</h5>
          <button type="button" class="close-btn" onclick="closeImageModal()">&times;</button>
        </div>
        <div class="modal-body">
          <img id="image-preview" src="" alt="Preview"
               style="max-width:100%;max-height:400px;display:block;margin:0 auto 20px;">
          <div id="image-meta-fields"></div>
          <div class="d-flex justify-content-end mt-3">
            <button class="btn btn-secondary" onclick="closeImageModal()">Close</button>
          </div>
        </div>
      </div>`;
    document.body.appendChild(modal);
}

// ===== Helpers ===== //
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ===== Flatpickr Setup ===== //
function initializeDatePickers() {
    if (typeof flatpickr !== "undefined") {
        flatpickr(".date-field", {
            dateFormat: "d/m/Y",
            allowInput: true,
            altInput: false
        });
    }
}

function formatDateFields() {
    document.querySelectorAll("input.date-field").forEach(input => {
        if (input.value.includes("-")) {
            const [yyyy, mm, dd] = input.value.split("-");
            input.value = `${dd}/${mm}/${yyyy}`;
        }
        input.pattern = "\\d{2}/\\d{2}/\\d{4}";
        input.placeholder = "dd/mm/yyyy";
        input.type = "text";
    });
}

/* ===== Phone & Aadhaar live masks ===== */
function addMasks() {
    document.querySelectorAll('input[name="phone"]').forEach(el => {
        el.addEventListener('input', () => {
            el.value = el.value.replace(/\D/g,'').slice(0,10);
        });
    });
    document.querySelectorAll('input[name="aadhar"], #id_aadhar_number').forEach(el => {
        el.addEventListener('input', () => {
            const v = el.value.replace(/\D/g,'').slice(0,12);
            el.value = v.replace(/(\d{4})(?=\d)/g, "$1 ").trim();
        });
    });
}

/* ===== intl-tel-input initialiser ===== */
function initPhoneInputs() {
    if (typeof window.intlTelInput === "undefined") return;
    document.querySelectorAll('input[name="phone"]').forEach(inp => {
        if (inp.dataset.itiAttached) return;
        window.intlTelInput(inp, {
            separateDialCode: true,
            initialCountry: "in",
            preferredCountries: ["in","us","ae","gb"]
        });
        inp.dataset.itiAttached = "1";
        inp.addEventListener("input", () => {
            inp.value = inp.value.replace(/\D/g,'').slice(0,10);
        });
    });
}

/* ===== Client-joining Aadhaar type-ahead ===== */
function setupAadharTypeahead() {
    const aadharInput = document.getElementById('search-aadhar');
    if (!aadharInput) return;
    aadharInput.addEventListener('keyup', function () {
        const q = this.value.replace(/\D/g,'').slice(0,12);
        const tgt = document.getElementById('aadhar-results');
        if (q.length < 2) { if (tgt) tgt.innerHTML = ""; return; }
        fetch(`/search/client/aadhar/?q=${q}`, {
            headers: { "X-Requested-With": "XMLHttpRequest" }
        })
        .then(r => r.json())
        .then(list => {
            if (!tgt) return;
            tgt.innerHTML = list.map(
              c => `<li data-id="${c.id}" onclick="loadClient(${c.id})">${c.aadhar} – ${c.name}</li>`
            ).join('');
        })
        .catch(err => console.error("Aadhaar search error:", err));
    });
}

/* Dummy stub */
function loadClient(id){ console.log("loadClient stub", id); }

// Prevent multiple Aadhar listeners
let _aadharListenerAdded = false;
function formatAadharInput() {
    if (_aadharListenerAdded) return;
    _aadharListenerAdded = true;
    document.addEventListener("input", function (e) {
        const input = e.target;
        if (input && input.id === "id_aadhar_number") {
            let raw = input.value.replace(/\D/g, "").slice(0, 12);
            input.value = raw.replace(/(.{4})(?=.)/g, "$1 ").trim();
        }
    });
}

function setupPermissionSelectAll() {
    document.querySelectorAll('.check-all').forEach(selectAllCheckbox => {
        const group = selectAllCheckbox.dataset.group;
        const groupCheckboxes = document.querySelectorAll(`.form-check-input.${group}`);

        selectAllCheckbox.addEventListener('change', function () {
            groupCheckboxes.forEach(cb => cb.checked = this.checked);
        });

        groupCheckboxes.forEach(cb => {
            cb.addEventListener('change', function () {
                const allChecked = Array.from(groupCheckboxes).every(c => c.checked);
                selectAllCheckbox.checked = allChecked;
            });
        });
    });
}

// === Role-level auto-permission switches === //
function setupRoleSwitches() {
    const master = document.getElementById('role-master-switch');
    const staff  = document.getElementById('role-staff-switch');
    const report = document.getElementById('role-report-switch');
    if (!master || !staff || !report) return;

    // All permission checkboxes
    const checkboxes = Array.from(document.querySelectorAll('.perm-checkbox'));

    // Buckets by feature
    const loanAppPerms   = checkboxes.filter(cb => cb.dataset.perm?.includes('loanapplication'));
    const fieldSchedPerm = checkboxes.filter(cb => cb.dataset.perm?.includes('fieldschedule'));
    const fieldRepPerm   = checkboxes.filter(cb => cb.dataset.perm?.includes('fieldreport'));

    const clearAll = () => {
        checkboxes.forEach(cb => { cb.checked = false; cb.disabled = false; });
    };

    // MASTER → select everything, unlock all, uncheck others
    master.addEventListener('change', () => {
        clearAll();
        if (master.checked) {
            checkboxes.forEach(cb => cb.checked = true);
            staff.checked = report.checked = false;
        }
    });

    // STAFF → only loan application perms (locked), uncheck others
    staff.addEventListener('change', () => {
        clearAll();
        if (staff.checked) {
            loanAppPerms.forEach(cb => { cb.checked = true; cb.disabled = true; });
            master.checked = report.checked = false;
        }
    });

    // REPORT → only field schedule + field report perms (locked), uncheck others
    report.addEventListener('change', () => {
        clearAll();
        if (report.checked) {
            [...fieldSchedPerm, ...fieldRepPerm].forEach(cb => { cb.checked = true; cb.disabled = true; });
            master.checked = staff.checked = false;
        }
    });
}


// === Sidebar dropdown click-toggle === //
function setupSidebarDropdownToggle() {
  const dropdowns = Array.from(document.querySelectorAll(".sidebar .dropdown"));
  dropdowns.forEach(dd => {
    const link = dd.querySelector(":scope > a");
    if (!link) return;
    link.addEventListener("click", e => {
      e.preventDefault();
      dropdowns.forEach(d => { if (d !== dd) d.classList.remove("open"); });
      dd.classList.toggle("open");
    });
  });
  document.addEventListener("click", e => {
    if (!e.target.closest(".sidebar")) {
      dropdowns.forEach(d => d.classList.remove("open"));
    }
  });
}

// === Entity path helper === //
function getEntityBase() {
    let p = window.location.pathname;
    if (!p.endsWith('/')) p += '/';
    return p;
}

// ===== Modal Skeleton Builder ===== //
function ensureModalSkeleton() {
    if (document.getElementById("entity-modal")) return;
    const modal = document.createElement("div");
    modal.id = "entity-modal";
    modal.className = "modal";
    modal.style.display = "none";
    modal.innerHTML = `
      <div class="modal-content">
        <div class="modal-header" style="margin-bottom:12px;">
          <h5 id="entity-modal-title" class="modal-title"></h5>
          <button type="button" class="close-btn" onclick="closeEntityModal()">&times;</button>
        </div>
        <div class="modal-body">
          <div id="form-errors"></div>
          <div id="entity-modal-body"></div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" onclick="closeEntityModal()">Close</button>
          <button id="modal-save-btn" class="btn btn-primary">Save</button>
        </div>
      </div>`;
    document.body.appendChild(modal);
}

// ===== Modal Save Logic ===== //
function setupSaveButtonHandler() {
    const saveBtn = document.getElementById("modal-save-btn");
    if (!saveBtn) return;
    const freshSave = saveBtn.cloneNode(true);
    saveBtn.parentNode.replaceChild(freshSave, saveBtn);
    freshSave.addEventListener("click", function (e) {
        e.preventDefault();
        const form = document.getElementById("entity-form");
        if (!form) return;
        const url = form.action;
        const formData = new FormData(form);
        const errorDiv = document.getElementById("form-errors");
        if (errorDiv) errorDiv.innerHTML = "";
        freshSave.disabled = true;
        freshSave.textContent = "Saving...";
        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData,
            credentials: "include"
        })
        .then(async (res) => {
            const ct = res.headers.get("content-type") || "";
            if (res.status === 401) { alert("Authentication required."); return; }
            if (ct.includes("application/json")) {
                const data = await res.json();
                if (data.success) {
                    closeEntityModal();
                    location.reload();
                } else {
                    showFormErrors(data.errors || {});
                }
            } else {
                const text = await res.text();
                console.error("Non-JSON response received:", text);
                alert("Server returned unexpected response. Reloading...");
                location.reload();
            }
        })
        .catch(err => {
            console.error("Submission failed:", err);
            alert("Submission failed. Check console.");
        })
        .finally(() => {
            freshSave.disabled = false;
            freshSave.textContent = "Save";
        });
    });
}

function showFormErrors(errors) {
    const errorDiv = document.getElementById("form-errors");
    if (!errorDiv) return;
    errorDiv.innerHTML = "";
    for (let field in errors) {
        const msgs = Array.isArray(errors[field]) ? errors[field].join(", ") : errors[field];
        errorDiv.innerHTML += `<p><strong>${field}:</strong> ${msgs}</p>`;
    }
}

// ===== Utility ===== //
function prettyName(entity) {
    return entity.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}

/* ===== Auto-code filler ===== */
function fillAutoCode(entity) {
    const codeInput = document.querySelector('#entity-form input[name="code"]');
    if (!codeInput || codeInput.value) return;
    fetch("/next_code/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `entity=${encodeURIComponent(entity)}`,
        credentials: "include"
    })
    .then(r => r.json())
    .then(data => { if (data.code) codeInput.value = data.code; })
    .catch(err => console.error("code-fetch error:", err));
}

// ===== Centralized Modal Injection ===== //
function insertEntityModal(entity, html, mode, id) {
    const base = getEntityBase();
    const temp = document.createElement("div");
    temp.innerHTML = html.trim();
    const returnedModal = temp.querySelector("#entity-modal");
    if (returnedModal) {
        const existing = document.getElementById("entity-modal");
        if (existing) existing.remove();
        document.body.appendChild(returnedModal);
        const titleEl = returnedModal.querySelector("#entity-modal-title");
        if (titleEl) titleEl.innerText = `${mode} ${prettyName(entity)}`;
        const form = returnedModal.querySelector("#entity-form");
        if (form) {
            form.dataset.entity = entity;
            if (mode === "Create") form.action = `${base}create/`;
            else if (mode === "Edit") form.action = `${base}update/${String(id).replace(/^:/, "")}/`;
        }
    } else {
        ensureModalSkeleton();
        const modal = document.getElementById("entity-modal");
        const title = document.getElementById("entity-modal-title");
        const bodyContainer = document.getElementById("entity-modal-body");
        if (!modal || !title || !bodyContainer) return;
        title.innerText = `${mode} ${prettyName(entity)}`;
        bodyContainer.innerHTML = html;
        modal.style.display = "flex";
        const form = document.getElementById("entity-form");
        if (form) {
            form.dataset.entity = entity;
            if (mode === "Create") form.action = `${base}create/`;
            else if (mode === "Edit") form.action = `${base}update/${String(id).replace(/^:/, "")}/`;
            if (mode === "Create") {
                const today = new Date();
                const formatted = `${String(today.getDate()).padStart(2, "0")}/${String(today.getMonth() + 1).padStart(2, "0")}/${today.getFullYear()}`;
                form.querySelectorAll("input.date-field").forEach(input => input.value = formatted);
            }
        }
    }
    const modalToShow = document.getElementById("entity-modal");
    if (modalToShow) modalToShow.style.display = "flex";
    initializeDatePickers();
    setupPermissionSelectAll();
    formatDateFields();
    addMasks();
    setupAadharTypeahead();
    formatAadharInput();
    initPhoneInputs();
    fillAutoCode(entity);
    setupSaveButtonHandler();
    setupRoleSwitches();
}

// ===== Open / Edit Entity ===== //
function openEntityModal(entityOrEvent) {
    let entity;
    if (typeof entityOrEvent === "string") {
        entity = entityOrEvent;
    } else if (entityOrEvent && entityOrEvent.currentTarget) {
        const el = entityOrEvent.currentTarget;
        entity = el.dataset.entity || el.getAttribute("data-entity");
    }
    if (!entity) {
        console.error("No entity provided to openEntityModal");
        return;
    }
    const base = getEntityBase();
    const url = `${base}get/`;
    fetch(url, { headers:{"X-Requested-With":"XMLHttpRequest"}, credentials:"include" })
    .then(async res => {
        if (res.status === 401) { alert("Authentication required."); return; }
        const ct = res.headers.get("content-type") || "";
        let html;
        if (ct.includes("application/json")) {
            const data = await res.json();
            if (!data.success) { alert(data.error || "Could not load form."); return; }
            html = data.html;
        } else {
            const text = await res.text();
            if (res.status === 404) { alert("Form endpoint not found."); return; }
            if (text.toLowerCase().includes("login")) { alert("Not authenticated."); return; }
            html = text;
        }
        insertEntityModal(entity, html, "Create");
    })
    .catch(err => {
        console.error("Load create form error:", err);
        alert("Failed to load create form.");
    });
}

function editEntity(entity, id) {
    if (!entity || !id) { console.error("editEntity requires entity and id"); return; }
    id = String(id).replace(/^:/, "");
    const base = getEntityBase();
    const url = `${base}get/${id}/`;
    fetch(url, { headers:{"X-Requested-With":"XMLHttpRequest"}, credentials:"include" })
    .then(async res => {
        if (res.status === 401) { alert("Authentication required."); return; }
        const ct = res.headers.get("content-type") || "";
        let html;
        if (ct.includes("application/json")) {
            const data = await res.json();
            if (!data.success) { alert(data.error || "Could not load form."); return; }
            html = data.html;
        } else {
            const text = await res.text();
            if (res.status === 404) { alert("Edit form endpoint not found."); return; }
            if (text.toLowerCase().includes("login")) { alert("Not authenticated."); return; }
            html = text;
        }
        insertEntityModal(entity, html, "Edit", id);
    })
    .catch(err => {
        console.error("Edit load error:", err);
        alert("Failed to load data.");
    });
}

function closeEntityModal() {
    const modal = document.getElementById("entity-modal");
    if (modal) modal.style.display = "none";
}

// ===== Delete ===== //
function deleteEntity(entity, id) {
  if (!confirm("Delete this record?")) return;

  const base = getEntityBase();       // e.g. "/userprofile/"
  id = String(id).replace(/^:/, "");
  const url = `${base}delete/${id}/`; // matches your urls.py

  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      "X-Requested-With": "XMLHttpRequest"
    },
    credentials: "include"
  })
  .then(async res => {
    const ct = (res.headers.get("content-type") || "").toLowerCase();
    // Quick debug so we see what's coming back
    console.log("DELETE status:", res.status, "content-type:", ct, "url:", url);

    // If server sent HTML (error page), do NOT try to parse JSON
    if (!ct.includes("application/json")) {
      const text = await res.text().catch(() => "");
      console.error("Non-JSON response:", text.slice(0, 400));
      alert("Delete failed (server returned an HTML error). Check console.");
      return;
    }

    const data = await res.json();

    if (res.status === 401) {
      alert("Please log in again.");
      return;
    }

    if (data.success) {
      location.reload();
      return;
    }

    const extras = data.blocked_by
      ? "\nBlocked by: " + Object.entries(data.blocked_by).map(([m, c]) => `${m} (${c})`).join(", ")
      : "";
    alert((data.error || "Delete failed.") + extras);
  })
  .catch(err => {
    console.error("Delete network error:", err);
    alert("Network error during delete.");
  });
}


/* ===== Fresh login modal state helper ===== */
function resetLoginModalState() {
    const u = document.getElementById("login-username");
    const p = document.getElementById("login-password");
    const otpBlock = document.getElementById("otp-block");
    const err = document.getElementById("login-error");
    const submitBtn = document.getElementById("login-submit");

    // Clear fields
    if (u) { u.value = ""; u.setAttribute("readonly","readonly"); }
    if (p) { p.value = ""; p.setAttribute("readonly","readonly"); }

    // Re-arm unlock on user intent
    [u,p].forEach(el => {
        if (!el) return;
        const unlock = () => el.removeAttribute("readonly");
        ["focus","keydown","pointerdown"].forEach(ev =>
          el.addEventListener(ev, function handler(){ unlock(); el.removeEventListener(ev, handler); }, { once:true })
        );
    });

    // Hide OTP + Error
    if (otpBlock) otpBlock.hidden = true;
    if (err) { err.hidden = true; err.style.display = ""; err.textContent = ""; }

    // Disable submit until typing
    if (submitBtn) submitBtn.setAttribute("disabled","disabled");
}

// ===== Login Modal ===== //
function openLoginModal() {
    const loginModal = document.getElementById("login-modal");
    if (loginModal) {
        resetLoginModalState();                 // ← ensure fresh every time
        loginModal.classList.add("show");
        loginModal.style.display = "flex";
        const u = document.getElementById("login-username");
        if (u) setTimeout(()=>u.focus(), 0);
    }
}
function closeLoginModal() {
    const loginModal = document.getElementById("login-modal");
    if (loginModal) {
        loginModal.classList.remove("show");
        loginModal.style.display = "none";
        resetLoginModalState();                 // ← prepare next open as fresh
    }
}

// ===== Image Preview ===== //
function openImageModal(id, entity, field) {
    ensureImagePreviewModal();
    const modal         = document.getElementById("image-preview-modal");
    const imageTag      = document.getElementById("image-preview");
    const metaContainer = document.getElementById("image-meta-fields");

    if (imageTag) imageTag.src = "";
    if (metaContainer) metaContainer.innerHTML = "";

    id = String(id).replace(/^:/, "");
    const url = `${getEntityBase()}get/${id}/`;
    fetch(url, { headers:{"X-Requested-With":"XMLHttpRequest"}, credentials:"include" })
    .then(async res => {
        if (res.status === 401) { alert("Authentication required."); return; }

        const ct = res.headers.get("content-type") || "";
        let data = {};
        if (ct.includes("application/json")) {
            data = await res.json();
        } else {
            const text = await res.text();
            data[field] = text.trim();
        }

        let img = data[field];
        if (img && typeof img === "object") img = img.url || img.path || "";
        if (!img) { alert("Image not available."); return; }
        if (!img.startsWith("/") && !img.startsWith("http")) img = `/media/${img}`;
        imageTag.src = img;

        const lines = [];
        if (data.code)   lines.push(`<p><strong>Code:</strong> ${data.code}</p>`);
        if (data.name)   lines.push(`<p><strong>Name:</strong> ${data.name}</p>`);
        if (data.status) lines.push(`<p><strong>Status:</strong> ${data.status}</p>`);
        metaContainer.innerHTML = lines.join("");
        modal.style.display = "flex";
    })
    .catch(err => {
        console.error("Image preview error:", err);
        alert("Failed to load image preview.");
    });
}

function closeImageModal() {
    const modal = document.getElementById("image-preview-modal");
    if (modal) modal.style.display = "none";
}

// === expose globally for inline handlers ===
window.openEntityModal  = openEntityModal;
window.editEntity       = editEntity;
window.deleteEntity     = deleteEntity;
window.closeEntityModal = closeEntityModal;
window.openImageModal   = openImageModal;
window.closeImageModal  = closeImageModal;

// === Pro Login UX — additive, preserves previous logic ===
document.addEventListener("DOMContentLoaded", function () {
  const form  = document.getElementById("admin-login-form");
  const modal = document.getElementById("login-modal");
  if (!form || !modal) return;

  const u = document.getElementById("login-username");
  const p = document.getElementById("login-password");
  const otpBlock = document.getElementById("otp-block");
  const otp = document.getElementById("login-otp");
  const err = document.getElementById("login-error");
  const submitBtn = document.getElementById("login-submit");
  const caps = document.getElementById("caps-warning");

  // Ensure we always use flex (matches CSS) and always reset to fresh
  window.openLoginModal = function () {
    resetLoginModalState();      // ← fresh before opening
    modal.classList.add("show");
    modal.style.display = "flex";
    setTimeout(() => u && u.focus(), 0);
  };

  window.closeLoginModal = window.closeLoginModal || function () {
    modal.classList.remove("show");
    modal.style.display = "none";
    resetLoginModalState();      // ← prepare fresh for next open
  };

  // Enter-to-submit from anywhere in the form
  form.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      submitBtn && submitBtn.click();
    }
  });

  // Caps Lock hint
  ["keydown","keyup"].forEach(ev => {
    p && p.addEventListener(ev, e => {
      if (e.getModifierState && e.getModifierState("CapsLock")) { caps.hidden = false; }
      else { caps.hidden = true; }
    });
  });

  function setLoading(on) {
    if (!submitBtn) return;
    if (on) { submitBtn.classList.add("loading"); submitBtn.setAttribute("disabled","disabled"); }
    else    { submitBtn.classList.remove("loading"); /* inputs control enable state */ }
  }
  function showErr(msg) {
    showInlineLoginError(msg || "Login failed."); // unify single show method
  }
  function clearErr() {
    if (err) { err.hidden = true; err.style.display = ""; err.textContent = ""; }
  }

  if (!form.dataset.enhancedSubmit) {
    form.dataset.enhancedSubmit = "1";
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      clearErr();
      setLoading(true);

      try {
        const res = await fetch(form.action, {
          method: "POST",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken")
          },
          body: new FormData(form),
          credentials: "include",
          redirect: "follow"
        });

        // Handle auth failures even if server doesn't return JSON
        if (res.redirected && !(res.headers.get("content-type") || "").toLowerCase().includes("application/json")) {
          setLoading(false);
          showErr("Invalid credentials.");
          return;
        }
        if (res.status === 401 || res.status === 400 || res.status === 403) {
          setLoading(false);
          showErr("Invalid credentials.");
          return;
        }

        if ((res.headers.get("content-type") || "").toLowerCase().includes("application/json")) {
          const data = await res.json();

          if (data.require_otp) {
            otpBlock.hidden = false;
            otp && otp.focus();
            setLoading(false);
            return;
          }

          if (data.success) {
            window.location.href = data.redirect_url || data.redirect || "/dashboard/";
          } else {
            setLoading(false);
            showErr(data.error || "Invalid credentials.");
          }
        } else {
          // Non-JSON fallback: keep modal, show inline error
          setLoading(false);
          showErr("Invalid credentials.");
        }
      } catch (ex) {
        console.error("Login error:", ex);
        setLoading(false);
        showErr("Network error. Please try again.");
      }
    });
  }

  // Hide error and control submit enable while typing
  function updateSubmitState(){
    const ok = (u && u.value.trim().length>0) && (p && p.value.trim().length>0);
    if (ok) submitBtn && submitBtn.removeAttribute("disabled");
    else    submitBtn && submitBtn.setAttribute("disabled","disabled");
    // Do not nuke an error that was just shown by submit; only clear while actually typing
    if (document.activeElement === u || document.activeElement === p) {
      clearErr();
    }
  }
  u && u.addEventListener("input", updateSubmitState);
  p && p.addEventListener("input", updateSubmitState);
  updateSubmitState();
});

/* ===== Bulletproof password visibility toggle (icon-based) ===== */
function eyeSVG(){ return '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7Z"></path><circle cx="12" cy="12" r="3"></circle></svg>'; }
function eyeOffSVG(){ return '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17.94 17.94A10.94 10.94 0 0 1 12 20C5 20 1 12 1 12A21.78 21.78 0 0 1 7.05 5.05"></path><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"></path><path d="M1 1l22 22"></path></svg>'; }

document.addEventListener("click", function (e) {
  const btn = e.target.closest("[data-toggle-pass]");
  if (!btn) return;

  e.preventDefault();
  e.stopPropagation();

  const wrap = btn.closest(".pro-passwrap");
  const input = wrap ? wrap.querySelector('input[type="password"], input[type="text"]') : null;
  if (!input) return;

  const nextType = input.getAttribute("type") === "password" ? "text" : "password";
  input.setAttribute("type", nextType);

  const showing = nextType === "text";
  btn.setAttribute("aria-pressed", showing ? "true" : "false");
  btn.setAttribute("title", showing ? "Hide password" : "Show password");
  btn.innerHTML = showing ? eyeOffSVG() : eyeSVG();

  input.focus();
});

// ultra-safe inline fallback for Show/Hide (kept for backward compatibility, now icon-based)
window.togglePass = function (btn) {
  try {
    const wrap = btn.closest(".pro-passwrap");
    const input = wrap ? wrap.querySelector('input[type="password"], input[type="text"]') : null;
    if (!input) return false;
    const next = input.type === "password" ? "text" : "password";
    input.type = next;
    const showing = next === "text";
    btn.setAttribute("aria-pressed", showing ? "true" : "false");
    btn.setAttribute("title", showing ? "Hide password" : "Show password");
    btn.innerHTML = showing ? eyeOffSVG() : eyeSVG();
    input.focus();
  } catch (e) {
    console.error("togglePass error:", e);
  }
  return false;
};
