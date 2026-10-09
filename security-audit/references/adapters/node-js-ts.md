# Adapter - Node.js / JavaScript / TypeScript Backends

Applicable to Express, Fastify, NestJS, Next.js route handlers/server actions, Remix loaders/actions, Hono, serverless handlers, and similar stacks.

## Route discovery

Trace router/controller registration, exported route handlers, decorators, server actions, RPC procedures, GraphQL resolvers, and middleware order. Do not assume middleware exists because a helper is imported.

## Authorization

Verify auth/role middleware or guards are actually attached to each sensitive route. In NestJS inspect global/controller/method guards and metadata. In Next.js distinguish client components from route handlers/server actions and verify server-side checks on mutations/data access.

## Data access

Inspect Prisma, Drizzle, Sequelize, TypeORM, Knex, Mongoose, Supabase clients, raw SQL, and service/repository wrappers for tenant/object scoping.

With Prisma/ORMs, generic `findUnique({where:{id}})`/`update({where:{id}})` patterns are candidates when ownership/tenant checks are not performed elsewhere. Prove the missing boundary before reporting.

## Frontend env

`NEXT_PUBLIC_*` and `VITE_*` values are designed to be client-exposed. Classify the contained credential, not the variable name alone.
