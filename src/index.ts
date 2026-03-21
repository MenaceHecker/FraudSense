import { ApolloServer, gql } from "apollo-server";
import axios from "axios";

const USER_SERVICE = process.env.USER_SERVICE || "http://localhost:8001";
const ORDER_SERVICE = process.env.ORDER_SERVICE || "http://localhost:8002";
const PAYMENT_SERVICE = process.env.PAYMENT_SERVICE || "http://localhost:8003";

const typeDefs = gql`
  type User {
    id: ID!
    name: String!
    email: String!
    orders: [Order!]!
  }

  type Order {
    id: ID!
    userId: ID!
    productName: String!
    amount: Float!
    status: String!
    payment: Payment
  }

  type Payment {
    id: ID!
    orderId: ID!
    status: String!
    method: String!
    transactionRef: String
  }

  type Query {
    users: [User!]!
    user(id: ID!): User
  }
`;

const resolvers = {
  Query: {
    users: async () => {
      const res = await axios.get(`${USER_SERVICE}/users`);
      return res.data;
    },
    user: async (_: any, { id }: { id: string }) => {
      const res = await axios.get(`${USER_SERVICE}/users/${id}`);
      return res.data;
    }
  },

  User: {
    orders: async (parent: any) => {
      const res = await axios.get(
        `${ORDER_SERVICE}/orders/user/${parent.id}`
      );
      return res.data;
    }
  },

  Order: {
    payment: async (parent: any) => {
      const res = await axios.get(
        `${PAYMENT_SERVICE}/payments/order/${parent.id}`
      );
      return res.data;
    }
  }
};

const server = new ApolloServer({ typeDefs, resolvers });

server.listen({ port: 4000 }).then(({ url }) => {
  console.log(`Gateway ready at ${url}`);
});