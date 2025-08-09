import { Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import type {JSX} from "react";

const PublicRoute: React.FC<{ children: JSX.Element }> = ({ children }) => {
  const { currentUser } = useAuth();

  if (currentUser) {
    return <Navigate to="/planit" replace />;
  }

  return children;
};

export default PublicRoute;