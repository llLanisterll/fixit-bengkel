import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    CredentialsProvider({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        try {
          // Call FastAPI login
          const res = await fetch("http://localhost:8000/api/auth/login", {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
              username: credentials.email as string,
              password: credentials.password as string,
            }),
          });

          if (!res.ok) return null;

          const data = await res.json();
          // Token is base64 encoded payload in the second segment
          const tokenPayload = JSON.parse(Buffer.from(data.access_token.split('.')[1], 'base64').toString());

          return {
            id: String(tokenPayload.id),
            email: tokenPayload.sub,
            name: tokenPayload.sub.split('@')[0], // Extract from email for fallback
            role: tokenPayload.role,
          };
        } catch (e) {
          console.error("Auth error:", e);
          return null;
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = (user as { role: string }).role;
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        (session.user as { role: string }).role = token.role as string;
        (session.user as { id: string }).id = token.id as string;
      }
      return session;
    },
  },
  pages: {
    signIn: "/login",
  },
  session: {
    strategy: "jwt",
  },
  secret: process.env.AUTH_SECRET || "super-secret-12345",
});
