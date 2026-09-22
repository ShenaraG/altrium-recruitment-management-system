// ============================================================
// ALTRIUM - Login Logic with Role-Based Routing
// ARMS-1 (Login) + ARMS-2,3,4,5 (RBAC routing)
// ============================================================

const ROLE_ROUTES = {
  hr_recruiter:   "dashboards/hr-dashboard.html",
  interviewer:    "dashboards/interviewer-dashboard.html",
  hiring_manager: "dashboards/hiring-manager-dashboard.html",
  management:     "dashboards/management-dashboard.html",
};

function showMessage(text, type) {
  const box = document.getElementById("message");
  if (!box) return;

  box.textContent = text;
  box.className = `message-box ${type}`;
  box.style.display = "block";
}

function setLoading(isLoading) {
  const btn = document.getElementById("loginBtn");
  if (!btn) return;

  btn.disabled = isLoading;
  btn.textContent = isLoading ? "Logging in…" : "LOGIN";
}

window.addEventListener("DOMContentLoaded", async () => {
  const emailInput = document.getElementById("email");
  const rememberMeCheckbox = document.getElementById("rememberMe");

  if (emailInput && rememberMeCheckbox) {
    const rememberedEmail = localStorage.getItem("rememberedEmail");
    if (rememberedEmail) {
      emailInput.value = rememberedEmail;
      rememberMeCheckbox.checked = true;
    }
  }

  const { data: { session } } = await supabaseClient.auth.getSession();
  if (session) {
    const role = localStorage.getItem("userRole");
    if (role && ROLE_ROUTES[role]) {
      window.location.href = ROLE_ROUTES[role];
    }
  }
});

document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const rememberMeCheckbox = document.getElementById("rememberMe");

  if (!emailInput || !passwordInput || !rememberMeCheckbox) {
    return;
  }

  const email = emailInput.value.trim();
  const password = passwordInput.value;

  if (!email || !password) {
    showMessage("Please fill in all fields.", "error");
    return;
  }

  setLoading(true);
  showMessage("Logging in…", "loading");

  const { data: authData, error: authError } =
    await supabaseClient.auth.signInWithPassword({ email, password });

  if (authError) {
    showMessage("Invalid email or password.", "error");
    setLoading(false);
    return;
  }

  const userId = authData.user.id;

  const { data: roleData, error: roleError } = await supabaseClient
    .from("user_roles")
    .select("role_id")
    .eq("user_id", userId)
    .single();

  if (roleError || !roleData) {
    await supabaseClient.auth.signOut();
    showMessage("Access denied. No role assigned.", "error");
    setLoading(false);
    return;
  }

  const { data: roleInfo, error: roleInfoError } = await supabaseClient
    .from("roles")
    .select("role_name")
    .eq("id", roleData.role_id)
    .single();

  if (roleInfoError || !roleInfo) {
    await supabaseClient.auth.signOut();
    showMessage("Access denied. Role not found.", "error");
    setLoading(false);
    return;
  }

  const roleName = roleInfo.role_name;

  if (!ROLE_ROUTES[roleName]) {
    await supabaseClient.auth.signOut();
    showMessage("Access denied. Unrecognised role.", "error");
    setLoading(false);
    return;
  }

  localStorage.setItem("userId", userId);
  localStorage.setItem("userEmail", authData.user.email);
  localStorage.setItem("userRole", roleName);

  if (rememberMeCheckbox.checked) {
    localStorage.setItem("rememberedEmail", email);
  } else {
    localStorage.removeItem("rememberedEmail");
  }

  showMessage("Login successful! Redirecting…", "success");
  setTimeout(() => {
    window.location.href = ROLE_ROUTES[roleName];
  }, 900);
});