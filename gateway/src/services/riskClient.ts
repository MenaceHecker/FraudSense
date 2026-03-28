import axios from "axios";
import { env } from "../config/env";

export async function fetchRiskAssessmentByTransactionId(transactionId: string) {
  try {
    const response = await axios.get(
      `${env.riskServiceUrl}/risk/${transactionId}`
    );
    return response.data;
  } catch (error: any) {
    if (error?.response?.status === 404) {
      return null;
    }
    throw error;
  }
}

export async function analyzeTransactionRisk(transactionId: string) {
  const response = await axios.post(
    `${env.riskServiceUrl}/risk/analyze/${transactionId}`
  );
  return response.data;
}