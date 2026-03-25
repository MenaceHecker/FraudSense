import axios from "axios";
import { env } from "../config/env";

type TransactionInput = {
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

type TransactionServiceResponse = {
  transactions: Record<string, unknown>[];
  total: number;
};

export async function fetchTransactions(flaggedOnly?: boolean) {
  const response = await axios.get<TransactionServiceResponse>(
    `${env.transactionServiceUrl}/transactions`,
    {
      params: flaggedOnly ? { flagged_only: true } : {},
    }
  );

  return response.data.transactions;
}

export async function fetchTransactionById(id: string) {
  const response = await axios.get(`${env.transactionServiceUrl}/transactions/${id}`);
  return response.data;
}

export async function fetchTransactionsByUser(userId: string) {
  const response = await axios.get<TransactionServiceResponse>(
    `${env.transactionServiceUrl}/transactions/user/${userId}`
  );

  return response.data.transactions;
}

export async function createTransaction(input: TransactionInput) {
  const payload = {
    txn_external_id: input.txnExternalId,
    user_id: input.userId,
    amount: input.amount,
    merchant: input.merchant,
    category: input.category,
    location: input.location,
    country_code: input.countryCode,
    timestamp: input.timestamp,
    device_id: input.deviceId ?? null,
    rapid_repeat: input.rapidRepeat ?? false,
  };

  const response = await axios.post(
    `${env.transactionServiceUrl}/transactions`,
    payload
  );

  return response.data;
}