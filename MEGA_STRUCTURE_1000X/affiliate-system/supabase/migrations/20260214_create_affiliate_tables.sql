-- Tabla de afiliados (extensión de auth.users si se usa Supabase Auth, o tabla independiente)
CREATE TABLE IF NOT EXISTS affiliates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL,
    -- Referencia al ID de usuario (Auth)
    referral_code VARCHAR(50) UNIQUE NOT NULL,
    commission_rate DECIMAL(5, 2) DEFAULT 30.00,
    -- porcentaje establecido en 30%
    total_earned DECIMAL(10, 2) DEFAULT 0,
    available_balance DECIMAL(10, 2) DEFAULT 0,
    pending_balance DECIMAL(10, 2) DEFAULT 0,
    paypal_email VARCHAR(255),
    bank_info JSONB,
    -- Datos bancarios para transferencias
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- Tabla de referidos (leads traídos por afiliados)
CREATE TABLE IF NOT EXISTS referrals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affiliate_id UUID REFERENCES affiliates(id) ON DELETE CASCADE,
    lead_id UUID,
    -- ID del lead en el sistema funnel
    referral_url TEXT,
    clicked_at TIMESTAMP WITH TIME ZONE,
    converted_at TIMESTAMP WITH TIME ZONE,
    -- Cuando el lead compra
    commission_amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'pending',
    -- 'clicked', 'pending', 'paid', 'cancelled'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- Tabla de comisiones generadas por transacciones
CREATE TABLE IF NOT EXISTS commissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affiliate_id UUID REFERENCES affiliates(id) ON DELETE CASCADE,
    referral_id UUID REFERENCES referrals(id) ON DELETE CASCADE,
    transaction_id VARCHAR(100),
    -- ID de la transacción en el sistema de pagos
    amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'pending',
    -- 'pending', 'approved', 'paid'
    paid_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- Tabla de solicitudes de pago (payouts)
CREATE TABLE IF NOT EXISTS payout_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    affiliate_id UUID REFERENCES affiliates(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2),
    method VARCHAR(50),
    -- 'paypal', 'transfer', 'mercado_pago'
    account_details JSONB,
    status VARCHAR(20) DEFAULT 'pending',
    -- 'pending', 'completed', 'rejected'
    processed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
-- Índices para optimización
CREATE INDEX IF NOT EXISTS idx_referrals_affiliate_id ON referrals(affiliate_id);
CREATE INDEX IF NOT EXISTS idx_commissions_affiliate_id ON commissions(affiliate_id);
CREATE INDEX IF NOT EXISTS idx_payouts_affiliate_id ON payout_requests(affiliate_id);