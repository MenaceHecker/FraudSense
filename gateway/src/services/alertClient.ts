import axios from "axios";
import { env } from "../config/env";

type CreateAlertInput = {
  transactionId: string;
  userId: string;
  amount: number;
  riskScore: number;
  severity: string;
  aiReason: string;
  recommendedAction: string;
};

type UpdateAlertStatusInput = {
  alertId: string;
  status: string;
  analystNotes?: string | null;
};

type AlertListResponse = {
  alerts: Record<string, unknown>[];
  total: number;
};

export async function fetchAlerts(status?: string, severity?: string) {
  const response = await axios.get<AlertListResponse>(
    `${env.alertServiceUrl}/alerts`,
    {
      params: {
        ...(status ? { status } : {}),
        ...(severity ? { severity } : {}),
      },
    }
  );

  return response.data.alerts;
}

export async function fetchAlertById(id: string) {
  const response = await axios.get(`${env.alertServiceUrl}/alerts/${id}`);
  return response.data;
}

export async function fetchAlertsByTransactionId(transactionId: string) {
  const response = await axios.get<AlertListResponse>(
    `${env.alertServiceUrl}/alerts/transaction/${transactionId}`
  );

  return response.data.alerts;
}

export async function createAlert(input: CreateAlertInput) {
  const payload = {
    transaction_id: input.transactionId,
    user_id: input.userId,
    amount: input.amount,
    risk_score: input.riskScore,
    severity: input.severity,
    ai_reason: input.aiReason,
    recommended_action: input.recommendedAction,
  };

  const response = await axios.post(`${env.alertServiceUrl}/alerts`, payload);
  return response.data;
}

export async function updateAlertStatus(input: UpdateAlertStatusInput) {
  const payload = {
    status: input.status,
    analyst_notes: input.analystNotes ?? null,
  };

  const response = await axios.patch(
    `${env.alertServiceUrl}/alerts/${input.alertId}/status`,
    payload
  );

  return response.data;
}

export async function fetchDashboardStats() {
  const response = await axios.get(`${env.alertServiceUrl}/stats/dashboard`);
  return response.data;
}