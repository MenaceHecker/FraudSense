import {
  createTransaction,
  fetchTransactionById,
  fetchTransactions,
  fetchTransactionsByUser,
} from "../services/transactionClient";

type QueryArgs = {
  id?: string;
  userId?: string;
  flaggedOnly?: boolean;
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
  },

  Mutation: {
    ingestTransaction: async (_parent: unknown, args: MutationArgs) => {
      return createTransaction(args.input);
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
    riskAssessment: async () => null,
    alerts: async () => [],
  },
};