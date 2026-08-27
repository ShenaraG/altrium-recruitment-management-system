// ----------------------------------
// Supabase Configuration
// ----------------------------------


// 4. Add config.js to .gitignore so keys don't leak to GitHub

// ============================================================
// ALTRIUM - Supabase Configuration
// ⚠️ DO NOT commit this file to GitHub (.gitignore covers it)
// ============================================================

const SUPABASE_URL = "https://yupyanaremnbgcgyeltz.supabase.co";   // ← keep your existing URL

const SUPABASE_KEY = "sb_publishable_SKyAjQFf6qpgmcmJejMyuA_2A1A-c8p";   // ← keep your existing key

// window.supabase comes from the CDN script in index.html
const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

console.log("✓ Supabase client initialized");