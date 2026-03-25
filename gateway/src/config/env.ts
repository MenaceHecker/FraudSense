import dotenv from "dotenv";

dotenv.config();

export const env = {
  port: Number(process.env.PORT || 4000),
  transactionServiceUrl:
    process.env.TRANSACTION_SERVICE_URL || "http://localhost:8001",
  riskServiceUrl: process.env.RISK_SERVICE_URL || "http://localhost:8002",
  alertServiceUrl: process.env.ALERT_SERVICE_URL || "http://localhost:8003",
};