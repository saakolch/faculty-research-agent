// Faculty Research Agent - Frontend JavaScript

let currentMatches = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadAvailableFiles();
    setupEventListeners();
});

function setupEventListeners() {
    // Enable match button when interests are entered
    document.getElementById('interests').addEventListener('input', function() {
        const matchBtn = document.getElementById('matchBtn');
        matchBtn.disabled = !this.value.trim();
    });
}

function loadAvailableFiles() {
    fetch('/files')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const fileSelect = document.getElementById('fileSelect');
                fileSelect.innerHTML = '<option value="">Select a file...</option>';
                
                data.files.forEach(file => {
                    const option = document.createElement('option');
                    option.value = file.name;
                    option.textContent = `${file.name} (${formatFileSize(file.size)})`;
                    fileSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error('Error loading files:', error);
            showStatus('loadingStatus', 'Error loading files', 'error');
        });
}

function startScraping() {
    const headless = document.getElementById('headless').checked;
    const delay = parseFloat(document.getElementById('delay').value);
    
    showStatus('scrapingStatus', 'Starting scraping process...', 'info');
    
    fetch('/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            headless: headless,
            delay: delay
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showStatus('scrapingStatus', data.message, 'success');
            document.getElementById('matchBtn').disabled = false;
            loadAvailableFiles(); // Refresh file list
        } else {
            showStatus('scrapingStatus', `Error: ${data.error}`, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showStatus('scrapingStatus', 'Error during scraping', 'error');
    });
}

function loadProfiles() {
    const filename = document.getElementById('fileSelect').value;
    
    if (!filename) {
        showStatus('loadingStatus', 'Please select a file', 'error');
        return;
    }
    
    showStatus('loadingStatus', 'Loading profiles...', 'info');
    
    fetch('/load_profiles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            filename: filename
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showStatus('loadingStatus', data.message, 'success');
            document.getElementById('matchBtn').disabled = false;
        } else {
            showStatus('loadingStatus', `Error: ${data.error}`, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showStatus('loadingStatus', 'Error loading profiles', 'error');
    });
}

function findMatches() {
    const interests = document.getElementById('interests').value.trim();
    const openaiKey = document.getElementById('openaiKey').value.trim();
    
    if (!interests) {
        showStatus('matchingStatus', 'Please enter your research interests', 'error');
        return;
    }
    
    showStatus('matchingStatus', 'Finding matches...', 'info');
    
    fetch('/match', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            interests: interests,
            openai_key: openaiKey
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentMatches = data.matches;
            displayResults(data);
            showStatus('matchingStatus', `Found ${data.total_matches} matches out of ${data.total_profiles} profiles`, 'success');
        } else {
            showStatus('matchingStatus', `Error: ${data.error}`, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showStatus('matchingStatus', 'Error finding matches', 'error');
    });
}

function displayResults(data) {
    const resultsCard = document.getElementById('resultsCard');
    const resultsSummary = document.getElementById('resultsSummary');
    const resultsList = document.getElementById('resultsList');
    
    // Show results section
    resultsCard.style.display = 'block';
    
    // Update summary
    resultsSummary.innerHTML = `
        <div class="alert alert-info">
            <i class="fas fa-info-circle me-2"></i>
            Found <strong>${data.total_matches}</strong> matching faculty members out of <strong>${data.total_profiles}</strong> total profiles.
        </div>
    `;
    
    // Display matches
    resultsList.innerHTML = '';
    
    if (data.matches.length === 0) {
        resultsList.innerHTML = `
            <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                No faculty members found that match your research interests. Try broadening your search criteria.
            </div>
        `;
        return;
    }
    
    data.matches.forEach((match, index) => {
        const matchCard = createFacultyCard(match, index);
        resultsList.appendChild(matchCard);
    });
}

function createFacultyCard(match, index) {
    const card = document.createElement('div');
    card.className = 'card faculty-card';
    
    const similarityColor = getSimilarityColor(match.similarity_score);
    
    card.innerHTML = `
        <div class="card-body">
            <div class="row">
                <div class="col-md-8">
                    <h5 class="card-title">${match.name}</h5>
                    <p class="card-text">
                        <strong>${match.title}</strong><br>
                        <em>${match.department}</em>
                    </p>
                    
                    ${match.research_interests.length > 0 ? `
                        <div class="research-interests">
                            <strong>Research Interests:</strong> ${match.research_interests.join(', ')}
                        </div>
                    ` : ''}
                    
                    ${match.bio ? `
                        <div class="mt-2">
                            <small class="text-muted">${match.bio}</small>
                        </div>
                    ` : ''}
                    
                    <div class="match-reasons">
                        <strong>Why this match:</strong>
                        <ul class="mb-0 mt-1">
                            ${match.match_reasons.map(reason => `<li>${reason}</li>`).join('')}
                        </ul>
                    </div>
                </div>
                
                <div class="col-md-4">
                    <div class="text-end">
                        <span class="badge similarity-badge" style="background-color: ${similarityColor}">
                            ${(match.similarity_score * 100).toFixed(1)}% Match
                        </span>
                    </div>
                    
                    <div class="mt-3">
                        <button class="btn btn-outline-primary btn-sm" onclick="getDetailedAnalysis(${index})">
                            <i class="fas fa-chart-line me-1"></i>Detailed Analysis
                        </button>
                    </div>
                    
                    <div class="faculty-links mt-2">
                        ${match.email ? `<a href="mailto:${match.email}" title="Email"><i class="fas fa-envelope"></i></a>` : ''}
                        ${match.google_scholar ? `<a href="${match.google_scholar}" target="_blank" title="Google Scholar"><i class="fab fa-google"></i></a>` : ''}
                        ${match.research_gate ? `<a href="${match.research_gate}" target="_blank" title="ResearchGate"><i class="fas fa-microscope"></i></a>` : ''}
                        ${match.profile_url ? `<a href="${match.profile_url}" target="_blank" title="Profile"><i class="fas fa-external-link-alt"></i></a>` : ''}
                    </div>
                </div>
            </div>
        </div>
    `;
    
    return card;
}

function getSimilarityColor(score) {
    if (score >= 0.8) return '#28a745'; // Green
    if (score >= 0.6) return '#ffc107'; // Yellow
    if (score >= 0.4) return '#fd7e14'; // Orange
    return '#dc3545'; // Red
}

function getDetailedAnalysis(index) {
    const interests = document.getElementById('interests').value.trim();
    
    if (!interests) {
        alert('Please enter your research interests first');
        return;
    }
    
    const modal = new bootstrap.Modal(document.getElementById('analysisModal'));
    const content = document.getElementById('analysisContent');
    
    content.innerHTML = '<div class="text-center"><div class="loading-spinner"></div> Loading analysis...</div>';
    modal.show();
    
    fetch(`/analyze/${index}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            interests: interests
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayAnalysis(data.analysis);
        } else {
            content.innerHTML = `<div class="alert alert-danger">Error: ${data.error}</div>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        content.innerHTML = '<div class="alert alert-danger">Error loading analysis</div>';
    });
}

function displayAnalysis(analysis) {
    const content = document.getElementById('analysisContent');
    
    if (analysis.error) {
        content.innerHTML = `<div class="alert alert-warning">${analysis.error}</div>`;
        return;
    }
    
    content.innerHTML = `
        <div class="analysis-section">
            <h6>Alignment Score</h6>
            <div class="progress mb-2">
                <div class="progress-bar" role="progressbar" style="width: ${analysis.alignment_score * 10}%" 
                     aria-valuenow="${analysis.alignment_score * 10}" aria-valuemin="0" aria-valuemax="100">
                    ${analysis.alignment_score}/10
                </div>
            </div>
        </div>
        
        ${analysis.strengths ? `
            <div class="analysis-section">
                <h6>Strengths</h6>
                <div>
                    ${analysis.strengths.map(strength => `<span class="strength-item">${strength}</span>`).join('')}
                </div>
            </div>
        ` : ''}
        
        ${analysis.potential_collaboration_areas ? `
            <div class="analysis-section">
                <h6>Potential Collaboration Areas</h6>
                <ul>
                    ${analysis.potential_collaboration_areas.map(area => `<li>${area}</li>`).join('')}
                </ul>
            </div>
        ` : ''}
        
        ${analysis.supervision_style ? `
            <div class="analysis-section">
                <h6>Supervision Style</h6>
                <p>${analysis.supervision_style}</p>
            </div>
        ` : ''}
        
        ${analysis.research_environment ? `
            <div class="analysis-section">
                <h6>Research Environment</h6>
                <p>${analysis.research_environment}</p>
            </div>
        ` : ''}
        
        ${analysis.recommendations ? `
            <div class="analysis-section">
                <h6>Recommendations</h6>
                ${analysis.recommendations.map(rec => `<div class="recommendation-item">${rec}</div>`).join('')}
            </div>
        ` : ''}
    `;
}

function exportResults(format) {
    if (currentMatches.length === 0) {
        alert('No results to export');
        return;
    }
    
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/export';
    
    const matchesInput = document.createElement('input');
    matchesInput.type = 'hidden';
    matchesInput.name = 'matches';
    matchesInput.value = JSON.stringify(currentMatches);
    
    const formatInput = document.createElement('input');
    formatInput.type = 'hidden';
    formatInput.name = 'format';
    formatInput.value = format;
    
    form.appendChild(matchesInput);
    form.appendChild(formatInput);
    
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

function showStatus(elementId, message, type) {
    const element = document.getElementById(elementId);
    element.innerHTML = `<div class="status-message status-${type}">${message}</div>`;
    
    // Auto-clear success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            element.innerHTML = '';
        }, 5000);
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
} 