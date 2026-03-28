import {
  createTransaction,
  fetchTransactionById,
  fetchTransactions,
  fetchTransactionsByUser,
} from "../services/transactionClient";
import {
  analyzeTransactionRisk,
  fetchRiskAssessmentByTransactionId,
} from "../services/riskClient";

type QueryArgs = {
  id?: string;
  userId?: string;
  flaggedOnly?: boolean;
  transactionId?: string;
};

type MutationArgs = {
  input: {
    txnExternalId: string;
    userId: string;
    amount: number;
    merchant: string;
    category: string;
    location: string;
    countryCode: string;
    timestamp: string;
    deviceId?: string | null;
    rapidRepeat?: boolean | null;
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
  },

  Mutation: {
    ingestTransaction: async (_parent: unknown, args: MutationArgs) => {
      return createTransaction(args.input);
    },
    analyzeTransaction: async (_parent: unknown, args: MutationArgs) => {
      if (!args.transactionId) {
        throw new Error("transactionId is required");
      }
      return analyzeTransactionRisk(args.transactionId);
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
    alerts: async () => [],
  },

  RiskAssessment: {
    transactionId: (parent: any) => parent.transaction_id,
    riskScore: (parent: any) => parent.risk_score,
    isSuspicious: (parent: any) => parent.is_suspicious,
    recommendedAction: (parent: any) => parent.recommended_action,
    keySignals: (parent: any) => parent.key_signals,
    modelVersion: (parent: any) => parent.model_version,
  },
};
