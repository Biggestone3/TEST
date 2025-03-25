import Box from '@mui/material/Box';
import NewsCard from './NewsCard';
import { fetchNews } from "../services/newsService";
import { useEffect, useState } from 'react';

interface NewsStackProps {
  language: 'en' | 'ar';
}

export default function NewsStack({ language }: NewsStackProps) {
    const [news, setNews] = useState<any[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        async function loadNews() {
            setLoading(true);
            const newsData = await fetchNews();
            if (newsData) setNews(newsData);
            setLoading(false);
        }

        loadNews();
    }, []);

    if (loading) return <p>Loading news...</p>;
    if (!news.length) return <p>No news available</p>;

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
      {news.map((newsItem, index) => (
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
