import { DefaultSession, DefaultUser } from "next-auth"
import { JWT, DefaultJWT } from "next-auth/jwt"

declare module "next-auth" {
  interface Session {
    user: {
      id: string
      credits: number
      membership_type: string
    } & DefaultSession["user"]
  }

  interface User extends DefaultUser {
    id: string
    credits?: number
    membership_type?: string
  }
}

declare module "next-auth/jwt" {
  interface JWT extends DefaultJWT {
    id: string
    credits?: number
    membership_type?: string
  }
}
