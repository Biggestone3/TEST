import * as React from 'react';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import { News } from './News'; 

interface NewsCardProps {
  newsItem: News;
  language: 'ar' | 'en';
}

export default function NewsCard({ newsItem, language }: NewsCardProps) {
  const [expanded, setExpanded] = React.useState(false);
  const [showAllSources, setShowAllSources] = React.useState(false);
  const isRTL = language === 'ar';

  // Handle imageUrl type from News class
  const imageUrl = typeof newsItem.imageUrl === 'string' 
    ? newsItem.imageUrl 
    : newsItem.imageUrl.default;

  // Content expansion logic
  const contentPreview = newsItem.content.split('\n')[0];
  const fullContent = newsItem.content;
  const hasMoreContent = newsItem.content.includes('\n');

  // Sources logic
  const visibleSources = showAllSources ? newsItem.sources : newsItem.sources.slice(0, 2);
  const hasMoreSources = newsItem.sources.length > 2;

  return (
    <Card sx={{ 
      width: '100%',
      my: 2,
      boxShadow: 3,
      display: 'flex',
      flexDirection: { xs: 'column', md: isRTL ? 'row-reverse' : 'row' },
      alignSelf: 'center',
      margin: 'auto',
      direction: isRTL ? 'rtl' : 'ltr',
      gap: 3
    }}>
      {/* Image Section */}
      <Box sx={{ 
        flex: '0 0 30%',
        maxWidth: '30%',
        height: 300,
        overflow: 'hidden',
        order: isRTL ? 2 : 0,
        marginRight: isRTL ? 0 : 2,
        marginLeft: isRTL ? 2 : 0
      }}>
        <CardMedia
          component="img"
          image={imageUrl}
          alt={newsItem.title}
          sx={{ 
            height: '100%', 
            width: '100%', 
            objectFit: 'cover'
          }}
        />
      </Box>

      {/* Content Section */}
      <Box sx={{ 
        flex: 1, 
        p: 3,
        minWidth: 0,
        maxWidth: '65%',
        flexShrink: 1,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        textAlign: isRTL ? 'right' : 'left',
        alignSelf: 'center'
      }}>
        <Box>
          <Typography variant="h4" gutterBottom sx={{ 
            fontWeight: 'bold',
            textAlign: isRTL ? 'right' : 'left'
          }}>
            {newsItem.title}
          </Typography>

          {/* Expandable Content */}
          <Typography paragraph sx={{ 
            textAlign: isRTL ? 'right' : 'left',
            overflow: 'hidden',
            display: '-webkit-box',
            WebkitLineClamp: expanded ? 'unset' : 3,
            WebkitBoxOrient: 'vertical',
            overflowWrap: 'break-word'
          }}>
            {expanded ? fullContent : contentPreview}
          </Typography>
        </Box>

        {/* Read More/Less */}
        {hasMoreContent && (
          <Typography
            variant="body2"
            color="primary"
            onClick={() => setExpanded(!expanded)}
            sx={{ 
              cursor: 'pointer',
              display: 'block',
              textAlign: isRTL ? 'right' : 'left',
              mt: 1
            }}
          >
            {expanded ? 
              (isRTL ? 'قراءة أقل' : 'Read Less') : 
              (isRTL ? 'قراءة المزيد' : 'Read More')}
          </Typography>
        )}

        {/* Sources Section */}
        <Box sx={{ mt: 3 }}>
          <Typography variant="subtitle2" sx={{ 
            color: 'text.secondary',
            textAlign: isRTL ? 'right' : 'left',
            mb: 1
          }}>
            {isRTL ? 'المصادر:' : 'Sources:'}
          </Typography>
          
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
            {visibleSources.map((source, index) => (
              <Link
                key={index}
                href={source.url}
                target="_blank"
                rel="noopener"
                sx={{ 
                  color: 'primary.main',
                  cursor: 'pointer',
                  '&:hover': { textDecoration: 'underline' }
                }}
              >
                {source.name}
              </Link>
            ))}
            
            {hasMoreSources && (
              <Typography
                variant="body2"
                color="primary"
                onClick={() => setShowAllSources(!showAllSources)}
                sx={{ 
                  cursor: 'pointer',
                  '&:hover': { textDecoration: 'underline' }
                }}
              >
                {showAllSources 
                  ? (isRTL ? 'عرض أقل' : 'Show Less') 
                  : (isRTL ? 'المزيد من المصادر' : 'More Sources')}
              </Typography>
            )}
          </Box>
        </Box>
      </Box>
    </Card>
  );
}