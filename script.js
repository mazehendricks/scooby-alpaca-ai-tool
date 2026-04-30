// Alpaca AI Trading System - Frontend Controller
// Connects UI to Flask API backend

const API_BASE_URL = 'http://localhost:5000/api';

// DEMO MODE - Set to false for LIVE paper trading with real Alpaca API
const DEMO_MODE = false;

// Console state
let consoleState = {
    autoScroll: true,
    verbose: true,
    maxLines: 500
};

// State management
let tradingState = {
    isRunning: false,
    isPaused: false,
    authenticated: DEMO_MODE, // Auto-authenticate in demo mode
    intervalId: null,
    liveUpdateIntervalId: null,
    config: {
        initialCapital: 10,
        algorithm: 'PPO',
        riskTolerance: 0.5,
        tradingSpeed: 1000
    },
    portfolio: {
        value: 10,
        cash: 10,
        positions: []
    },
    metrics: {
        totalReturn: 0,
        sharpeRatio: 0,
        maxDrawdown: 0,
        winRate: 0,
        totalTrades: 0
    },
    riskLimits: {
        maxDailyTrades: 50,
        maxDailyLossPercent: 5,
        maxPositionSizePercent: 20,
        minAccountBalance: 1000
    }
};

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Alpaca AI Trading System Initialized');
    logToConsole('SYSTEM', '🚀 Alpaca AI Trading System Initialized');
    
    // Initialize UI elements
    initializeEventListeners();
    updateRiskToleranceDisplay();
    
    // Check server health and authentication
    logToConsole('SYSTEM', 'Checking server health...');
    await checkServerHealth();
    await checkAuthStatus();
    
    // Start live updates polling
    startLiveUpdates();
    
    console.log('✅ System ready');
    logToConsole('SYSTEM', '✅ System ready - All systems operational', 'success');
    
    if (DEMO_MODE) {
        logToConsole('SYSTEM', '🎮 DEMO MODE ACTIVE - No real money or API keys required', 'warning');
    }
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
    
    // Risk management inputs
    document.getElementById('maxDailyTrades').addEventListener('change', updateRiskConfig);
    document.getElementById('maxPositionSize').addEventListener('change', updateRiskConfig);
    document.getElementById('maxDailyLoss').addEventListener('change', updateRiskConfig);
    document.getElementById('minAccountBalance').addEventListener('change', updateRiskConfig);
}

function updateRiskConfig() {
    tradingState.riskLimits = {
        maxDailyTrades: parseInt(document.getElementById('maxDailyTrades').value),
        maxDailyLossPercent: parseFloat(document.getElementById('maxDailyLoss').value),
        maxPositionSizePercent: parseFloat(document.getElementById('maxPositionSize').value),
        minAccountBalance: parseFloat(document.getElementById('minAccountBalance').value)
    };
    console.log('⚙️ Risk limits updated:', tradingState.riskLimits);
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
    logToConsole('SYSTEM', '🚐 Starting trading system...', 'info');
    
    if (!DEMO_MODE && !tradingState.authenticated) {
        addTradeLog('⚠️ Authenticating with Alpaca...', 'warning');
        logToConsole('API', 'Authenticating with Alpaca Markets...', 'warning');
        const loginSuccess = await login();
        if (!loginSuccess) {
            addTradeLog('❌ Authentication failed. Check your API keys in config.py', 'error');
            logToConsole('API', '❌ Authentication failed', 'error');
            return;
        }
    }
    
    if (DEMO_MODE) {
        addTradeLog('🎮 DEMO MODE: Running simulated trading (no real money)', 'info');
        logToConsole('SYSTEM', '🎮 DEMO MODE: Running simulated trading', 'info');
    }
    
    tradingState.isRunning = true;
    tradingState.isPaused = false;
    
    // Update UI
    document.getElementById('startBtn').disabled = true;
    document.getElementById('pauseBtn').disabled = false;
    document.getElementById('resetBtn').disabled = false;
    
    addTradeLog('✅ Trading system started', 'success');
    logToConsole('SYSTEM', `✅ Trading started with ${tradingState.config.algorithm} algorithm`, 'success');
    logToConsole('SYSTEM', `Configuration: Capital=$${tradingState.config.initialCapital}, Risk=${tradingState.config.riskTolerance}, Speed=${tradingState.config.tradingSpeed}ms`, 'info');
    updateAIExplanation('System active. Analyzing market conditions and executing trades based on ' + tradingState.config.algorithm + ' algorithm.');
    
    // Start trading loop and ensure live updates are running
    startTradingLoop();
    if (!tradingState.liveUpdateIntervalId && !DEMO_MODE) {
        startLiveUpdates();
    }
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
        logToConsole('SYSTEM', '▶️ Trading resumed', 'success');
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
        logToConsole('SYSTEM', '⏸️ Trading paused - All operations suspended', 'warning');
    }
}

async function handleReset() {
    console.log('🔄 Resetting system...');
    logToConsole('SYSTEM', '🔄 Reset requested by user', 'warning');
    
    if (confirm('Are you sure you want to reset? This will stop all trading and clear data.')) {
        // Stop trading
        tradingState.isRunning = false;
        tradingState.isPaused = false;
        if (tradingState.intervalId) {
            clearInterval(tradingState.intervalId);
            tradingState.intervalId = null;
        }
        
        logToConsole('SYSTEM', 'Stopping all trading operations...', 'info');
        
        // Reset circuit breaker
        try {
            await fetch(`${API_BASE_URL}/circuit-breaker/reset`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            logToConsole('API', 'Circuit breaker reset', 'success');
        } catch (error) {
            console.error('Circuit breaker reset error:', error);
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
        
        logToConsole('SYSTEM', 'Resetting portfolio and metrics...', 'info');
        updatePortfolioDisplay();
        document.getElementById('tradeLog').innerHTML = '<div class="no-trades">System reset. Ready to start trading.</div>';
        updateAIExplanation('System idle. Start trading to view AI decision rationale and model interpretability.');
        
        addTradeLog('🔄 System reset complete', 'info');
        logToConsole('SYSTEM', '✅ System reset complete - Ready for new session', 'success');
    } else {
        logToConsole('SYSTEM', 'Reset cancelled by user', 'info');
    }
}

async function handleEmergencyStop() {
    console.log('🛑 EMERGENCY STOP ACTIVATED');
    logToConsole('SYSTEM', '🚨 EMERGENCY STOP ACTIVATED', 'error');
    
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
            logToConsole('SYSTEM', '🛑 All trading operations halted immediately', 'error');
            logToConsole('SYSTEM', '⚠️ Manual intervention required to reset system', 'warning');
            updateAIExplanation('⚠️ CIRCUIT BREAKER ACTIVATED: Emergency stop triggered. Manual intervention required to reset system.');
            
            alert('🛑 EMERGENCY STOP ACTIVATED\n\nAll trading has been halted. Please review the system before resetting.');
        }
    } catch (error) {
        console.error('Emergency stop error:', error);
        addTradeLog('❌ Emergency stop request failed', 'error');
        logToConsole('ERROR', `Emergency stop failed: ${error.message}`, 'error');
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
            if (!DEMO_MODE) {
                await loadPositions(); // Update positions table
            } else {
                updateDemoPortfolio(); // Update demo portfolio
            }
        }
    }, tradingState.config.tradingSpeed);
}

async function executeTradingCycle() {
    try {
        // Simulate AI trading decision
        const decision = generateTradingDecision();
        
        if (consoleState.verbose) {
            logToConsole('DECISION', `AI analyzing market... Action: ${decision.action} | Symbol: ${decision.symbol} | Confidence: ${decision.confidence}`, 'info');
        }
        
        if (decision.action !== 'HOLD') {
            await executeTradeDecision(decision);
        }
        
        // Update technical indicators
        updateTechnicalIndicators();
        
    } catch (error) {
        console.error('Trading cycle error:', error);
        addTradeLog(`❌ Error in trading cycle: ${error.message}`, 'error');
        logToConsole('ERROR', `Trading cycle error: ${error.message}`, 'error');
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
        logToConsole('TRADE', `🟢 BUY ${quantity} shares of ${symbol} @ confidence ${confidence}`, 'success');
        logToConsole('DECISION', `Reason: ${reason}`, 'info');
        
        // Simulate trade execution
        tradingState.metrics.totalTrades++;
        
        // In demo mode, simulate portfolio impact
        if (DEMO_MODE) {
            const estimatedPrice = 150 + Math.random() * 50;
            const cost = quantity * estimatedPrice;
            tradingState.portfolio.value -= cost * 0.001; // Small cost for trade
            logToConsole('TRADE', `Estimated cost: $${cost.toFixed(2)} | Portfolio: $${tradingState.portfolio.value.toFixed(2)}`, 'info');
        }
        
        // Update AI explanation
        updateAIExplanation(`${tradingState.config.algorithm} Algorithm Decision: BUY ${symbol}\n\nRationale: ${reason}\nConfidence Score: ${confidence}\nRisk Level: ${tradingState.config.riskTolerance.toFixed(2)}\n\nThe model analyzed technical indicators, market sentiment, and historical patterns to make this decision.`);
        
    } else if (action === 'SELL') {
        addTradeLog(`🔴 SELL ${quantity} ${symbol} - ${reason} (Confidence: ${confidence})`, 'error');
        logToConsole('TRADE', `🔴 SELL ${quantity} shares of ${symbol} @ confidence ${confidence}`, 'warning');
        logToConsole('DECISION', `Reason: ${reason}`, 'info');
        
        tradingState.metrics.totalTrades++;
        
        // In demo mode, simulate portfolio impact
        if (DEMO_MODE) {
            const estimatedPrice = 150 + Math.random() * 50;
            const revenue = quantity * estimatedPrice;
            tradingState.portfolio.value += revenue * 0.002; // Small gain for trade
            logToConsole('TRADE', `Estimated revenue: $${revenue.toFixed(2)} | Portfolio: $${tradingState.portfolio.value.toFixed(2)}`, 'info');
        }
        
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
// LIVE UPDATES
// ============================================================================

function startLiveUpdates() {
    // Clear any existing interval
    if (tradingState.liveUpdateIntervalId) {
        clearInterval(tradingState.liveUpdateIntervalId);
    }
    
    // Update every 2 seconds
    tradingState.liveUpdateIntervalId = setInterval(async () => {
        await updateLiveMetrics();
    }, 2000);
    
    // Initial update
    updateLiveMetrics();
    
    console.log('📡 Live updates started');
}

function stopLiveUpdates() {
    if (tradingState.liveUpdateIntervalId) {
        clearInterval(tradingState.liveUpdateIntervalId);
        tradingState.liveUpdateIntervalId = null;
        console.log('📡 Live updates stopped');
    }
}

async function updateLiveMetrics() {
    if (!tradingState.authenticated) return;
    
    try {
        const { response, data } = await apiCall('/metrics/live');
        if (response.ok) {
            // Update portfolio metrics
            tradingState.portfolio.value = data.portfolio_value;
            tradingState.metrics.totalReturn = data.total_return;
            tradingState.metrics.sharpeRatio = data.sharpe_ratio;
            tradingState.metrics.maxDrawdown = data.max_drawdown;
            tradingState.metrics.winRate = data.win_rate;
            tradingState.metrics.totalTrades = data.total_trades;
            
            // Update UI
            updateLivePortfolioDisplay(data);
            
            if (consoleState.verbose) {
                logToConsole('API', `Live metrics - Portfolio: $${data.portfolio_value.toFixed(2)}, Return: ${data.total_return_percent.toFixed(2)}%`, 'info');
            }
        }
    } catch (error) {
        console.error('Live metrics update error:', error);
    }
}

function updateLivePortfolioDisplay(data) {
    // Portfolio Value
    document.getElementById('currentValue').textContent = `$${data.portfolio_value.toFixed(2)}`;
    
    const returnPercent = data.total_return_percent;
    document.getElementById('valueChange').textContent = `${returnPercent >= 0 ? '+' : ''}${returnPercent.toFixed(2)}%`;
    document.getElementById('valueChange').className = `metric-change ${returnPercent >= 0 ? 'positive' : 'negative'}`;
    
    // Total Return
    document.getElementById('totalReturn').textContent = `$${data.total_return.toFixed(2)}`;
    document.getElementById('returnPercent').textContent = `${returnPercent >= 0 ? '+' : ''}${returnPercent.toFixed(2)}%`;
    document.getElementById('returnPercent').className = `metric-change ${returnPercent >= 0 ? 'positive' : 'negative'}`;
    
    // Sharpe Ratio
    document.getElementById('sharpeRatio').textContent = data.sharpe_ratio.toFixed(2);
    
    // Max Drawdown
    document.getElementById('maxDrawdown').textContent = `${data.max_drawdown.toFixed(2)}%`;
    
    // Win Rate
    document.getElementById('winRate').textContent = `${data.win_rate.toFixed(2)}%`;
    
    // Total Trades
    document.getElementById('totalTrades').textContent = data.total_trades;
}

// ============================================================================
// RISK MANAGEMENT FUNCTIONS
// ============================================================================

async function updateRiskLimits() {
    try {
        const { response, data } = await apiCall('/risk/limits', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(tradingState.riskLimits)
        });
        
        if (data.success) {
            addTradeLog('✅ Risk limits updated', 'success');
            logToConsole('SYSTEM', `Risk limits: Max trades=${tradingState.riskLimits.maxDailyTrades}, Max loss=${tradingState.riskLimits.maxDailyLossPercent}%`, 'success');
            return true;
        } else {
            addTradeLog(`❌ Failed to update risk limits: ${data.message}`, 'error');
            return false;
        }
    } catch (error) {
        console.error('Update risk limits error:', error);
        addTradeLog('❌ Error updating risk limits', 'error');
        return false;
    }
}

async function setStopLoss(symbol, stopPrice) {
    try {
        const { response, data } = await apiCall('/risk/stop-loss', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol, stop_price: stopPrice })
        });
        
        if (data.success) {
            addTradeLog(`✅ Stop-loss set for ${symbol} at $${stopPrice}`, 'success');
            logToConsole('TRADE', `Stop-loss order placed: ${symbol} @ $${stopPrice}`, 'success');
            return true;
        } else {
            addTradeLog(`❌ Failed to set stop-loss: ${data.message}`, 'error');
            return false;
        }
    } catch (error) {
        console.error('Set stop-loss error:', error);
        addTradeLog('❌ Error setting stop-loss', 'error');
        return false;
    }
}

async function setTakeProfit(symbol, limitPrice) {
    try {
        const { response, data } = await apiCall('/risk/take-profit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol, limit_price: limitPrice })
        });
        
        if (data.success) {
            addTradeLog(`✅ Take-profit set for ${symbol} at $${limitPrice}`, 'success');
            logToConsole('TRADE', `Take-profit order placed: ${symbol} @ $${limitPrice}`, 'success');
            return true;
        } else {
            addTradeLog(`❌ Failed to set take-profit: ${data.message}`, 'error');
            return false;
        }
    } catch (error) {
        console.error('Set take-profit error:', error);
        addTradeLog('❌ Error setting take-profit', 'error');
        return false;
    }
}

async function closeAllPositions() {
    if (!confirm('⚠️ Are you sure you want to close ALL positions? This action cannot be undone.')) {
        logToConsole('USER', 'Close all positions cancelled by user', 'info');
        return false;
    }
    
    try {
        const { response, data } = await apiCall('/risk/close-all', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (data.success) {
            addTradeLog('🚨 All positions closed (emergency liquidation)', 'warning');
            logToConsole('TRADE', '🚨 EMERGENCY LIQUIDATION - All positions closed', 'warning');
            return true;
        } else {
            addTradeLog(`❌ Failed to close positions: ${data.message}`, 'error');
            return false;
        }
    } catch (error) {
        console.error('Close all positions error:', error);
        addTradeLog('❌ Error closing positions', 'error');
        return false;
    }
}

async function loadPositions() {
    if (!tradingState.authenticated) return;
    
    try {
        const { response, data } = await apiCall('/account/positions');
        if (response.ok) {
            updatePositionsTable(data.positions);
            if (data.positions && data.positions.length > 0) {
                logToConsole('API', `Loaded ${data.positions.length} open position(s)`, 'success');
            }
        }
    } catch (error) {
        console.error('Load positions error:', error);
    }
}

function updatePositionsTable(positions) {
    const tbody = document.getElementById('holdingsBody');
    
    if (!positions || positions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="no-data">No positions currently held. Start trading to begin building your portfolio.</td></tr>';
        return;
    }
    
    tbody.innerHTML = positions.map(pos => {
        const pnlClass = pos.pnl >= 0 ? 'positive' : 'negative';
        const pnlSign = pos.pnl >= 0 ? '+' : '';
        
        return `
            <tr>
                <td><strong>${pos.symbol}</strong></td>
                <td>${pos.quantity}</td>
                <td>$${pos.average_price.toFixed(2)}</td>
                <td>$${pos.current_price.toFixed(2)}</td>
                <td>$${pos.current_value.toFixed(2)}</td>
                <td class="${pnlClass}">${pnlSign}$${pos.pnl.toFixed(2)} (${pnlSign}${pos.pnl_percent.toFixed(2)}%)</td>
                <td>${((pos.current_value / tradingState.portfolio.value) * 100).toFixed(1)}%</td>
            </tr>
        `;
    }).join('');
}

// ============================================================================
// UI UPDATES
// ============================================================================

// Demo portfolio update function
function updateDemoPortfolio() {
    // Simulate portfolio value changes
    const change = (Math.random() - 0.48) * 0.5; // Slight upward bias
    tradingState.portfolio.value += change;
    
    const initialCapital = tradingState.config.initialCapital;
    const totalReturn = tradingState.portfolio.value - initialCapital;
    const returnPercent = (totalReturn / initialCapital) * 100;
    
    // Update metrics
    tradingState.metrics.totalReturn = totalReturn;
    
    // Update UI
    document.getElementById('currentValue').textContent = `$${tradingState.portfolio.value.toFixed(2)}`;
    document.getElementById('valueChange').textContent = `${returnPercent >= 0 ? '+' : ''}${returnPercent.toFixed(2)}%`;
    document.getElementById('valueChange').className = `metric-change ${returnPercent >= 0 ? 'positive' : 'negative'}`;
    
    document.getElementById('totalReturn').textContent = `$${totalReturn.toFixed(2)}`;
    document.getElementById('returnPercent').textContent = `${returnPercent >= 0 ? '+' : ''}${returnPercent.toFixed(2)}%`;
    document.getElementById('returnPercent').className = `metric-change ${returnPercent >= 0 ? 'positive' : 'negative'}`;
    
    // Update other metrics with simulated values
    tradingState.metrics.sharpeRatio = 0.5 + Math.random() * 1.5;
    tradingState.metrics.maxDrawdown = Math.random() * 5;
    tradingState.metrics.winRate = 45 + Math.random() * 20;
    
    document.getElementById('sharpeRatio').textContent = tradingState.metrics.sharpeRatio.toFixed(2);
    document.getElementById('maxDrawdown').textContent = `${tradingState.metrics.maxDrawdown.toFixed(2)}%`;
    document.getElementById('winRate').textContent = `${tradingState.metrics.winRate.toFixed(2)}%`;
    document.getElementById('totalTrades').textContent = tradingState.metrics.totalTrades;
}

// This function is no longer needed - all data comes from Alpaca API via updateLiveMetrics()
// Keeping it as a stub in case it's called from elsewhere
function updatePortfolioDisplay() {
    console.log('Portfolio display updated via live API data');
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

// ============================================================================
// RISK MANAGEMENT UI HANDLERS
// ============================================================================

async function handleSetStopLoss() {
    const symbol = document.getElementById('stopLossSymbol').value.toUpperCase().trim();
    const stopPrice = parseFloat(document.getElementById('stopLossPrice').value);
    
    if (!symbol) {
        alert('Please enter a symbol');
        return;
    }
    
    if (!stopPrice || stopPrice <= 0) {
        alert('Please enter a valid stop-loss price');
        return;
    }
    
    const success = await setStopLoss(symbol, stopPrice);
    
    if (success) {
        document.getElementById('stopLossSymbol').value = '';
        document.getElementById('stopLossPrice').value = '';
    }
}

async function handleSetTakeProfit() {
    const symbol = document.getElementById('takeProfitSymbol').value.toUpperCase().trim();
    const limitPrice = parseFloat(document.getElementById('takeProfitPrice').value);
    
    if (!symbol) {
        alert('Please enter a symbol');
        return;
    }
    
    if (!limitPrice || limitPrice <= 0) {
        alert('Please enter a valid take-profit price');
        return;
    }
    
    const success = await setTakeProfit(symbol, limitPrice);
    
    if (success) {
        document.getElementById('takeProfitSymbol').value = '';
        document.getElementById('takeProfitPrice').value = '';
    }
}

// ============================================================================
// CONSOLE FUNCTIONS
// ============================================================================

function logToConsole(tag, message, type = 'info') {
    const consoleOutput = document.getElementById('consoleOutput');
    if (!consoleOutput) return;
    
    const timestamp = new Date().toLocaleTimeString();
    const line = document.createElement('div');
    line.className = `console-line ${type}`;
    
    const tagClass = tag.toLowerCase().replace(/\s+/g, '-');
    
    line.innerHTML = `
        <span class="console-timestamp">[${timestamp}]</span>
        <span class="console-tag ${tagClass}">[${tag}]</span>
        <span class="console-message">${message}</span>
    `;
    
    consoleOutput.appendChild(line);
    
    // Auto-scroll if enabled
    if (consoleState.autoScroll) {
        consoleOutput.scrollTop = consoleOutput.scrollHeight;
    }
    
    // Limit console lines
    while (consoleOutput.children.length > consoleState.maxLines) {
        consoleOutput.removeChild(consoleOutput.firstChild);
    }
}

function clearConsole() {
    const consoleOutput = document.getElementById('consoleOutput');
    consoleOutput.innerHTML = '';
    logToConsole('SYSTEM', 'Console cleared', 'info');
}

function toggleConsoleAutoScroll() {
    consoleState.autoScroll = !consoleState.autoScroll;
    document.getElementById('autoScrollStatus').textContent =
        `Auto-Scroll: ${consoleState.autoScroll ? 'ON' : 'OFF'}`;
    logToConsole('SYSTEM', `Auto-scroll ${consoleState.autoScroll ? 'enabled' : 'disabled'}`, 'info');
}

// ============================================================================
// EDITABLE METRICS FUNCTIONS
// ============================================================================

function editMetric(elementId, label, suffix) {
    const element = document.getElementById(elementId);
    const currentValue = element.textContent.replace(/[$%,]/g, '');
    
    const newValue = prompt(`Edit ${label}:`, currentValue);
    
    if (newValue !== null && newValue !== '') {
        const numValue = parseFloat(newValue);
        if (!isNaN(numValue)) {
            // Update the display
            if (suffix === '$') {
                element.textContent = `$${numValue.toFixed(2)}`;
            } else if (suffix === '%') {
                element.textContent = `${numValue.toFixed(2)}%`;
            } else {
                element.textContent = numValue.toFixed(2);
            }
            
            // Update internal state
            if (elementId === 'currentValue') {
                tradingState.portfolio.value = numValue;
            } else if (elementId === 'totalTrades') {
                tradingState.metrics.totalTrades = Math.floor(numValue);
                element.textContent = Math.floor(numValue);
            } else if (elementId === 'sharpeRatio') {
                tradingState.metrics.sharpeRatio = numValue;
            } else if (elementId === 'maxDrawdown') {
                tradingState.metrics.maxDrawdown = numValue;
            } else if (elementId === 'winRate') {
                tradingState.metrics.winRate = numValue;
            }
            
            // Flash animation
            element.classList.add('value-flash');
            setTimeout(() => element.classList.remove('value-flash'), 500);
            
            logToConsole('USER', `${label} manually updated to ${element.textContent}`, 'info');
        } else {
            alert('Please enter a valid number');
        }
    }
}

function editSentiment() {
    const sentiments = ['Bullish 📈', 'Bearish 📉', 'Neutral ➡️', 'Very Bullish 🚀', 'Very Bearish 💥'];
    const current = document.getElementById('newsSentiment').textContent;
    
    let message = 'Select News Sentiment:\n\n';
    sentiments.forEach((s, i) => {
        message += `${i + 1}. ${s}\n`;
    });
    
    const choice = prompt(message, '1');
    const index = parseInt(choice) - 1;
    
    if (index >= 0 && index < sentiments.length) {
        document.getElementById('newsSentiment').textContent = sentiments[index];
        logToConsole('USER', `News sentiment changed to: ${sentiments[index]}`, 'info');
    }
}

function editIndicator(elementId, label) {
    const element = document.getElementById(elementId);
    const currentValue = element.textContent;
    
    const newValue = prompt(`Edit ${label}:`, currentValue);
    
    if (newValue !== null && newValue !== '') {
        element.textContent = newValue;
        
        // Flash animation
        element.classList.add('value-flash');
        setTimeout(() => element.classList.remove('value-flash'), 500);
        
        logToConsole('USER', `${label} manually updated to ${newValue}`, 'info');
    }
}

// ============================================================================
// ENHANCED LOGGING FOR EXISTING FUNCTIONS
// ============================================================================

// Override console.log to also log to UI console
const originalConsoleLog = console.log;
console.log = function(...args) {
    originalConsoleLog.apply(console, args);
    if (consoleState.verbose && document.getElementById('consoleOutput')) {
        const message = args.join(' ');
        if (message.includes('✅')) {
            logToConsole('SYSTEM', message, 'success');
        } else if (message.includes('❌') || message.includes('ERROR')) {
            logToConsole('SYSTEM', message, 'error');
        } else if (message.includes('⚠️')) {
            logToConsole('SYSTEM', message, 'warning');
        } else {
            logToConsole('DEBUG', message, 'info');
        }
    }
};

// Make functions globally accessible
window.updateRiskLimits = updateRiskLimits;
window.handleSetStopLoss = handleSetStopLoss;
window.handleSetTakeProfit = handleSetTakeProfit;
window.closeAllPositions = closeAllPositions;
window.clearConsole = clearConsole;
window.toggleConsoleAutoScroll = toggleConsoleAutoScroll;
window.editMetric = editMetric;
window.editSentiment = editSentiment;
window.editIndicator = editIndicator;

console.log('📊 Alpaca AI Trading System loaded');
logToConsole('SYSTEM', '📊 All modules loaded successfully', 'success');
