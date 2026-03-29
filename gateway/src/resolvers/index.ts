import {
  createTransaction,
  fetchTransactionById,
  fetchTransactions,
  fetchTransactionsByUser,
} from "../services/transactionClient";
import { fetchRiskAssessmentByTransactionId } from "../services/riskClient";
import {
  createAlert,
  fetchAlertById,
  fetchAlerts,
  fetchAlertsByTransactionId,
  fetchDashboardStats,
  updateAlertStatus,
} from "../services/alertClient";
import { analyzeTransactionAndCreateAlertIfNeeded } from "../services/fraudOrchestrator";

type QueryArgs = {
  id?: string;
  userId?: string;
  flaggedOnly?: boolean;
  transactionId?: string;
  status?: string;
  severity?: string;
};

type MutationArgs = {
  input?: {
    txnExternalId?: string;
    userId?: string;
    amount?: number;
    merchant?: string;
    category?: string;
    location?: string;
    countryCode?: string;
    timestamp?: string;
    deviceId?: string | null;
    rapidRepeat?: boolean | null;

    transactionId?: string;
    riskScore?: number;
    aiReason?: string;
    recommendedAction?: string;
    alertId?: string;
    analystNotes?: string | null;
    status?: string;
    severity?: string;
  };
  transactionId?: string;
};

export const resolvers = {
  Query: {
    transactions: async (_parent: unknown, args: QueryArgs) => {
      return fetchTransactions(args.flaggedOnly);
    },
    transaction: async (_parent: unknown, args: QueryArgs) => {
      if (!args.id) return null;
      return fetchTransactionById(args.id);
    },
    transactionsByUser: async (_parent: unknown, args: QueryArgs) => {
      if (!args.userId) return [];
      return fetchTransactionsByUser(args.userId);
    },
    riskAssessment: async (_parent: unknown, args: QueryArgs) => {
      if (!args.transactionId) return null;
      return fetchRiskAssessmentByTransactionId(args.transactionId);
    },
    alerts: async (_parent: unknown, args: QueryArgs) => {
      return fetchAlerts(args.status, args.severity);
    },
    alert: async (_parent: unknown, args: QueryArgs) => {
      if (!args.id) return null;
      return fetchAlertById(args.id);
    },
    dashboardStats: async () => {
      return fetchDashboardStats();
    },
  },

  Mutation: {
    ingestTransaction: async (_parent: unknown, args: MutationArgs) => {
      if (!args.input) {
        throw new Error("input is required");
      }
      return createTransaction(args.input as any);
    },

    analyzeTransaction: async (_parent: unknown, args: MutationArgs) => {
      if (!args.transactionId) {
        throw new Error("transactionId is required");
      }

      return analyzeTransactionAndCreateAlertIfNeeded(args.transactionId);
    },

    createAlert: async (_parent: unknown, args: MutationArgs) => {
      if (!args.input) {
        throw new Error("input is required");
      }
      return createAlert(args.input as any);
    },

    updateAlertStatus: async (_parent: unknown, args: MutationArgs) => {
      if (!args.input) {
        throw new Error("input is required");
      }
      return updateAlertStatus(args.input as any);
    },
  },

  Transaction: {
    txnExternalId: (parent: any) => parent.txn_external_id,
    userId: (parent: any) => parent.user_id,
    countryCode: (parent: any) => parent.country_code,
    deviceId: (parent: any) => parent.device_id,
    rapidRepeat: (parent: any) => parent.rapid_repeat,
    isFlagged: (parent: any) => parent.is_flagged,
    createdAt: (parent: any) => parent.created_at,
    riskAssessment: async (parent: any) => {
      return fetchRiskAssessmentByTransactionId(parent.id);
    },
    alerts: async (parent: any) => {
      return fetchAlertsByTransactionId(parent.id);
    },
  },

  RiskAssessment: {
    transactionId: (parent: any) => parent.transaction_id,
    riskScore: (parent: any) => parent.risk_score,
    isSuspicious: (parent: any) => parent.is_suspicious,
    recommendedAction: (parent: any) => parent.recommended_action,
    keySignals: (parent: any) => parent.key_signals,
    modelVersion: (parent: any) => parent.model_version,
  },

  Alert: {
    transactionId: (parent: any) => parent.transaction_id,
    userId: (parent: any) => parent.user_id,
    riskScore: (parent: any) => parent.risk_score,
    aiReason: (parent: any) => parent.ai_reason,
    recommendedAction: (parent: any) => parent.recommended_action,
    analystNotes: (parent: any) => parent.analyst_notes,
    createdAt: (parent: any) => parent.created_at,
    resolvedAt: (parent: any) => parent.resolved_at,
  },

  DashboardStats: {
    totalTransactions: (parent: any) => parent.total_transactions,
    flaggedTransactions: (parent: any) => parent.flagged_transactions,
    highSeverityAlerts: (parent: any) => parent.high_severity_alerts,
    mediumSeverityAlerts: (parent: any) => parent.medium_severity_alerts,
    resolvedAlerts: (parent: any) => parent.resolved_alerts,
  },
};