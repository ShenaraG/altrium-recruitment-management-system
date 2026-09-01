// ============================================================
// ALTRIUM - Auth Guard
// Include this script at the TOP of every dashboard page.
// It checks the session + role before the page renders.
// ============================================================

// Each dashboard declares which role is allowed, e.g.:
//   <script>const REQUIRED_ROLE = "hr_recruiter";</script>
//   <script src="../js/auth-guard.js"></script>

(async () => {
  // 1. Check active Supabase session
  const { data: { session } } = await supabaseClient.auth.getSession();

  if (!session) {
    // Not logged in at all → back to login
    window.location.href = "../index.html";
    return;
  }

  // 2. Check localStorage role matches the required role for this page
  const storedRole = localStorage.getItem("userRole");

  if (!storedRole || storedRole !== REQUIRED_ROLE) {
    // Wrong role trying to access this dashboard
    window.location.href = "../index.html";
    return;
  }

  // 3. Double-check role against database (prevents localStorage tampering)
  // REPLACE WITH THIS
const { data: roleData, error } = await supabaseClient
    .from("user_roles")
    .select("role_id")
    .eq("user_id", session.user.id)
    .single();

if (error || !roleData) {
    await supabaseClient.auth.signOut();
    localStorage.clear();
    window.location.href = "../index.html";
    return;
}

const { data: roleInfo } = await supabaseClient
    .from("roles")
    .select("role_name")
    .eq("id", roleData.role_id)
    .single();

if (!roleInfo || roleInfo.role_name !== REQUIRED_ROLE) {
    await supabaseClient.auth.signOut();
    localStorage.clear();
    window.location.href = "../index.html";
    return;
}

  // 4. All checks passed – populate header user info
  function populateHeaderUserInfo() {
    const emailEl = document.getElementById("userEmail");
    const roleEl  = document.getElementById("userRoleDisplay");

    if (emailEl) {
      const email = localStorage.getItem("userEmail") || "";
      const displayName = email
        ? email.split("@")[0]
            .replace(/\./g, " ")
            .replace(/\b\w/g, l => l.toUpperCase())
        : "User";
      emailEl.textContent = displayName;
    }

    if (roleEl) roleEl.textContent = formatRole(storedRole);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", populateHeaderUserInfo);
  } else {
    populateHeaderUserInfo();
  }
})();

// ── Logout helper (called by every dashboard's logout button) ─
async function logout() {
  await supabaseClient.auth.signOut();
  localStorage.clear();
  window.location.href = "../index.html";
}

// ── Readable role label ───────────────────────────────────────
function formatRole(role) {
  const labels = {
    hr_recruiter:   "HR Recruiter",
    interviewer:    "Interviewer",
    hiring_manager: "Hiring Manager",
    management:     "Management",
  };
  return labels[role] || role;
}