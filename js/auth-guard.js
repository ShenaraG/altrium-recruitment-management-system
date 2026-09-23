// ============================================================
// ALTRIUM - Auth Guard
// Include this script at the TOP of every dashboard page.
// It checks the session + role before the page renders.
// ============================================================

// Each dashboard declares which role is allowed, e.g.:
//   <script>const REQUIRED_ROLE = "hr_recruiter";</script>
//   <script src="../js/auth-guard.js"></script>

(async () => {
  const { data: { session } } = await supabaseClient.auth.getSession();

  if (!session) {
    window.location.href = "../index.html";
    return;
  }

  const storedRole = localStorage.getItem("userRole");

  if (!storedRole || storedRole !== REQUIRED_ROLE) {
    window.location.href = "../index.html";
    return;
  }

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

  function populateHeaderUserInfo() {
    const emailEl = document.getElementById("userEmail");
    const roleEl = document.getElementById("userRoleDisplay");
    const avatarEl = document.querySelector(".user-avatar");
    const profiles = {
      hr_recruiter: {
        name: "Sarah",
        image: "https://randomuser.me/api/portraits/women/44.jpg",
        alt: "Sarah, HR Recruiter",
      },
      interviewer: {
        name: "James",
        image: "https://randomuser.me/api/portraits/men/32.jpg",
        alt: "James, Interviewer",
      },
      hiring_manager: {
        name: "Emma",
        image: "https://randomuser.me/api/portraits/women/68.jpg",
        alt: "Emma, Hiring Manager",
      },
      management: {
        name: "Michael",
        image: "https://randomuser.me/api/portraits/men/75.jpg",
        alt: "Michael, HR Director",
      },
    };

    const profile = profiles[storedRole];

    if (emailEl) {
      emailEl.textContent = profile?.name || "User";
    }

    if (roleEl) roleEl.textContent = formatRole(storedRole);
    if (avatarEl && profile) {
      avatarEl.src = profile.image;
      avatarEl.alt = profile.alt;
    }
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
    management:     "HR Director / Management",
  };
  return labels[role] || role;
}