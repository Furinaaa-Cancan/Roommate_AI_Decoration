"use client"

import { useSession, signOut } from "next-auth/react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { 
  User, 
  LogOut, 
  Settings, 
  CreditCard, 
  ChevronDown,
  Loader2 
} from "lucide-react"

export function UserMenu() {
  const { data: session, status } = useSession()
  const [isOpen, setIsOpen] = useState(false)

  if (status === "loading") {
    return (
      <Button variant="ghost" size="sm" disabled>
        <Loader2 className="h-4 w-4 animate-spin" />
      </Button>
    )
  }

  if (!session) {
    return (
      <Button variant="default" size="sm" asChild>
        <a href="/login">登录</a>
      </Button>
    )
  }

  return (
    <div className="relative">
      <Button
        variant="ghost"
        size="sm"
        className="flex items-center gap-2"
        onClick={() => setIsOpen(!isOpen)}
      >
        {session.user?.image ? (
          <img
            src={session.user.image}
            alt={session.user.name || "用户"}
            className="h-6 w-6 rounded-full"
          />
        ) : (
          <User className="h-4 w-4" />
        )}
        <span className="hidden md:inline-block max-w-[100px] truncate">
          {session.user?.name || session.user?.email}
        </span>
        <ChevronDown className="h-3 w-3" />
      </Button>

      {isOpen && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          <div className="absolute right-0 top-full mt-2 w-56 z-50 rounded-md border bg-popover p-1 shadow-lg">
            <div className="px-3 py-2 border-b mb-1">
              <p className="text-sm font-medium">{session.user?.name}</p>
              <p className="text-xs text-muted-foreground">{session.user?.email}</p>
              {(session.user as any)?.credits !== undefined && (
                <p className="text-xs text-primary mt-1">
                  积分: {(session.user as any).credits}
                </p>
              )}
            </div>
            
            <button
              className="w-full flex items-center gap-2 px-3 py-2 text-sm hover:bg-accent rounded-sm"
              onClick={() => {
                setIsOpen(false)
                window.location.href = "/profile"
              }}
            >
              <User className="h-4 w-4" />
              个人资料
            </button>
            
            <button
              className="w-full flex items-center gap-2 px-3 py-2 text-sm hover:bg-accent rounded-sm"
              onClick={() => {
                setIsOpen(false)
                window.location.href = "/settings"
              }}
            >
              <Settings className="h-4 w-4" />
              设置
            </button>
            
            <button
              className="w-full flex items-center gap-2 px-3 py-2 text-sm hover:bg-accent rounded-sm"
              onClick={() => {
                setIsOpen(false)
                window.location.href = "/billing"
              }}
            >
              <CreditCard className="h-4 w-4" />
              充值 / 订阅
            </button>
            
            <div className="border-t mt-1 pt-1">
              <button
                className="w-full flex items-center gap-2 px-3 py-2 text-sm text-destructive hover:bg-accent rounded-sm"
                onClick={() => signOut({ callbackUrl: "/" })}
              >
                <LogOut className="h-4 w-4" />
                退出登录
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
