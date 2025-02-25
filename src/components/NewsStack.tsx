import Box from '@mui/material/Box';
import NewsCard from './NewsCard';
import newsItemsByLang from './content';

interface NewsStackProps {
  language: 'en' | 'ar';
}

export default function NewsStack({ language }: NewsStackProps) {
  return (
    <Box sx={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      width: '90vw', 
      maxWidth: '100%',
      
      padding: 3,
      direction: language === 'ar' ? 'rtl' : 'ltr' ,
      
    }}>
      {newsItemsByLang[language]?.map((newsItem, index) => (
        <Box key={index} sx={{ 
          width: '100%',
          maxWidth: 1200,
          mb: 4,
          display: 'flex',
          justifyContent: 'center'
        }}>
          <NewsCard newsItem={newsItem} language={language} />
        </Box>
      ))}
    </Box>
  );
}