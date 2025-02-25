import  React from 'react';
import { useState } from 'react';
import SearchAppBar from './components/Appbar';
import NewsStack from './components/NewsStack';
import { Box } from '@mui/material';

export default function App() {
  const [language, setLanguage] = useState<'en' | 'ar'>('en');

  return (
    <Box sx={{ 
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      direction: language === 'ar' ? 'rtl' : 'ltr'
    }}>
      <SearchAppBar language={language} setLanguage={setLanguage} />
      
      
      <Box component="main" sx={{ 
        flexGrow: 1,
        marginTop: '64px', 
        padding: 3
      }}>
        <NewsStack language={language} />
      </Box>
    </Box>
  );
}