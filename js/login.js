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
  box.textContent = text;
  box.className = `message-box ${type}`;
  box.style.display = "block";
}

function setLoading(isLoading) {
  const btn = document.getElementById("loginBtn");
  btn.disabled = isLoading;
  btn.textContent = isLoading ? "Logging in…" : "LOGIN";
}

// Redirect if already logged in
window.addEventListener("DOMContentLoaded", async () => {
  const { data: { session } } = await supabaseClient.auth.getSession();
  if (session) {
    const role = localStorage.getItem("userRole");
    if (role && ROLE_ROUTES[role]) {
      window.location.href = ROLE_ROUTES[role];
    }
  }
});

// Login form submit
document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email    = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  if (!email || !password) {
    showMessage("Please fill in all fields.", "error");
    return;
  }

  setLoading(true);
  showMessage("Logging in…", "loading");

  // Step 1: Authenticate
  const { data: authData, error: authError } =
    await supabaseClient.auth.signInWithPassword({ email, password });

  if (authError) {
    showMessage("❌ Invalid email or password.", "error");
    setLoading(false);
    return;
  }

  const userId = authData.user.id;
  console.log("✅ Auth success. userId:", userId);

  // Step 2: Get role_id from user_roles
  const { data: roleData, error: roleError } = await supabaseClient
    .from("user_roles")
    .select("role_id")
    .eq("user_id", userId)
    .single();

  console.log("roleData:", roleData, "roleError:", roleError);

  if (roleError || !roleData) {
    await supabaseClient.auth.signOut();
    showMessage("❌ Access denied. No role assigned.", "error");
    setLoading(false);
    return;
  }

  // Step 3: Get role_name from roles
  const { data: roleInfo, error: roleInfoError } = await supabaseClient
    .from("roles")
    .select("role_name")
    .eq("id", roleData.role_id)
    .single();

  console.log("roleInfo:", roleInfo, "roleInfoError:", roleInfoError);

  if (roleInfoError || !roleInfo) {
    await supabaseClient.auth.signOut();
    showMessage("❌ Access denied. Role not found.", "error");
    setLoading(false);
    return;
  }

  const roleName = roleInfo.role_name;
  console.log("✅ Role found:", roleName);

  if (!ROLE_ROUTES[roleName]) {
    await supabaseClient.auth.signOut();
    showMessage("❌ Access denied. Unrecognised role.", "error");
    setLoading(false);
    return;
  }

  // Step 4: Store and redirect
  localStorage.setItem("userId",    userId);
  localStorage.setItem("userEmail", authData.user.email);
  localStorage.setItem("userRole",  roleName);

  showMessage("Login successful! Redirecting…", "success");
  setTimeout(() => {
    window.location.href = ROLE_ROUTES[roleName];
  }, 900);
});