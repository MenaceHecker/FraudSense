import { ensureAlertForTransaction } from "./alertClient";
import { analyzeTransactionRisk } from "./riskClient";
import { fetchTransactionById } from "./transactionClient";

type TransactionRecord = {
  id: string;
  user_id: string;
  amount: number | string;
};

type RiskAssessmentRecord = {
  id: string;
  transaction_id: string;
  risk_score: number;
  severity: string;
  reason: string;
  recommended_action: string;
};

export async function analyzeTransactionAndCreateAlertIfNeeded(
  transactionId: string
): Promise<RiskAssessmentRecord> {
  const transaction = (await fetchTransactionById(
    transactionId
  )) as TransactionRecord | null;

  if (!transaction) {
    throw new Error("Transaction not found");
  }

  const assessment = (await analyzeTransactionRisk(
    transactionId
  )) as RiskAssessmentRecord;

  if (assessment.severity === "medium" || assessment.severity === "high") {
    await ensureAlertForTransaction({
      transactionId: transaction.id,
      userId: transaction.user_id,
      amount: Number(transaction.amount),
      riskScore: Number(assessment.risk_score),
      severity: assessment.severity,
      aiReason: assessment.reason,
      recommendedAction: assessment.recommended_action,
    });
  }

  return assessment;
}