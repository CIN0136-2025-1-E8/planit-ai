import {Route, Routes} from 'react-router-dom';
import HomePage from './HomePage';
import PlanitPage from './Planitpage';
import LoginPage from './LoginPage';
import RegistrationPage from './RegistrationPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage/>}/>
      <Route path="/planit" element={<PlanitPage/>}/>
      <Route path="/login" element={<LoginPage/>}/>
      <Route path="/register" element={<RegistrationPage/>}/>
    </Routes>
  );
}

export default App;
