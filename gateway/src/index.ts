import { ApolloServer } from "@apollo/server";
import { expressMiddleware } from "@apollo/server/express4";
import bodyParser from "body-parser";
import cors from "cors";
import express from "express";
import { env } from "./config/env";
import { resolvers } from "./resolvers";
import { typeDefs } from "./schema/typeDefs";

async function startServer() {
  const app = express();

  const server = new ApolloServer({
    typeDefs,
    resolvers,
  });
  await server.start();

  app.get("/health", (_req, res) => {
    res.json({ status: "ok", service: "gateway" });
  });

  app.use("/", cors(), bodyParser.json(), expressMiddleware(server));

  await new Promise<void>((resolve) =>
    app.listen({ port: env.port }, resolve)
  );

  console.log(`FraudSense Gateway running at http://localhost:${env.port}/`);
  console.log(`Health check at http://localhost:${env.port}/health`);
}

startServer().catch((error) => {
  console.error("Failed to start gateway:", error);
  process.exit(1);
});
