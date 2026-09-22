// ----------------------------------
// Supabase Configuration
// ----------------------------------

// ============================================================
// ALTRIUM - Supabase Configuration
//  Local static testing uses a demo client so the dashboard
//  pages still render without a live Supabase session.
// ============================================================

const SUPABASE_URL = "https://yupyanaremnbgcgyeltz.supabase.co";
const SUPABASE_KEY = "sb_publishable_SKyAjQFf6qpgmcmJejMyuA_2A1A-c8p";
const isLocalDemo = ["localhost", "127.0.0.1", "::1"].includes(window.location.hostname);

const demoData = {
  positions: [
    { id: 1, title: "Senior Frontend Engineer", description: "Build and refine the customer-facing web experience.", salary_range: "$120k - $150k", status: "Open", created_at: "2026-01-10T09:00:00Z", retention_date: null, closed_date: null },
    { id: 2, title: "Product Designer", description: "Design workflows and user journeys for a fast-moving product team.", salary_range: "$100k - $130k", status: "Open", created_at: "2026-01-14T09:00:00Z", retention_date: null, closed_date: null },
    { id: 3, title: "Data Analyst", description: "Analyse hiring and operational metrics across the recruitment funnel.", salary_range: "$90k - $120k", status: "Closed", created_at: "2025-12-10T09:00:00Z", retention_date: "2027-01-01", closed_date: "2026-01-01" }
  ],
  candidates: [
    { id: 1, full_name: "Ava Thompson", email: "ava.thompson@example.com", phone: "+1 555 100 001", created_at: "2026-01-01T09:00:00Z" },
    { id: 2, full_name: "Noah Patel", email: "noah.patel@example.com", phone: "+1 555 100 002", created_at: "2026-01-11T09:00:00Z" },
    { id: 3, full_name: "Mila Garcia", email: "mila.garcia@example.com", phone: "+1 555 100 003", created_at: "2026-01-15T09:00:00Z" }
  ],
  candidate_positions: [
    { candidate_id: 1, position_id: 1, status: "Applied", current_stage: 1, created_at: "2026-01-02T09:00:00Z" },
    { candidate_id: 2, position_id: 1, status: "On Hold", current_stage: 2, created_at: "2026-01-12T09:00:00Z" },
    { candidate_id: 3, position_id: 2, status: "Applied", current_stage: 1, created_at: "2026-01-16T09:00:00Z" },
    { candidate_id: 1, position_id: 2, status: "Hired", current_stage: 3, created_at: "2026-01-18T09:00:00Z" }
  ],
  decisions: [
    { id: 1, candidate_id: 1, position_id: 2, status: "Hired", decision_date: "2026-02-01", hiring_manager_name: "demo", hiring_manager_id: "demo-user", created_at: "2026-02-01T09:00:00Z" }
  ],
  feedback: [
    { id: 1, candidate_id: 1, position_id: 1, interviewer_name: "Priya Shah", rating: 4.8, recommendation: "Move to Next Stage", comments: "Strong communication and thoughtful problem-solving examples.", criteria: "Communication, Technical depth, Team fit", version: 2, stage: 1, is_latest: true, created_at: "2026-01-20T09:00:00Z", candidates: { full_name: "Ava Thompson", email: "ava.thompson@example.com" } },
    { id: 2, candidate_id: 2, position_id: 1, interviewer_name: "Lucas Chen", rating: 3.7, recommendation: "On Hold", comments: "Good fundamentals but needs more product experience.", criteria: "Communication, Technical depth, Team fit", version: 1, stage: 2, is_latest: true, created_at: "2026-01-22T09:00:00Z", candidates: { full_name: "Noah Patel", email: "noah.patel@example.com" } },
    { id: 3, candidate_id: 3, position_id: 2, interviewer_name: "Emilia Ross", rating: 4.3, recommendation: "Move to Next Stage", comments: "Excellent clarity and design instincts.", criteria: "Design thinking, Craft, Collaboration", version: 1, stage: 1, is_latest: true, created_at: "2026-01-25T09:00:00Z", candidates: { full_name: "Mila Garcia", email: "mila.garcia@example.com" } }
  ],
  interview_stages: [
    { id: 1, position_id: 1, stage_name: "Application Review", stage_order: 1 },
    { id: 2, position_id: 1, stage_name: "Technical Screen", stage_order: 2 },
    { id: 3, position_id: 2, stage_name: "Portfolio Review", stage_order: 1 }
  ],
  cv_uploads: [
    { id: 1, candidate_id: 1, file_name: "ava_thompson_cv.pdf", file_url: "https://example.com/cv-uploads/ava_thompson_cv.pdf", storage_path: "uploads/ava_thompson_cv.pdf", uploaded_at: "2026-01-20T09:00:00Z" }
  ],
  user_roles: [{ user_id: "demo-user", role_id: 1 }],
  roles: [{ id: 1, role_name: "hiring_manager" }, { id: 2, role_name: "hr_recruiter" }, { id: 3, role_name: "management" }, { id: 4, role_name: "interviewer" }],
  "cv-uploads": []
};

function matchRow(row, filter) {
  const { column, value } = filter;
  return String(row[column]) === String(value);
}

class DemoQuery {
  constructor(table) {
    this.table = table;
    this.filters = [];
    this.orderBy = null;
    this.limitCount = null;
    this.selectFields = null;
    this.options = {};
    this.isSingle = false;
    this.isMaybeSingle = false;
    this.isHead = false;
    this.isDelete = false;
    this.isUpdate = false;
    this.insertValues = null;
  }

  select(fields, options = {}) {
    this.selectFields = fields;
    this.options = options;
    return this;
  }

  eq(column, value) {
    this.filters.push({ type: "eq", column, value });
    return this;
  }

  neq(column, value) {
    this.filters.push({ type: "neq", column, value });
    return this;
  }

  order(column, { ascending = true } = {}) {
    this.orderBy = { column, ascending };
    return this;
  }

  limit(count) {
    this.limitCount = count;
    return this;
  }

  single() {
    this.isSingle = true;
    return this;
  }

  maybeSingle() {
    this.isMaybeSingle = true;
    return this;
  }

  insert(values) {
    this.isUpdate = false;
    this.insertValues = values;
    return this;
  }

  update(values) {
    this.isUpdate = true;
    this.insertValues = values;
    return this;
  }

  delete() {
    this.isDelete = true;
    return this;
  }

  async then(resolve, reject) {
    try {
      const result = await this.execute();
      return resolve ? resolve(result) : result;
    } catch (error) {
      if (reject) return reject(error);
      throw error;
    }
  }

  async execute() {
    const tableData = Array.isArray(demoData[this.table]) ? [...demoData[this.table]] : [];
    let filtered = tableData.filter((row) => {
      return this.filters.every((filter) => {
        const cell = row[filter.column];
        if (filter.type === "eq") return String(cell) === String(filter.value);
        if (filter.type === "neq") return String(cell) !== String(filter.value);
        return true;
      });
    });

    const addNestedRelations = (rows) => rows.map((row) => {
      const nextRow = { ...row };
      const candidate = demoData.candidates?.find(c => Number(c.id) === Number(nextRow.candidate_id));
      const position = demoData.positions?.find(p => Number(p.id) === Number(nextRow.position_id));
      if (candidate) nextRow.candidates = { ...candidate };
      if (position) nextRow.positions = { ...position };
      if (this.table === "feedback" && nextRow.candidate_id != null) {
        const fbCandidate = demoData.candidates?.find(c => Number(c.id) === Number(nextRow.candidate_id));
        if (fbCandidate) nextRow.candidates = { ...fbCandidate };
      }
      if (this.table === "cv_uploads" && nextRow.candidate_id != null) {
        const cvCandidate = demoData.candidates?.find(c => Number(c.id) === Number(nextRow.candidate_id));
        if (cvCandidate) nextRow.candidates = { ...cvCandidate };
      }
      return nextRow;
    });

    if (this.orderBy) {
      filtered.sort((a, b) => {
        const left = a[this.orderBy.column] ?? "";
        const right = b[this.orderBy.column] ?? "";
        const result = String(left).localeCompare(String(right));
        return this.orderBy.ascending ? result : -result;
      });
    }

    if (this.limitCount !== null) {
      filtered = filtered.slice(0, this.limitCount);
    }

    if (this.isDelete) {
      const rows = demoData[this.table] || [];
      demoData[this.table] = rows.filter((row) => !this.filters.every((filter) => {
        const cell = row[filter.column];
        return String(cell) === String(filter.value);
      }));
      return { data: null, error: null };
    }

    if (this.insertValues) {
      const rows = demoData[this.table] || [];
      if (Array.isArray(this.insertValues)) {
        demoData[this.table] = rows.concat(this.insertValues.map((item) => ({ ...item })));
      } else {
        demoData[this.table] = rows.concat([{ ...this.insertValues }]);
      }
      return { data: this.insertValues, error: null };
    }

    if (this.isUpdate) {
      const rows = demoData[this.table] || [];
      demoData[this.table] = rows.map((row) => {
        const matches = this.filters.every((filter) => String(row[filter.column]) === String(filter.value));
        return matches ? { ...row, ...this.insertValues } : row;
      });
      return { data: demoData[this.table], error: null };
    }

    if (this.options.count === "exact" && this.options.head) {
      return { count: filtered.length, data: null, error: null };
    }

    if (this.isSingle || this.isMaybeSingle) {
      return { data: addNestedRelations(filtered)[0] || null, error: null };
    }

    if (this.options.head) {
      return { count: filtered.length, data: null, error: null };
    }

    return { data: addNestedRelations(filtered), error: null };
  }
}

const demoSupabaseClient = {
  auth: {
    async getSession() {
      return { data: { session: null } };
    },
    async signOut() {
      return { error: null };
    },
    async signInWithPassword() {
      return { data: { user: { id: "demo-user", email: "demo.user@altrium.com" } }, error: null };
    }
  },
  from(tableName) {
    return new DemoQuery(tableName);
  },
  storage: {
    from(bucketName) {
      return {
        async upload(filePath) {
          return { data: { path: filePath }, error: null };
        },
        getPublicUrl(filePath) {
          return { data: { publicUrl: `https://example.com/${bucketName}/${filePath}` } };
        },
        async remove() {
          return { data: null, error: null };
        }
      };
    }
  }
};

const supabaseClient = isLocalDemo ? demoSupabaseClient : window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
console.log("✓ Supabase client initialized");