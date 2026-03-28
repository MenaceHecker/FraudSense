import { gql } from "apollo-server";

export const typeDefs = gql`
  type Transaction {
    id: ID!
    txnExternalId: String!
    userId: String!
    amount: Float!
    merchant: String!
    category: String!
    location: String!
    countryCode: String!
    timestamp: String!
    deviceId: String
    rapidRepeat: Boolean!
    isFlagged: Boolean!
    flags: [String!]!
    createdAt: String!
    riskAssessment: RiskAssessment
    alerts: [Alert!]!
  }

  type RiskAssessment {
    id: ID!
    transactionId: ID!
    riskScore: Int!
    isSuspicious: Boolean!
    severity: String!
    reason: String!
    recommendedAction: String!
    keySignals: [String!]!
    modelVersion: String
  }

  type Alert {
    id: ID!
    transactionId: ID!
    userId: String!
    amount: Float!
    riskScore: Int!
    severity: String!
    aiReason: String!
    recommendedAction: String!
    status: String!
    analystNotes: String
    createdAt: String!
    resolvedAt: String
  }

  type DashboardStats {
    totalTransactions: Int!
    flaggedTransactions: Int!
    highSeverityAlerts: Int!
    mediumSeverityAlerts: Int!
    resolvedAlerts: Int!
  }

  input TransactionInput {
    txnExternalId: String!
    userId: String!
    amount: Float!
    merchant: String!
    category: String!
    location: String!
    countryCode: String!
    timestamp: String!
    deviceId: String
    rapidRepeat: Boolean
  }

  input CreateAlertInput {
    transactionId: ID!
    userId: String!
    amount: Float!
    riskScore: Int!
    severity: String!
    aiReason: String!
    recommendedAction: String!
  }

  input UpdateAlertStatusInput {
    alertId: ID!
    status: String!
    analystNotes: String
  }

  type Query {
    transactions(flaggedOnly: Boolean): [Transaction!]!
    transaction(id: ID!): Transaction
    transactionsByUser(userId: String!): [Transaction!]!
    riskAssessment(transactionId: ID!): RiskAssessment
    alerts(status: String, severity: String): [Alert!]!
    alert(id: ID!): Alert
    dashboardStats: DashboardStats!
  }

  type Mutation {
    ingestTransaction(input: TransactionInput!): Transaction!
    analyzeTransaction(transactionId: ID!): RiskAssessment!
    createAlert(input: CreateAlertInput!): Alert!
    updateAlertStatus(input: UpdateAlertStatusInput!): Alert!
  }
`;