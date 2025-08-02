import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route} from 'react-router-dom'
import './index.css'
// import App from './App.tsx'
import HomePage from './HomePage.tsx'
import Planitpage from './Planitpage.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/planit" element={<Planitpage />} />
      </Routes>
    </BrowserRouter>  
  </StrictMode>,
)
