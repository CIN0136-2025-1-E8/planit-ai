import {Route, Routes} from 'react-router-dom';
import HomePage from './HomePage';
import PlanitPage from './Planitpage';
import LoginPage from './LoginPage';
import RegistrationPage from './RegistrationPage';
import ProtectedRoute from './ProtectedRoute';
import PublicRoute from './PublicRoute';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage/>}/>

      <Route
        path="/planit"
        element={
          <ProtectedRoute>
            <PlanitPage/>
          </ProtectedRoute>
        }
      />

      <Route
        path="/login"
        element={
          <PublicRoute>
            <LoginPage/>
          </PublicRoute>
        }
      />

      <Route
        path="/register"
        element={
          <PublicRoute>
            <RegistrationPage/>
          </PublicRoute>
        }
      />
    </Routes>
  );
}

export default App;
