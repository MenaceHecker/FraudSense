import { ApolloServer } from "@apollo/server";
import { startStandaloneServer } from "@apollo/server/standalone";
import { env } from "./config/env";
import { resolvers } from "./resolvers";
import { typeDefs } from "./schema/typeDefs";

async function startServer() {
  const server = new ApolloServer({
    typeDefs,
    resolvers,
  });

  const { url } = await startStandaloneServer(server, {
    listen: { port: env.port },
  });
  console.log(`FraudSense Gateway running at ${url}`);
}

startServer().catch((error) => {
  console.error("Failed to start gateway:", error);
  process.exit(1);
});