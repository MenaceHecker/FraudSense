CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY,
    txn_external_id VARCHAR(64) UNIQUE NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    merchant VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    location VARCHAR(255) NOT NULL,
    country_code VARCHAR(2) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(128),
    rapid_repeat BOOLEAN DEFAULT FALSE,
    is_flagged BOOLEAN DEFAULT FALSE,
    flags TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS risk_assessments (
    id UUID PRIMARY KEY,
    transaction_id UUID UNIQUE NOT NULL,
    risk_score INT NOT NULL,
    is_suspicious BOOLEAN NOT NULL,
    severity VARCHAR(20) NOT NULL,
    reason TEXT NOT NULL,
    recommended_action VARCHAR(20) NOT NULL,
    key_signals TEXT[] DEFAULT '{}',
    model_version VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY,
    transaction_id UUID NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    risk_score INT NOT NULL,
    severity VARCHAR(20) NOT NULL,
    ai_reason TEXT NOT NULL,
    recommended_action VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'open',
    analyst_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);