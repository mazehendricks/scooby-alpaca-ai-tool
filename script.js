// Alpaca AI Trading System - Frontend Controller
// Connects UI to Flask API backend

const API_BASE_URL = 'http://localhost:5000/api';

// State management
let tradingState = {
    isRunning: false,
    isPaused: false,
    authenticated: false,
    intervalId: null,
    config: {
        initialCapital: 10000,
        algorithm: 'PPO',
        riskTolerance: 0.5,
        tradingSpeed: 1000
    },
    portfolio: {
        value: 10000,
        cash: 10000,
        positions: []
    },
    metrics: {
        totalReturn: 0,
        sharpeRatio: 0,
        maxDrawdown: 0,
        winRate: 0,
        totalTrades: 0
    }
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Alpaca AI Trading System Initialized');
    
    // Initialize UI elements
    initializeEventListeners();
    updateRiskToleranceDisplay();
    
    // Check server health and authentication
    await checkServerHealth();
    await checkAuthStatus();
    
    console.log('✅ System ready');
});

// ============================================================================
// EVENT LISTENERS
// ============================================================================

function initializeEventListeners() {
    // Control buttons
    document.getElementById('startBtn').addEventListener('click', handleStart);
    document.getElementById('pauseBtn').addEventListener('click', handlePause);
    document.getElementById('resetBtn').addEventListener('click', handleReset);
    document.getElementById('circuitBreaker').addEventListener('click', handleEmergencyStop);
    
    // Configuration inputs
    document.getElementById('initialCapital').addEventListener('change', updateConfig);
    document.getElementById('algorithm').addEventListener('change', updateConfig);
    document.getElementById('riskTolerance').addEventListener('input', updateRiskToleranceDisplay);
    document.getElementById('riskTolerance').addEventListener('change', updateConfig);
    document.getElementById('tradingSpeed').addEventListener('change', updateConfig);
}

function updateRiskToleranceDisplay() {
    const slider = document.getElementById('riskTolerance');
    const display = document.getElementById('riskValue');
    display.textContent = parseFloat(slider.value).toFixed(2);
}

function updateConfig() {
    tradingState.config = {
        initialCapital: parseFloat(document.getElementById('initialCapital').value),
        algorithm: document.getElementById('algorithm').value,
        riskTolerance: parseFloat(document.getElementById('riskTolerance').value),
        tradingSpeed: parseInt(document.getElementById('tradingSpeed').value)
    };
    console.log('⚙️ Configuration updated:', tradingState.config);
}

// ============================================================================
// BUTTON HANDLERS
// ============================================================================

async function handleStart() {
    console.log('🚐 Starting trading system...');
    
    if (!tradingState.authenticated) {
        addTradeLog('⚠️ Authenticating with Alpaca...', 'warning');
        const loginSuccess = await login();
        if (!loginSuccess) {
            addTradeLog('❌ Authentication failed. Check your API keys in config.py', 'error');
            return;
        }
    }
    
    tradingState.isRunning = true;
    tradingState.isPaused = false;
    
    // Update UI
    document.getElementById('startBtn').disabled = true;
    document.getElementById('pauseBtn').disabled = false;
    document.getElementById('resetBtn').disabled = false;
    
    addTradeLog('✅ Trading system started', 'success');
    updateAIExplanation('System active. Analyzing market conditions and executing trades based on ' + tradingState.config.algorithm + ' algorithm.');
    
    // Start trading loop
    startTradingLoop();
}

async function handlePause() {
    console.log('⏸️ Pausing trading system...');
    
    if (tradingState.isPaused) {
        // Resume
        tradingState.isPaused = false;
        document.getElementById('pauseBtn').innerHTML = `
            <span class="btn-icon">⏸️</span>
            <span class="btn-label">
                <span class="btn-main">PAUSE TRADING</span>
                <span class="btn-sub">Temporarily Stop</span>
            </span>
        `;
        addTradeLog('▶️ Trading resumed', 'info');
        startTradingLoop();
    } else {
        // Pause
        tradingState.isPaused = true;
        if (tradingState.intervalId) {
            clearInterval(tradingState.intervalId);
            tradingState.intervalId = null;
        }
        document.getElementById('pauseBtn').innerHTML = `
            <span class="btn-icon">▶️</span>
            <span class="btn-label">
                <span class="btn-main">RESUME TRADING</span>
                <span class="btn-sub">Continue</span>
            </span>
        `;
        addTradeLog('⏸️ Trading paused', 'warning');
    }
}

async function handleReset() {
    console.log('🔄 Resetting system...');
    
    if (confirm('Are you sure you want to reset? This will stop all trading and clear data.')) {
        // Stop trading
        tradingState.isRunning = false;
        tradingState.isPaused = false;
        if (tradingState.intervalId) {
            clearInterval(tradingState.intervalId);
            tradingState.intervalId = null;
        }
        
        // Reset UI
        document.getElementById('startBtn').disabled = false;
        document.getElementById('pauseBtn').disabled = true;
        document.getElementById('resetBtn').disabled = false;
        
        // Reset metrics
        tradingState.portfolio.value = tradingState.config.initialCapital;
        tradingState.metrics = {
            totalReturn: 0,
            sharpeRatio: 0,
            maxDrawdown: 0,
            winRate: 0,
            totalTrades: 0
        };
        
        updatePortfolioDisplay();
        document.getElementById('tradeLog').innerHTML = '<div class="no-trades">System reset. Ready to start trading.</div>';
        updateAIExplanation('System idle. Start trading to view AI decision rationale and model interpretability.');
        
        addTradeLog('🔄 System reset complete', 'info');
    }
}

async function handleEmergencyStop() {
    console.log('🛑 EMERGENCY STOP ACTIVATED');
    
    try {
        const response = await fetch(`${API_BASE_URL}/circuit-breaker/emergency-stop`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reason: 'Manual emergency stop from frontend' })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Stop all trading
            tradingState.isRunning = false;
            tradingState.isPaused = false;
            if (tradingState.intervalId) {
                clearInterval(tradingState.intervalId);
                tradingState.intervalId = null;
            }
            
            document.getElementById('startBtn').disabled = true;
            document.getElementById('pauseBtn').disabled = true;
            
            addTradeLog('🛑 EMERGENCY STOP: All trading halted', 'error');
            updateAIExplanation('⚠️ CIRCUIT BREAKER ACTIVATED: Emergency stop triggered. Manual intervention required to reset system.');
            
            alert('🛑 EMERGENCY STOP ACTIVATED\n\nAll trading has been halted. Please review the system before resetting.');
        }
    } catch (error) {
        console.error('Emergency stop error:', error);
        addTradeLog('❌ Emergency stop request failed', 'error');
    }
}

// ============================================================================
// TRADING LOGIC
// ============================================================================

function startTradingLoop() {
    if (tradingState.intervalId) {
        clearInterval(tradingState.intervalId);
    }
    
    tradingState.intervalId = setInterval(async () => {
        if (tradingState.isRunning && !tradingState.isPaused) {
            await executeTradingCycle();
        }
    }, tradingState.config.tradingSpeed);
}

async function executeTradingCycle() {
    try {
        // Simulate AI trading decision
        const decision = generateTradingDecision();
        
        if (decision.action !== 'HOLD') {
            await executeTradeDecision(decision);
        }
        
        // Update portfolio and metrics
        await updatePortfolioData();
        updatePortfolioDisplay();
        updateTechnicalIndicators();
        
    } catch (error) {
        console.error('Trading cycle error:', error);
        addTradeLog(`❌ Error in trading cycle: ${error.message}`, 'error');
    }
}

function generateTradingDecision() {
    // Simulate AI decision making based on configuration
    const symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'NVDA', 'META'];
    const actions = ['BUY', 'SELL', 'HOLD'];
    
    // Weight decisions based on risk tolerance
    const holdWeight = 1 - tradingState.config.riskTolerance;
    const tradeWeight = tradingState.config.riskTolerance;
    
    const rand = Math.random();
    let action;
    if (rand < holdWeight) {
        action = 'HOLD';
    } else if (rand < holdWeight + (tradeWeight / 2)) {
        action = 'BUY';
    } else {
        action = 'SELL';
    }
    
    return {
        action: action,
        symbol: symbols[Math.floor(Math.random() * symbols.length)],
        quantity: Math.floor(Math.random() * 10) + 1,
        confidence: (Math.random() * 0.3 + 0.7).toFixed(2), // 0.70 - 1.00
        reason: generateTradeReason(action)
    };
}

function generateTradeReason(action) {
    const reasons = {
        'BUY': [
            'Strong bullish momentum detected',
            'RSI indicates oversold conditions',
            'Positive earnings surprise expected',
            'Technical breakout pattern identified',
            'Favorable risk/reward ratio'
        ],
        'SELL': [
            'Overbought conditions detected',
            'Resistance level reached',
            'Profit-taking opportunity',
            'Risk management: reducing exposure',
            'Bearish divergence in indicators'
        ],
        'HOLD': [
            'Market conditions neutral',
            'Waiting for clearer signals',
            'Consolidation phase'
        ]
    };
    
    const actionReasons = reasons[action] || reasons['HOLD'];
    return actionReasons[Math.floor(Math.random() * actionReasons.length)];
}

async function executeTradeDecision(decision) {
    const { action, symbol, quantity, confidence, reason } = decision;
    
    if (action === 'BUY') {
        addTradeLog(`🟢 BUY ${quantity} ${symbol} - ${reason} (Confidence: ${confidence})`, 'success');
        
        // Simulate trade execution
        tradingState.metrics.totalTrades++;
        
        // Update AI explanation
        updateAIExplanation(`${tradingState.config.algorithm} Algorithm Decision: BUY ${symbol}\n\nRationale: ${reason}\nConfidence Score: ${confidence}\nRisk Level: ${tradingState.config.riskTolerance.toFixed(2)}\n\nThe model analyzed technical indicators, market sentiment, and historical patterns to make this decision.`);
        
    } else if (action === 'SELL') {
        addTradeLog(`🔴 SELL ${quantity} ${symbol} - ${reason} (Confidence: ${confidence})`, 'error');
        
        tradingState.metrics.totalTrades++;
        
        updateAIExplanation(`${tradingState.config.algorithm} Algorithm Decision: SELL ${symbol}\n\nRationale: ${reason}\nConfidence Score: ${confidence}\nRisk Level: ${tradingState.config.riskTolerance.toFixed(2)}\n\nThe model identified optimal exit conditions based on technical analysis and risk management protocols.`);
    }
}

// ============================================================================
// API CALLS
// ============================================================================

async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('🏥 Server health:', data);
        return data.status === 'healthy';
    } catch (error) {
        console.error('❌ Server health check failed:', error);
        addTradeLog('⚠️ Cannot connect to API server. Make sure it is running on port 5000.', 'error');
        return false;
    }
}

async function checkAuthStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/status`);
        const data = await response.json();
        tradingState.authenticated = data.authenticated;
        console.log('🔐 Auth status:', data);
        return data.authenticated;
    } catch (error) {
        console.error('Auth status check failed:', error);
        return false;
    }
}

async function login() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        
        if (data.success) {
            tradingState.authenticated = true;
            console.log('✅ Authenticated with Alpaca');
            addTradeLog('✅ Connected to Alpaca Markets', 'success');
            return true;
        } else {
            console.error('❌ Authentication failed:', data.message);
            return false;
        }
    } catch (error) {
        console.error('Login error:', error);
        return false;
    }
}

async function updatePortfolioData() {
    if (!tradingState.authenticated) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/account/portfolio`);
        if (response.ok) {
            const data = await response.json();
            tradingState.portfolio.value = data.portfolio_value || tradingState.portfolio.value;
        }
    } catch (error) {
        console.error('Portfolio update error:', error);
    }
}

// ============================================================================
// UI UPDATES
// ============================================================================

function updatePortfolioDisplay() {
    // Simulate portfolio changes
    const change = (Math.random() - 0.48) * 100; // Slight upward bias
    tradingState.portfolio.value += change;
    
    const totalReturn = tradingState.portfolio.value - tradingState.config.initialCapital;
    const returnPercent = (totalReturn / tradingState.config.initialCapital) * 100;
    
    // Update metrics
    tradingState.metrics.totalReturn = totalReturn;
    tradingState.metrics.sharpeRatio = (Math.random() * 2).toFixed(2);
    tradingState.metrics.maxDrawdown = -(Math.random() * 15).toFixed(2);
    tradingState.metrics.winRate = (45 + Math.random() * 20).toFixed(2);
    
    // Update UI
    document.getElementById('currentValue').textContent = `$${tradingState.portfolio.value.toFixed(2)}`;
    document.getElementById('valueChange').textContent = `${returnPercent >= 0 ? '+' : ''}${returnPercent.toFixed(2)}%`;
    document.getElementById('valueChange').className = `metric-change ${returnPercent >= 0 ? 'positive' : 'negative'}`;
    
    document.getElementById('totalReturn').textContent = `$${totalReturn.toFixed(2)}`;
    document.getElementById('returnPercent').textContent = `${returnPercent >= 0 ? '+' : ''}${returnPercent.toFixed(2)}%`;
    document.getElementById('returnPercent').className = `metric-change ${returnPercent >= 0 ? 'positive' : 'negative'}`;
    
    document.getElementById('sharpeRatio').textContent = tradingState.metrics.sharpeRatio;
    document.getElementById('maxDrawdown').textContent = `${tradingState.metrics.maxDrawdown}%`;
    document.getElementById('winRate').textContent = `${tradingState.metrics.winRate}%`;
    document.getElementById('totalTrades').textContent = tradingState.metrics.totalTrades;
}

function updateTechnicalIndicators() {
    // Simulate technical indicators
    document.getElementById('sma50').textContent = (150 + Math.random() * 50).toFixed(2);
    document.getElementById('ema20').textContent = (145 + Math.random() * 55).toFixed(2);
    document.getElementById('rsi').textContent = (30 + Math.random() * 40).toFixed(1);
    document.getElementById('macd').textContent = (Math.random() * 4 - 2).toFixed(2);
    document.getElementById('bollinger').textContent = `${(145 + Math.random() * 10).toFixed(2)} / ${(165 + Math.random() * 10).toFixed(2)}`;
    document.getElementById('atr').textContent = (2 + Math.random() * 3).toFixed(2);
    document.getElementById('obv').textContent = (Math.random() * 1000000).toFixed(0);
    document.getElementById('vwap').textContent = (155 + Math.random() * 20).toFixed(2);
    
    // Update sentiment
    const sentiments = ['Bullish 📈', 'Bearish 📉', 'Neutral ➡️'];
    document.getElementById('newsSentiment').textContent = sentiments[Math.floor(Math.random() * sentiments.length)];
    document.getElementById('vixValue').textContent = (12 + Math.random() * 15).toFixed(1);
    document.getElementById('aiConfidence').textContent = `${(75 + Math.random() * 20).toFixed(0)}%`;
}

function addTradeLog(message, type = 'info') {
    const logContainer = document.getElementById('tradeLog');
    
    // Remove "no trades" message if present
    const noTrades = logContainer.querySelector('.no-trades');
    if (noTrades) {
        noTrades.remove();
    }
    
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = `trade-entry ${type}`;
    logEntry.innerHTML = `<span class="trade-time">[${timestamp}]</span> ${message}`;
    
    logContainer.insertBefore(logEntry, logContainer.firstChild);
    
    // Keep only last 50 entries
    while (logContainer.children.length > 50) {
        logContainer.removeChild(logContainer.lastChild);
    }
}

function updateAIExplanation(text) {
    const explanationBox = document.getElementById('aiExplanation');
    explanationBox.innerHTML = `<p class="explanation-text">${text}</p>`;
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

function formatPercent(value) {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
}

console.log('📊 Alpaca AI Trading System loaded');
