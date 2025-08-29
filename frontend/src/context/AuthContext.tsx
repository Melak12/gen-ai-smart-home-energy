"use client"
import React, { createContext, useContext, useState, useEffect } from "react";
import { login, getMe } from "../lib/auth";


export type User = {
  id: number;
  email: string;
  role: string;
};

interface AuthContextType {
  user: User | null;
  token: string | null;
  loginUser: (email: string, password: string) => Promise<void>;
  logout: () => void;
}


const AuthContext = createContext<AuthContextType | undefined>(undefined);


export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // Optionally: load token from localStorage/sessionStorage
  }, []);

  const loginUser = async (email: string, password: string) => {
    const { access_token } = await login(email, password);
    setToken(access_token);
  const me = await getMe(access_token);
  setUser(me as User);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loginUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
