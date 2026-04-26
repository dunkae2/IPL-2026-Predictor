<template>
  <div id="app">
    <!-- Header -->
    <header class="header">
      <div class="header-left">
        <div class="logo-icon">
          <svg width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="11" cy="11" r="10" fill="#c0392b" stroke="#922b21" stroke-width="0.5"/>
            <path d="M11 1 C11 1, 7 5, 7 11 C7 17, 11 21, 11 21" stroke="white" stroke-width="1.2" fill="none"/>
            <path d="M11 1 C11 1, 15 5, 15 11 C15 17, 11 21, 11 21" stroke="white" stroke-width="1.2" fill="none"/>
            <path d="M8 4.5 C8.8 5.2, 9.5 5.5, 11 5.5 C12.5 5.5, 13.2 5.2, 14 4.5" stroke="white" stroke-width="0.9" fill="none"/>
            <path d="M7.5 8 C8.5 8.8, 9.8 9.2, 11 9.2 C12.2 9.2, 13.5 8.8, 14.5 8" stroke="white" stroke-width="0.9" fill="none"/>
            <path d="M7.5 14 C8.5 13.2, 9.8 12.8, 11 12.8 C12.2 12.8, 13.5 13.2, 14.5 14" stroke="white" stroke-width="0.9" fill="none"/>
            <path d="M8 17.5 C8.8 16.8, 9.5 16.5, 11 16.5 C12.5 16.5, 13.2 16.8, 14 17.5" stroke="white" stroke-width="0.9" fill="none"/>
          </svg>
        </div>
        <div>
          <div class="logo-text syne">CREASE</div>
          <div class="logo-sub">{{ seriesName || 'IPL PREDICTOR' }}</div>
        </div>
      </div>
      <div class="header-right">
        <div v-if="apiCallsToday > 80" class="api-warning">{{ 100 - apiCallsToday }} API calls left</div>
        <button v-if="!demoMode" @click="startDemo" class="demo-btn">Demo</button>
        <button v-else @click="stopDemo" class="demo-btn demo-btn-active">Stop Demo</button>
        <button class="tab-btn" :class="{ active: activeTab === 'upcoming' }" @click="activeTab = 'upcoming'">Upcoming</button>
        <button class="tab-btn" :class="{ active: activeTab === 'results' }" @click="activeTab = 'results'">Results</button>
      </div>
    </header>

    <!-- UPCOMING TAB -->
    <main v-if="activeTab === 'upcoming'" class="main-content">
      <div v-if="loadingMatches" class="loading-text">LOADING FIXTURES...</div>

      <div v-else>
        <!-- LIVE / DEMO -->
        <div v-if="demoMode || liveMatches.length" style="margin-bottom: 48px;">
          <div class="section-header-live">
            <span class="live-pulse"></span>
            <span class="section-label" style="color: #22c55e; margin-bottom: 0;">Live Now</span>
          </div>

          <!-- Demo card -->
          <div v-if="demoMode" class="live-card">
            <div class="live-accent"></div>
            <div class="match-teams-grid">
              <div>
                <div class="team-short" :style="{ color: teamColor('Chennai Super Kings') }">CSK</div>
                <div class="team-name syne">Chennai Super Kings</div>
                <div class="team-role">{{ demoPhase === 'innings1' ? 'Batting' : 'Defending' }}</div>
              </div>
              <div class="vs-divider">VS</div>
              <div style="text-align: right;">
                <div class="team-short" :style="{ color: teamColor('Gujarat Titans') }">GT</div>
                <div class="team-name syne">Gujarat Titans</div>
                <div class="team-role">{{ demoPhase === 'innings1' ? 'Bowling' : 'Chasing' }}</div>
              </div>
            </div>

            <div class="innings-badge" :style="{ borderColor: demoPhase === 'innings1' ? '#f5c518' : '#22c55e', color: demoPhase === 'innings1' ? '#f5c518' : '#22c55e' }">
              {{ demoPhase === 'innings1' ? 'Innings 1' : 'Innings 2 · Chasing' }}
            </div>

            <div class="stats-row">
              <div v-for="stat in demoStats" :key="stat.label" class="stat-box">
                <div class="stat-label">{{ stat.label }}</div>
                <div class="stat-value">{{ stat.value }}</div>
              </div>
            </div>

            <div style="margin-top: 16px;">
              <div class="prob-row" style="margin-bottom: 12px;">
                <div class="prob-team-row">
                  <span class="prob-team-label">{{ demoPhase === 'innings1' ? 'Chennai Super Kings' : 'Gujarat Titans (chasing)' }}</span>
                  <span class="syne prob-pct" :style="{ color: demoPhase === 'innings1' ? teamColor('Chennai Super Kings') : '#22c55e' }">{{ demoProbPct }}%</span>
                </div>
                <div class="prob-bar-bg">
                  <div class="prob-bar-fill" :style="{ width: demoProbPct + '%', background: demoPhase === 'innings1' ? teamColor('Chennai Super Kings') : '#22c55e' }"></div>
                </div>
              </div>
              <div class="prob-row">
                <div class="prob-team-row">
                  <span class="prob-team-label">{{ demoPhase === 'innings1' ? 'Gujarat Titans' : 'Chennai Super Kings (defending)' }}</span>
                  <span class="syne prob-pct" :style="{ color: teamColor('Gujarat Titans') }">{{ 100 - demoProbPct }}%</span>
                </div>
                <div class="prob-bar-bg">
                  <div class="prob-bar-fill" :style="{ width: (100 - demoProbPct) + '%', background: teamColor('Gujarat Titans') }"></div>
                </div>
              </div>
            </div>

            <div v-if="demoProbHistory.length > 1" style="margin-top: 24px;">
              <div class="section-label" style="margin-bottom: 10px;">Win probability · over by over</div>
              <div class="chart-legend">
                <span class="legend-dot" :style="{ background: demoPhase === 'innings1' ? teamColor('Chennai Super Kings') : '#22c55e' }"></span>
                <span class="legend-label" :style="{ color: demoPhase === 'innings1' ? teamColor('Chennai Super Kings') : '#22c55e' }">{{ demoPhase === 'innings1' ? 'CSK' : 'GT (chasing)' }}</span>
                <span class="legend-dot" :style="{ background: demoPhase === 'innings1' ? teamColor('Gujarat Titans') : teamColor('Chennai Super Kings'), marginLeft: '16px' }"></span>
                <span class="legend-label" :style="{ color: demoPhase === 'innings1' ? teamColor('Gujarat Titans') : teamColor('Chennai Super Kings') }">{{ demoPhase === 'innings1' ? 'GT' : 'CSK (defending)' }}</span>
              </div>
              <div style="position: relative; height: 200px;">
                <canvas id="demo-chart" role="img" aria-label="Win probability chart">Win probability chart</canvas>
              </div>
            </div>
          </div>

          <!-- Real live matches -->
          <div v-for="match in liveMatches" :key="match.id" class="live-card" style="margin-bottom: 12px;">
            <div class="live-accent"></div>
            <div class="match-teams-grid" style="margin-bottom: 16px;">
              <div>
                <div class="team-short" :style="{ color: teamColor(match.teams[0]) }">{{ shortName(match.teams[0]) }}</div>
                <div class="team-name syne">{{ match.teams[0] }}</div>
                <div v-if="liveData[match.id]" class="team-role">{{ getLiveRole(match.id, match.teams[0]) }}</div>
              </div>
              <div class="vs-divider">VS</div>
              <div style="text-align: right;">
                <div class="team-short" :style="{ color: teamColor(match.teams[1]) }">{{ shortName(match.teams[1]) }}</div>
                <div class="team-name syne">{{ match.teams[1] }}</div>
                <div v-if="liveData[match.id]" class="team-role">{{ getLiveRole(match.id, match.teams[1]) }}</div>
              </div>
            </div>

            <div v-if="liveData[match.id]">
              <div v-if="liveData[match.id].status === 'innings1'">
                <div class="innings-badge" style="border-color: #f5c518; color: #f5c518;">Innings 1 in progress</div>
                <div class="stats-row" style="margin-top: 12px;">
                  <div class="stat-box">
                    <div class="stat-label">Score</div>
                    <div class="stat-value">{{ liveData[match.id].match_state.runs }}/{{ liveData[match.id].match_state.wickets }}</div>
                  </div>
                  <div class="stat-box">
                    <div class="stat-label">Overs</div>
                    <div class="stat-value">{{ liveData[match.id].match_state.overs_done }}</div>
                  </div>
                  <div class="stat-box">
                    <div class="stat-label">CRR</div>
                    <div class="stat-value">{{ liveData[match.id].match_state.current_run_rate }}</div>
                  </div>
                  <div class="stat-box">
                    <div class="stat-label">Projected</div>
                    <div class="stat-value">{{ liveData[match.id].match_state.projected_total }}</div>
                  </div>
                </div>
                <div style="margin-top: 16px;">
                  <div class="prob-row" style="margin-bottom: 12px;">
                    <div class="prob-team-row">
                      <span class="prob-team-label">{{ liveData[match.id].batting_team }} (batting)</span>
                      <span class="syne prob-pct" :style="{ color: teamColor(liveData[match.id].batting_team) }">{{ pct(liveData[match.id].batting_win_probability) }}</span>
                    </div>
                    <div class="prob-bar-bg"><div class="prob-bar-fill" :style="{ width: pct(liveData[match.id].batting_win_probability), background: teamColor(liveData[match.id].batting_team) }"></div></div>
                  </div>
                  <div class="prob-row">
                    <div class="prob-team-row">
                      <span class="prob-team-label">{{ liveData[match.id].bowling_team }} (bowling)</span>
                      <span class="syne prob-pct" :style="{ color: teamColor(liveData[match.id].bowling_team) }">{{ pct(liveData[match.id].bowling_win_probability) }}</span>
                    </div>
                    <div class="prob-bar-bg"><div class="prob-bar-fill" :style="{ width: pct(liveData[match.id].bowling_win_probability), background: teamColor(liveData[match.id].bowling_team) }"></div></div>
                  </div>
                </div>
              </div>

              <div v-else-if="liveData[match.id].status === 'live'">
                <div class="innings-badge" style="border-color: #22c55e; color: #22c55e;">Innings 2 · Chase</div>
                <div class="stats-row" style="margin-top: 12px;">
                  <div class="stat-box" v-for="(val, key) in liveStats(match.id)" :key="key">
                    <div class="stat-label">{{ key }}</div>
                    <div class="stat-value">{{ val }}</div>
                  </div>
                </div>
                <div style="margin-top: 16px;">
                  <div class="prob-row" style="margin-bottom: 12px;">
                    <div class="prob-team-row">
                      <span class="prob-team-label">{{ liveData[match.id].chasing_team }} (chasing)</span>
                      <span class="syne prob-pct" style="color: #22c55e;">{{ pct(liveData[match.id].chasing_win_probability) }}</span>
                    </div>
                    <div class="prob-bar-bg"><div class="prob-bar-fill" :style="{ width: pct(liveData[match.id].chasing_win_probability), background: '#22c55e' }"></div></div>
                  </div>
                  <div class="prob-row">
                    <div class="prob-team-row">
                      <span class="prob-team-label">{{ liveData[match.id].defending_team }} (defending)</span>
                      <span class="syne prob-pct" :style="{ color: teamColor(liveData[match.id].defending_team) }">{{ pct(liveData[match.id].defending_win_probability) }}</span>
                    </div>
                    <div class="prob-bar-bg"><div class="prob-bar-fill" :style="{ width: pct(liveData[match.id].defending_win_probability), background: teamColor(liveData[match.id].defending_team) }"></div></div>
                  </div>
                </div>
                <div v-if="probHistory[match.id] && probHistory[match.id].length > 1" style="margin-top: 24px;">
                  <div class="section-label" style="margin-bottom: 6px;">Win probability · over by over</div>
                  <div class="chart-legend">
                    <span class="legend-dot" style="background: #22c55e;"></span>
                    <span class="legend-label" style="color: #22c55e;">{{ liveData[match.id].chasing_team }}</span>
                    <span class="legend-dot" :style="{ background: teamColor(liveData[match.id].defending_team), marginLeft: '16px' }"></span>
                    <span class="legend-label" :style="{ color: teamColor(liveData[match.id].defending_team) }">{{ liveData[match.id].defending_team }}</span>
                  </div>
                  <div style="position: relative; height: 200px;">
                    <canvas :id="'chart-' + match.id" role="img" aria-label="Live win probability chart">Live win probability</canvas>
                  </div>
                </div>
              </div>

              <div v-else class="waiting-text">Waiting for match to start...</div>
            </div>
            <div v-else class="waiting-text">Fetching live data...</div>
          </div>
        </div>

        <!-- Next Match Hero -->
        <div v-if="nextMatch && !demoMode" style="margin-bottom: 48px;">
          <div class="section-label">{{ isToday(nextMatch.date) ? 'Today' : 'Next Match' }}</div>
          <div class="hero-card">
            <div class="hero-accent" :style="{ background: teamColor(nextMatch.teams[0]) }"></div>
            <div class="match-teams-grid" style="margin-bottom: 20px;">
              <div>
                <div class="team-short" :style="{ color: teamColor(nextMatch.teams[0]) }">{{ shortName(nextMatch.teams[0]) }}</div>
                <div class="team-name syne" style="font-size: 24px;">{{ nextMatch.teams[0] }}</div>
              </div>
              <div class="vs-divider">VS</div>
              <div style="text-align: right;">
                <div class="team-short" :style="{ color: teamColor(nextMatch.teams[1]) }">{{ shortName(nextMatch.teams[1]) }}</div>
                <div class="team-name syne" style="font-size: 24px;">{{ nextMatch.teams[1] }}</div>
              </div>
            </div>
            <div class="match-meta">
              <span>{{ formatDate(nextMatch.date) }}</span>
              <span class="meta-dot">·</span>
              <span>{{ shortVenue(nextMatch.venue) }}</span>
              <span class="meta-dot">·</span>
              <span style="color: #3a3a5c;">{{ timeUntilMatch(nextMatch.date) }}</span>
            </div>
            <div v-if="!heroPrediction && !loadingHero" style="margin-top: 20px;">
              <button @click="fetchHeroPrediction" class="predict-btn" :style="{ background: teamColor(nextMatch.teams[0]) }">Get Prediction</button>
            </div>
            <div v-else-if="loadingHero" class="computing-text">COMPUTING...</div>
            <div v-else-if="heroPrediction" style="margin-top: 20px;">
              <div class="prob-row" style="margin-bottom: 14px;">
                <div class="prob-team-row">
                  <span class="prob-team-label" style="font-size: 15px;">{{ heroPrediction.team_a }}</span>
                  <span class="syne" style="font-size: 24px; font-weight: 700;" :style="{ color: teamColor(heroPrediction.team_a) }">{{ pct(heroPrediction.team_a_win_probability) }}</span>
                </div>
                <div class="prob-bar-bg"><div class="prob-bar-fill" :style="{ width: pct(heroPrediction.team_a_win_probability), background: teamColor(heroPrediction.team_a) }"></div></div>
              </div>
              <div class="prob-row">
                <div class="prob-team-row">
                  <span class="prob-team-label" style="font-size: 15px;">{{ heroPrediction.team_b }}</span>
                  <span class="syne" style="font-size: 24px; font-weight: 700;" :style="{ color: teamColor(heroPrediction.team_b) }">{{ pct(heroPrediction.team_b_win_probability) }}</span>
                </div>
                <div class="prob-bar-bg"><div class="prob-bar-fill" :style="{ width: pct(heroPrediction.team_b_win_probability), background: teamColor(heroPrediction.team_b) }"></div></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Next 7 days -->
        <div v-if="weekMatches.length && !demoMode">
          <div class="section-label">Next 7 Days</div>
          <div class="match-list">
            <div v-for="match in weekMatches" :key="match.id" class="match-card" @click="toggleMatchPrediction(match)">
              <div class="match-card-top">
                <div class="team-chips">
                  <div class="team-chip" :style="{ background: teamColor(match.teams[0]) + '22', borderColor: teamColor(match.teams[0]) + '55' }">
                    <span :style="{ color: teamColor(match.teams[0]) }">{{ shortName(match.teams[0]) }}</span>
                  </div>
                  <span class="vs-small">vs</span>
                  <div class="team-chip" :style="{ background: teamColor(match.teams[1]) + '22', borderColor: teamColor(match.teams[1]) + '55' }">
                    <span :style="{ color: teamColor(match.teams[1]) }">{{ shortName(match.teams[1]) }}</span>
                  </div>
                </div>
                <span class="match-date">{{ formatDate(match.date) }}</span>
              </div>
              <div class="match-card-bottom">
                <span class="venue-text">{{ shortVenue(match.venue) }}</span>
                <span v-if="!matchPredictions[match.id] && !loadingPredictions[match.id]" class="tap-hint">Tap to predict →</span>
                <span v-if="loadingPredictions[match.id]" class="loading-small">LOADING...</span>
              </div>
              <div v-if="matchPredictions[match.id]" class="inline-prediction">
                <div class="prediction-grid">
                  <div>
                    <div class="pred-team-row">
                      <span class="prob-team-label">{{ match.teams[0] }}</span>
                      <span class="syne" style="font-size: 18px; font-weight: 700;" :style="{ color: teamColor(match.teams[0]) }">{{ pct(matchPredictions[match.id].team_a_win_probability) }}</span>
                    </div>
                    <div class="prob-bar-bg"><div class="prob-bar-fill" :style="{ width: pct(matchPredictions[match.id].team_a_win_probability), background: teamColor(match.teams[0]) }"></div></div>
                  </div>
                  <div>
                    <div class="pred-team-row">
                      <span class="prob-team-label">{{ match.teams[1] }}</span>
                      <span class="syne" style="font-size: 18px; font-weight: 700;" :style="{ color: teamColor(match.teams[1]) }">{{ pct(matchPredictions[match.id].team_b_win_probability) }}</span>
                    </div>
                    <div class="prob-bar-bg"><div class="prob-bar-fill" :style="{ width: pct(matchPredictions[match.id].team_b_win_probability), background: teamColor(match.teams[1]) }"></div></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Later season -->
        <div v-if="laterMatches.length && !demoMode" style="margin-top: 40px;">
          <div class="section-label">Later in the Season</div>
          <div style="display: flex; flex-direction: column; gap: 8px;">
            <div v-for="match in laterMatches" :key="match.id" class="later-card"
              @mouseenter="e => e.currentTarget.style.borderColor='#1e1e30'"
              @mouseleave="e => e.currentTarget.style.borderColor='#10101a'"
              @click="toggleMatchPrediction(match)">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; gap:10px; align-items:center;">
                  <span :style="{ color: teamColor(match.teams[0]) }" style="font-size:14px; font-weight:500;">{{ match.teams[0] }}</span>
                  <span style="font-size:12px; color:#2a2a4a;">vs</span>
                  <span :style="{ color: teamColor(match.teams[1]) }" style="font-size:14px; font-weight:500;">{{ match.teams[1] }}</span>
                </div>
                <span style="font-size:12px; color:#3a3a5c;">{{ formatDate(match.date) }}</span>
              </div>
              <div v-if="matchPredictions[match.id]" style="margin-top:10px; display:flex; gap:16px;">
                <span :style="{ color: teamColor(match.teams[0]) }" style="font-size:14px; font-weight:600;">{{ pct(matchPredictions[match.id].team_a_win_probability) }}</span>
                <span style="color:#2a2a4a;">·</span>
                <span :style="{ color: teamColor(match.teams[1]) }" style="font-size:14px; font-weight:600;">{{ pct(matchPredictions[match.id].team_b_win_probability) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- RESULTS TAB -->
    <main v-if="activeTab === 'results'" class="main-content">
      <div v-if="loadingMatches" class="loading-text">LOADING...</div>
      <div v-else>
        <div class="section-label">Completed Matches</div>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          <div v-for="match in completedMatches" :key="match.id" class="result-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <div style="display:flex; gap:10px; align-items:center;">
                <span :style="{ color: teamColor(match.teams[0]) }" style="font-size:15px; font-weight:600;">{{ match.teams[0] }}</span>
                <span style="font-size:12px; color:#2a2a4a;">vs</span>
                <span :style="{ color: teamColor(match.teams[1]) }" style="font-size:15px; font-weight:600;">{{ match.teams[1] }}</span>
              </div>
              <span style="font-size:12px; color:#3a3a5c;">{{ formatDate(match.date) }}</span>
            </div>
            <div style="font-size:14px; color:#8a8aaa;">{{ match.match_status }}</div>
            <div style="font-size:12px; color:#3a3a5c; margin-top:4px;">{{ shortVenue(match.venue) }}</div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick } from 'vue'

const API_BASE = 'http://127.0.0.1:8000'
const activeTab = ref('upcoming')
const loadingMatches = ref(true)
const matches = ref([])
const matchPredictions = reactive({})
const loadingPredictions = reactive({})
const heroPrediction = ref(null)
const loadingHero = ref(false)
const liveData = reactive({})
const probHistory = reactive({})
const seriesName = ref('')
const apiCallsToday = ref(0)
const demoMode = ref(false)
const demoProbHistory = ref([])
const demoProbPct = ref(50)
const demoStats = ref([])
const demoPhase = ref('innings1')
const charts = {}
let matchListTimeout = null
let livePollingInterval = null
let demoInterval = null

const TEAM_COLORS = {
  'Chennai Super Kings': '#f5c518',
  'Mumbai Indians': '#0ea5e9',
  'Royal Challengers Bengaluru': '#ef4444',
  'Royal Challengers Bangalore': '#ef4444',
  'Kolkata Knight Riders': '#a78bfa',
  'Sunrisers Hyderabad': '#f97316',
  'Delhi Capitals': '#38bdf8',
  'Rajasthan Royals': '#ec4899',
  'Gujarat Titans': '#94a3b8',
  'Lucknow Super Giants': '#2dd4bf',
  'Punjab Kings': '#f87171',
}

const TEAM_SHORT = {
  'Chennai Super Kings': 'CSK', 'Mumbai Indians': 'MI',
  'Royal Challengers Bengaluru': 'RCB', 'Royal Challengers Bangalore': 'RCB',
  'Kolkata Knight Riders': 'KKR', 'Sunrisers Hyderabad': 'SRH',
  'Delhi Capitals': 'DC', 'Rajasthan Royals': 'RR',
  'Gujarat Titans': 'GT', 'Lucknow Super Giants': 'LSG', 'Punjab Kings': 'PBKS',
}

function teamColor(team) { return TEAM_COLORS[team] || '#a855f7' }
function shortName(team) { return TEAM_SHORT[team] || team.split(' ').map(w => w[0]).join('') }
function pct(v) { return (v * 100).toFixed(0) + '%' }

function formatDate(dateStr) {
  const d = new Date(dateStr + 'Z')
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }) + ', ' +
    d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true })
}

function timeUntilMatch(dateStr) {
  const diff = new Date(dateStr + 'Z') - new Date()
  if (diff < 0) return 'Started'
  const h = Math.floor(diff / 3600000)
  const m = Math.floor((diff % 3600000) / 60000)
  if (h > 24) return `${Math.floor(h / 24)}d away`
  if (h > 0) return `${h}h ${m}m away`
  return `${m}m away`
}

function shortVenue(venue) { return venue ? venue.split(',')[0] : '' }
function isToday(dateStr) { return new Date(dateStr + 'Z').toDateString() === new Date().toDateString() }
function daysFromNow(dateStr) { return (new Date(dateStr + 'Z') - new Date()) / (1000 * 60 * 60 * 24) }
function minsUntil(dateStr) { return (new Date(dateStr + 'Z') - new Date()) / 60000 }

function getLiveRole(matchId, team) {
  const d = liveData[matchId]
  if (!d) return ''
  if (d.status === 'innings1') return team === d.batting_team ? 'Batting' : 'Bowling'
  if (d.status === 'live') return team === d.chasing_team ? 'Chasing' : 'Defending'
  return ''
}

function liveStats(matchId) {
  const s = liveData[matchId]?.match_state
  if (!s) return {}
  const need = s.runs_required <= 0 ? 'Won!' : `${s.runs_required} (${Math.floor(s.balls_remaining / 6)}.${s.balls_remaining % 6} ov)`
  return {
    'Target': s.target,
    'Need': need,
    'Wkts': s.wickets_remaining,
    'CRR': s.current_run_rate,
    'RRR': s.runs_required <= 0 ? '—' : s.required_run_rate,
  }
}

const liveMatches = computed(() => matches.value.filter(m => m.status === 'live'))
const upcomingMatches = computed(() => [...matches.value].filter(m => m.status === 'upcoming').sort((a, b) => new Date(a.date + 'Z') - new Date(b.date + 'Z')))
const nextMatch = computed(() => upcomingMatches.value[0] || null)
const weekMatches = computed(() => upcomingMatches.value.slice(1).filter(m => daysFromNow(m.date) <= 7))
const laterMatches = computed(() => upcomingMatches.value.slice(1).filter(m => daysFromNow(m.date) > 7))
const completedMatches = computed(() => [...matches.value].filter(m => m.status === 'completed').sort((a, b) => new Date(b.date + 'Z') - new Date(a.date + 'Z')))

async function fetchMatches() {
  try {
    const res = await fetch(`${API_BASE}/matches`)
    const data = await res.json()
    matches.value = data.matches
    if (data.series_name) seriesName.value = data.series_name
    apiCallsToday.value = data.api_calls_today || 0

    const live = matches.value.filter(m => m.status === 'live')
    if (live.length && !livePollingInterval) {
      live.forEach(m => fetchLivePrediction(m.id))
      livePollingInterval = setInterval(() => {
        matches.value.filter(m => m.status === 'live').forEach(m => fetchLivePrediction(m.id))
      }, 180000)
    }
    if (!live.length && livePollingInterval) {
      clearInterval(livePollingInterval)
      livePollingInterval = null
    }
  } catch (e) { console.error(e) }
  loadingMatches.value = false
}

function scheduleMatchListPolling() {
  const tick = () => {
    fetchMatches()
    const upcoming = [...matches.value].filter(m => m.status === 'upcoming').sort((a, b) => new Date(a.date + 'Z') - new Date(b.date + 'Z'))
    const mins = upcoming.length ? minsUntil(upcoming[0].date) : 9999
    const interval = (mins < 30 && mins > -30) ? 60000 : 300000
    matchListTimeout = setTimeout(tick, interval)
  }
  matchListTimeout = setTimeout(tick, 60000)
}

async function fetchLivePrediction(matchId) {
  try {
    const res = await fetch(`${API_BASE}/match/${matchId}/live_prediction`)
    const data = await res.json()
    liveData[matchId] = data

    if (data.status === 'live' || data.status === 'innings1') {
      if (!probHistory[matchId]) probHistory[matchId] = []
      const overs = data.match_state.overs_done
      const prob = data.status === 'live' ? data.chasing_win_probability : data.batting_win_probability
      const last = probHistory[matchId].slice(-1)[0]
      if (!last || last.overs !== overs) {
        probHistory[matchId].push({ overs, prob })
        const c1 = data.status === 'live' ? '#22c55e' : teamColor(data.batting_team)
        const c2 = data.status === 'live' ? teamColor(data.defending_team) : teamColor(data.bowling_team)
        await nextTick()
        renderTwoLineChart('chart-' + matchId, probHistory[matchId], c1, c2)
      }
    }

    if (data.status === 'ended') {
      clearInterval(livePollingInterval)
      livePollingInterval = null
      fetchMatches()
    }
  } catch (e) { console.error(e) }
}

async function fetchHeroPrediction() {
  if (!nextMatch.value) return
  loadingHero.value = true
  try {
    const res = await fetch(`${API_BASE}/predict/prematch`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ team_a: nextMatch.value.teams[0], team_b: nextMatch.value.teams[1] })
    })
    heroPrediction.value = await res.json()
  } catch (e) { console.error(e) }
  loadingHero.value = false
}

async function toggleMatchPrediction(match) {
  if (matchPredictions[match.id] || loadingPredictions[match.id]) return
  loadingPredictions[match.id] = true
  try {
    const res = await fetch(`${API_BASE}/predict/prematch`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ team_a: match.teams[0], team_b: match.teams[1] })
    })
    matchPredictions[match.id] = await res.json()
  } catch (e) { console.error(e) }
  loadingPredictions[match.id] = false
}

function startDemo() {
  demoMode.value = true
  demoProbHistory.value = []
  demoPhase.value = 'innings1'
  let over = 0

  const inn1Script = [52, 55, 58, 54, 50, 48, 45, 60, 65, 68, 62, 57, 63, 67, 65, 70, 74, 76, 72, 75]
  const inn2Script = [42, 45, 48, 44, 40, 38, 35, 52, 58, 62, 60, 55, 65, 70, 68, 72, 75, 80, 85, 90]

  const inn2Stats = [
    { target: 175, runs: 12, wickets: 9, crr: 7.2, rrr: 9.1 },
    { target: 175, runs: 28, wickets: 9, crr: 8.4, rrr: 9.4 },
    { target: 175, runs: 44, wickets: 8, crr: 8.8, rrr: 9.5 },
    { target: 175, runs: 58, wickets: 8, crr: 8.3, rrr: 9.8 },
    { target: 175, runs: 71, wickets: 7, crr: 8.1, rrr: 10.2 },
    { target: 175, runs: 85, wickets: 7, crr: 8.5, rrr: 10.0 },
    { target: 175, runs: 102, wickets: 7, crr: 8.5, rrr: 9.75 },
    { target: 175, runs: 122, wickets: 7, crr: 9.4, rrr: 9.5 },
    { target: 175, runs: 140, wickets: 7, crr: 9.3, rrr: 9.0 },
    { target: 175, runs: 155, wickets: 7, crr: 9.4, rrr: 8.3 },
    { target: 175, runs: 162, wickets: 7, crr: 9.0, rrr: 7.8 },
    { target: 175, runs: 168, wickets: 6, crr: 9.1, rrr: 7.5 },
    { target: 175, runs: 175, wickets: 6, crr: 9.2, rrr: 0 },
  ]

  const tick = () => {
    if (over < 20) {
      // Innings 1
      demoPhase.value = 'innings1'
      const prob = inn1Script[over]
      const runs = Math.round(8.5 * (over + 1))
      const wickets = Math.min(9, Math.floor((over + 1) / 4))
      demoProbPct.value = prob
      demoProbHistory.value = [...demoProbHistory.value, { overs: over + 1, prob: prob / 100 }]
      demoStats.value = [
        { label: 'Score', value: `${runs}/${wickets}` },
        { label: 'Overs', value: over + 1 },
        { label: 'CRR', value: '8.5' },
        { label: 'Projected', value: 170 },
      ]
      nextTick(() => renderTwoLineChart('demo-chart', demoProbHistory.value, teamColor('Chennai Super Kings'), teamColor('Gujarat Titans')))
      over++
    } else {
      // Transition: reset chart for innings 2
      if (over === 20) {
        if (charts['demo-chart']) {
          charts['demo-chart'].destroy()
          delete charts['demo-chart']
        }
        demoProbHistory.value = []
        demoPhase.value = 'innings2'
      }

      const i = over - 20
      if (i >= inn2Script.length) { stopDemo(); return }

      const prob = inn2Script[i]
      const s = inn2Stats[Math.min(i, inn2Stats.length - 1)]

      // Stop demo when chase is complete
      if (s.runs >= s.target) { stopDemo(); return }

      demoProbPct.value = prob
      demoProbHistory.value = [...demoProbHistory.value, { overs: i + 1, prob: prob / 100 }]
      demoStats.value = [
        { label: 'Target', value: s.target },
        { label: 'Need', value: s.runs >= s.target ? 'Won!' : `${s.target - s.runs} (${20 - i - 1} ov)` },
        { label: 'Wkts', value: s.wickets },
        { label: 'CRR', value: s.crr.toFixed(1) },
        { label: 'RRR', value: s.runs >= s.target ? '—' : s.rrr.toFixed(1) },
      ]
      nextTick(() => renderTwoLineChart('demo-chart', demoProbHistory.value, '#22c55e', teamColor('Chennai Super Kings')))
      over++
    }
  }

  tick()
  demoInterval = setInterval(tick, 1800)
}

function stopDemo() {
  demoMode.value = false
  if (demoInterval) { clearInterval(demoInterval); demoInterval = null }
  if (charts['demo-chart']) { charts['demo-chart'].destroy(); delete charts['demo-chart'] }
  demoProbHistory.value = []
}

function renderTwoLineChart(canvasId, history, color1, color2) {
  if (!history || history.length < 2) return
  const canvas = document.getElementById(canvasId)
  if (!canvas || !window.Chart) return

  const labels = history.map(h => `${h.overs}`)
  const data1 = history.map(h => parseFloat((h.prob * 100).toFixed(1)))
  const data2 = history.map(h => parseFloat(((1 - h.prob) * 100).toFixed(1)))

  if (charts[canvasId]) {
    charts[canvasId].data.labels = labels
    charts[canvasId].data.datasets[0].data = data1
    charts[canvasId].data.datasets[1].data = data2
    charts[canvasId].update('none')
    return
  }

  charts[canvasId] = new window.Chart(canvas, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          data: data1,
          borderColor: color1,
          backgroundColor: 'transparent',
          borderWidth: 2.5,
          pointRadius: 3,
          pointBackgroundColor: color1,
          pointBorderColor: '#080810',
          pointBorderWidth: 2,
          fill: false,
          tension: 0.4
        },
        {
          data: data2,
          borderColor: color2,
          backgroundColor: 'transparent',
          borderWidth: 2.5,
          pointRadius: 3,
          pointBackgroundColor: color2,
          pointBorderColor: '#080810',
          pointBorderWidth: 2,
          fill: false,
          tension: 0.4,
          borderDash: [4, 3]
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#12121e',
          borderColor: '#2a2a40',
          borderWidth: 1,
          titleColor: '#888',
          titleFont: { family: 'IBM Plex Mono', size: 11 },
          bodyFont: { family: 'IBM Plex Mono', size: 12 },
          padding: 10,
          callbacks: {
            title: ctx => `Over ${ctx[0].label}`,
            label: ctx => `  ${ctx.datasetIndex === 0 ? 'Team 1' : 'Team 2'}: ${ctx.parsed.y}%`
          }
        }
      },
      scales: {
        x: {
          ticks: { color: '#3a3a5c', font: { family: 'IBM Plex Mono', size: 10 }, maxRotation: 0 },
          grid: { color: '#10101a' },
          title: { display: true, text: 'Over', color: '#2a2a4a', font: { family: 'IBM Plex Mono', size: 10 } }
        },
        y: {
          min: 0, max: 100,
          ticks: { color: '#3a3a5c', font: { family: 'IBM Plex Mono', size: 10 }, callback: v => v + '%', stepSize: 25 },
          grid: { color: '#10101a' }
        }
      }
    }
  })
}

onMounted(async () => {
  const script = document.createElement('script')
  script.src = 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js'
  document.head.appendChild(script)
  await fetchMatches()
  scheduleMatchListPolling()
})

onUnmounted(() => {
  if (matchListTimeout) clearTimeout(matchListTimeout)
  if (livePollingInterval) clearInterval(livePollingInterval)
  if (demoInterval) clearInterval(demoInterval)
  Object.values(charts).forEach(c => c.destroy())
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
#app { background: #080810; min-height: 100vh; font-family: 'IBM Plex Mono', monospace; color: #e8e4f0; }
.syne { font-family: 'Syne', sans-serif; }

.header { border-bottom: 1.5px solid #10101a; padding: 20px 36px; display: flex; align-items: center; justify-content: space-between; position: sticky; top: 0; background: #080810; z-index: 10; }
.header-left { display: flex; align-items: center; gap: 14px; }
.header-right { display: flex; gap: 8px; align-items: center; }

.logo-icon { width: 36px; height: 36px; background: #1a0a0a; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1.5px solid #c0392b33; }
.logo-text { font-size: 20px; font-weight: 800; letter-spacing: 0.05em; background: linear-gradient(90deg, #a855f7, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.logo-sub { font-size: 10px; color: #3a3a5c; letter-spacing: 0.15em; margin-top: 1px; }

.tab-btn { background: transparent; border: 1.5px solid #1e1e2e; color: #555; padding: 8px 18px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; letter-spacing: 0.08em; cursor: pointer; transition: all 0.2s; border-radius: 4px; text-transform: uppercase; }
.tab-btn.active { background: #a855f7; color: #080810; border-color: #a855f7; }
.tab-btn:hover:not(.active) { border-color: #2a2a4a; color: #888; }

.demo-btn { background: #0f0f1e; border: 1.5px solid #2a2a4e; color: #7c3aed; padding: 8px 16px; font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 0.08em; cursor: pointer; border-radius: 4px; text-transform: uppercase; transition: all 0.2s; }
.demo-btn:hover { background: #1a1a2e; }
.demo-btn-active { border-color: #22c55e; color: #22c55e; }
.api-warning { font-size: 10px; color: #f97316; border: 1px solid #f9731644; padding: 4px 8px; border-radius: 4px; }

.main-content { max-width: 820px; margin: 0 auto; padding: 36px 24px; }
.loading-text { color: #3a3a5c; font-size: 13px; letter-spacing: 0.1em; padding: 60px 0; text-align: center; }

.section-label { font-size: 10px; letter-spacing: 0.2em; text-transform: uppercase; color: #3a3a5c; margin-bottom: 14px; font-family: 'IBM Plex Mono', monospace; display: block; }
.section-header-live { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }

.live-pulse { display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #22c55e; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100% { opacity:1; transform:scale(1) } 50% { opacity:.6; transform:scale(1.3) } }

.live-card { border: 1.5px solid #1a3a2a; background: #090f0d; border-radius: 12px; padding: 28px; position: relative; overflow: hidden; }
.live-accent { position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #22c55e; border-radius: 4px 0 0 4px; }

.hero-card { border: 1.5px solid #1e1e30; background: #0c0c1a; border-radius: 12px; padding: 28px; position: relative; overflow: hidden; }
.hero-accent { position: absolute; top: 0; left: 0; width: 4px; height: 100%; }

.innings-badge { display: inline-block; border: 1px solid; border-radius: 4px; padding: 3px 10px; font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 12px; }

.match-teams-grid { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 16px; margin-bottom: 24px; }
.team-short { font-size: 12px; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 6px; }
.team-name { font-size: 20px; font-weight: 700; color: #e8e4f0; line-height: 1.2; }
.team-role { font-size: 13px; color: #3a3a5c; margin-top: 4px; }
.vs-divider { text-align: center; font-size: 11px; color: #2a2a4a; letter-spacing: 0.2em; }

.stats-row { display: flex; gap: 10px; flex-wrap: wrap; }
.stat-box { background: #0f1a14; border: 1px solid #1a2a1e; border-radius: 6px; padding: 8px 14px; }
.stat-label { font-size: 10px; color: #3a5a4a; letter-spacing: 0.1em; text-transform: uppercase; }
.stat-value { font-size: 15px; font-weight: 600; color: #e8e4f0; margin-top: 2px; }

.prob-bar-bg { height: 5px; background: #14141e; border-radius: 3px; overflow: hidden; margin-top: 6px; }
.prob-bar-fill { height: 100%; border-radius: 3px; transition: width 0.8s cubic-bezier(.4,0,.2,1); }
.prob-team-label { font-size: 14px; color: #aaa; }
.prob-pct { font-size: 20px; font-weight: 700; }
.prob-team-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }

.chart-legend { display: flex; align-items: center; margin-bottom: 10px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.legend-label { font-size: 12px; margin-left: 6px; }

.match-meta { display: flex; gap: 12px; font-size: 13px; color: #4a4a6a; margin-bottom: 4px; flex-wrap: wrap; }
.meta-dot { color: #2a2a4a; }

.predict-btn { border: none; padding: 12px 24px; font-family: 'IBM Plex Mono', monospace; font-size: 13px; letter-spacing: 0.1em; text-transform: uppercase; cursor: pointer; font-weight: 500; border-radius: 6px; color: #080810; transition: all 0.2s; }
.predict-btn:hover { transform: translateY(-1px); filter: brightness(1.1); }

.computing-text { font-size: 13px; color: #3a3a5c; letter-spacing: 0.1em; margin-top: 16px; }
.waiting-text { font-size: 13px; color: #3a5a4a; }

.match-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 40px; }
.match-card { border: 1.5px solid #14141e; background: #0c0c18; border-radius: 10px; padding: 18px 20px; cursor: pointer; transition: border-color 0.2s, transform 0.15s; }
.match-card:hover { border-color: #2a2a3e; transform: translateY(-1px); }
.match-card-top { display: flex; justify-content: space-between; align-items: center; }
.match-card-bottom { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; }
.team-chips { display: flex; align-items: center; gap: 8px; }
.team-chip { border: 1px solid; border-radius: 20px; padding: 4px 12px; font-size: 13px; font-weight: 500; }
.vs-small { font-size: 12px; color: #3a3a5c; }
.match-date { font-size: 13px; color: #4a4a6a; }
.venue-text { font-size: 13px; color: #3a3a5c; }
.tap-hint { font-size: 13px; color: #4a4a6a; }
.loading-small { font-size: 12px; color: #3a3a5c; letter-spacing: 0.08em; }

.inline-prediction { margin-top: 16px; padding-top: 16px; border-top: 1px solid #14141e; }
.prediction-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.pred-team-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }

.later-card { border: 1.5px solid #10101a; background: #090912; border-radius: 8px; padding: 14px 20px; cursor: pointer; transition: border-color 0.2s; }
.result-card { border: 1.5px solid #12121c; background: #0a0a14; border-radius: 8px; padding: 18px 22px; }
</style>