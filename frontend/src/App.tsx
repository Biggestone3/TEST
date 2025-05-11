import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Box } from '@mui/material';
import { GoogleOAuthProvider } from '@react-oauth/google';
import SearchAppBar from './components/Appbar';
import NewsStack from './components/NewsStack';
import AuthCallback from './components/AuthCallback';


export default function App() {
  const [language, setLanguage] = useState<'en' | 'ar'>('ar');

  return (
    <GoogleOAuthProvider clientId={import.meta.env.VITE_GOOGLE_CLIENT_ID}>
      <Router>
        <Box sx={{
          paddingTop: '64px',
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column'
        }}>
          <SearchAppBar language={language} setLanguage={setLanguage} />
          <Routes>
            <Route path="/" element={
              <Box component="main" sx={{ p: 3 }}>
                <NewsStack language={language} />
              </Box>
            } />

            <Route path="/auth/callback" element={<AuthCallback />} />
          </Routes>
        </Box>
      </Router>
    </GoogleOAuthProvider>
  );
}
