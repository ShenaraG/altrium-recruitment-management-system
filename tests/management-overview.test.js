const assert = require('assert');
const { calculateOverviewMetrics } = require('../js/management-overview.js');

const metrics = calculateOverviewMetrics({
  candidates: [
    { id: 1, created_at: '2026-09-01T10:00:00Z' },
    { id: 2, created_at: '2026-09-03T12:00:00Z' },
    { id: 3, created_at: '2026-09-07T12:00:00Z' }
  ],
  positions: [
    { id: 11, title: 'Senior Engineer', status: 'Open' },
    { id: 12, title: 'Product Manager', status: 'Closed' }
  ],
  candidatePositions: [
    { candidate_id: 1, position_id: 11, status: 'Hired', created_at: '2026-09-02T09:00:00Z' },
    { candidate_id: 2, position_id: 11, status: 'Rejected', created_at: '2026-09-04T09:00:00Z' },
    { candidate_id: 3, position_id: 11, status: 'Interview', created_at: '2026-09-08T09:00:00Z' }
  ],
  decisions: [
    { candidate_id: 1, position_id: 11, status: 'Hired', decision_date: '2026-09-15T00:00:00Z' },
    { candidate_id: 2, position_id: 11, status: 'Rejected', decision_date: '2026-09-12T00:00:00Z' }
  ]
});

assert.strictEqual(metrics.totalCandidates, 3);
assert.strictEqual(metrics.openPositions, 1);
assert.strictEqual(metrics.hiredCandidates, 1);
assert.strictEqual(metrics.pipelineSize, 1);
assert.strictEqual(metrics.dropoffRate, 33.3);
assert.ok(metrics.avgTimeToHireDays >= 10);
assert.strictEqual(metrics.positionSummary.length, 2);
assert.strictEqual(metrics.positionSummary[0].positionName, 'Senior Engineer');
assert.strictEqual(metrics.positionSummary[0].hired, 1);

console.log('management overview metrics test passed');
