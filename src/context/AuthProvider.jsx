import { createContext, useContext, useState, useEffect } from "react";
import PropTypes from "prop-types";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    // ✅ Retrieve user details from localStorage when app loads
    const token = localStorage.getItem("access_token");
    const email = localStorage.getItem("user_email");
    const userId = localStorage.getItem("user_id");

    if (token && email && userId) {
      return { id: userId, email, token };
    }
    return null;
  });

  useEffect(() => {
    // ✅ Ensure user stays logged in on page refresh
    const token = localStorage.getItem("access_token");
    const email = localStorage.getItem("user_email");
    const userId = localStorage.getItem("user_id");

    if (token && email && userId && !user) {
      setUser({ id: userId, email, token });
    }
  }, [user]); // Re-run when `user` changes

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_email");
    localStorage.removeItem("user_id");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, setUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

AuthProvider.propTypes = {
  children: PropTypes.node,
};
