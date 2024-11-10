'use client';

import { createContext, useContext, useState, ReactNode } from 'react';
import { User, UserType } from '@/lib/types';

interface UserContextType {
  user: User | null;
  login: (type: UserType) => void;
  logout: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = (type: UserType) => {
    // TODO: Replace with actual user data from API
    setUser({
      id: '1',
      type,
      name: type === 'club' ? 'Demo Club' : 'Demo Company',
      email: `demo@${type}.com`,
    });
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}