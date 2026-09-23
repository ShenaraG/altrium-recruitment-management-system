// Supabase Configuration

const SUPABASE_URL = "https://yupyanaremnbgcgyeltz.supabase.co";
const SUPABASE_KEY = "sb_publishable_SKyAjQFf6qpgmcmJejMyuA_2A1A-c8p";

if (!window.supabase) {
  throw new Error("Supabase SDK is required before config.js is loaded.");
}

const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);