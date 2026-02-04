import { NextAuthOptions } from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import CredentialsProvider from "next-auth/providers/credentials"

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
    }),
    CredentialsProvider({
      name: "邮箱登录",
      credentials: {
        email: { label: "邮箱", type: "email", placeholder: "your@email.com" },
        password: { label: "密码", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null
        }
        
        try {
          const res = await fetch(`${process.env.BACKEND_URL || 'http://localhost:8000'}/api/v1/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              email: credentials.email,
              password: credentials.password,
            }),
          })
          
          if (!res.ok) {
            return null
          }
          
          const user = await res.json()
          return user
        } catch (error) {
          console.error("Login error:", error)
          return null
        }
      },
    }),
  ],
  
  callbacks: {
    async signIn({ user, account, profile }) {
      if (account?.provider === "google") {
        try {
          const res = await fetch(`${process.env.BACKEND_URL || 'http://localhost:8000'}/api/v1/auth/oauth`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              provider: "google",
              provider_id: account.providerAccountId,
              email: user.email,
              name: user.name,
              avatar: user.image,
            }),
          })
          
          if (res.ok) {
            const userData = await res.json()
            user.id = userData.id
            user.credits = userData.credits
            user.membership_type = userData.membership_type
          }
        } catch (error) {
          console.error("OAuth sync error:", error)
        }
      }
      return true
    },
    
    async jwt({ token, user, account }) {
      if (user) {
        token.id = user.id
        token.credits = (user as any).credits
        token.membership_type = (user as any).membership_type
      }
      return token
    },
    
    async session({ session, token }) {
      if (session.user && token.id) {
        // 从后端获取最新用户信息
        try {
          const res = await fetch(`${process.env.BACKEND_URL || 'http://localhost:8000'}/api/v1/auth/me?user_id=${token.id}`)
          if (res.ok) {
            const userData = await res.json()
            session.user.name = userData.name
            session.user.image = userData.avatar
            ;(session.user as any).id = userData.id
            ;(session.user as any).credits = userData.credits
            ;(session.user as any).membership_type = userData.membership_type
          } else {
            // 后端不可用时使用 token 中的数据
            ;(session.user as any).id = token.id
            ;(session.user as any).credits = token.credits
            ;(session.user as any).membership_type = token.membership_type
          }
        } catch {
          // 后端不可用时使用 token 中的数据
          ;(session.user as any).id = token.id
          ;(session.user as any).credits = token.credits
          ;(session.user as any).membership_type = token.membership_type
        }
      }
      return session
    },
  },
  
  pages: {
    signIn: "/login",
    error: "/login",
  },
  
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  
  cookies: {
    pkceCodeVerifier: {
      name: "next-auth.pkce.code_verifier",
      options: {
        httpOnly: true,
        sameSite: "lax",
        path: "/",
        secure: process.env.NODE_ENV === "production",
      },
    },
  },
  
  secret: process.env.NEXTAUTH_SECRET,
}
