function safeNumber(value, fallback = 0) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

function formatPercentage(value) {
  if (!Number.isFinite(value)) return '—';
  return `${value.toFixed(1)}%`;
}

function calculateOverviewMetrics({ candidates = [], positions = [], candidatePositions = [], decisions = [] }) {
  const totalCandidates = candidates.length;
  const openPositions = positions.filter(pos => pos.status === 'Open' || pos.status === 'open').length;
  const hiredCandidates = candidatePositions.filter(link => String(link.status).toLowerCase() === 'hired').length;
  const pipelineSize = candidatePositions.filter(link => {
    const status = String(link.status || '').toLowerCase();
    return status !== 'hired' && status !== 'rejected' && status !== 'withdrawn';
  }).length;

  const rejectedOrWithdrawn = candidatePositions.filter(link => {
    const status = String(link.status || '').toLowerCase();
    return status === 'rejected' || status === 'withdrawn';
  }).length;
  const totalProgressRecords = candidatePositions.length || totalCandidates;
  const dropoffRate = totalProgressRecords > 0
    ? (rejectedOrWithdrawn / totalProgressRecords) * 100
    : 0;

  const candidateById = new Map((candidates || []).map(candidate => [Number(candidate.id), candidate]));
  const candidatePositionDates = new Map();

  (candidatePositions || []).forEach(link => {
    const candidateId = Number(link.candidate_id);
    const createdAt = link.created_at || null;
    if (!candidatePositionDates.has(candidateId) || (createdAt && !candidatePositionDates.get(candidateId))) {
      candidatePositionDates.set(candidateId, createdAt);
    }
  });

  const hiredDates = decisions
    .filter(d => String(d.status || '').toLowerCase() === 'hired' && d.decision_date)
    .map(d => {
      const candidateId = Number(d.candidate_id);
      const candidate = candidateById.get(candidateId);
      const srcDate = candidate?.created_at || candidatePositionDates.get(candidateId) || d.decision_date;
      const start = new Date(srcDate).getTime();
      const end = new Date(d.decision_date).getTime();
      return Number.isFinite(start) && Number.isFinite(end) ? end - start : null;
    })
    .filter(value => value !== null && Number.isFinite(value));

  const avgTimeToHireDays = hiredDates.length
    ? hiredDates.reduce((sum, ms) => sum + ms, 0) / hiredDates.length / 86400000
    : null;

  const positionSummary = positions.map(position => {
    const linked = candidatePositions.filter(link => Number(link.position_id) === Number(position.id));
    const hired = linked.filter(link => String(link.status).toLowerCase() === 'hired').length;
    const rejected = linked.filter(link => String(link.status).toLowerCase() === 'rejected').length;
    const inProgress = linked.filter(link => {
      const status = String(link.status || '').toLowerCase();
      return status !== 'hired' && status !== 'rejected' && status !== 'withdrawn';
    }).length;

    return {
      positionId: position.id,
      positionName: position.title || 'Untitled position',
      candidates: linked.length,
      inProgress,
      hired,
      rejected,
      status: position.status || 'Open'
    };
  });

  const chartData = {
    labels: ['Current'],
    datasets: [
      { label: 'Candidates Added', data: [totalCandidates] },
      { label: 'Hired', data: [hiredCandidates] }
    ]
  };

  return {
    totalCandidates,
    openPositions,
    hiredCandidates,
    pipelineSize,
    dropoffRate: Number(dropoffRate.toFixed(1)),
    avgTimeToHireDays: avgTimeToHireDays == null ? null : Number(avgTimeToHireDays.toFixed(1)),
    positionSummary,
    chartData
  };
}

if (typeof module !== 'undefined') {
  module.exports = { calculateOverviewMetrics, formatPercentage, safeNumber };
}
