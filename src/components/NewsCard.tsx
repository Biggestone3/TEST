
import * as React from 'react';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';


import { News } from './News';

interface NewsCardProps {
  newsItem: News;
  language: 'ar' | 'en';
}

export default function NewsCard({ newsItem, language }: NewsCardProps) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [expanded, setExpanded] = React.useState(false);
  const [showAllSources, setShowAllSources] = React.useState(false);
  const isRTL = language === 'ar';

  // Handle image URL
  const imageUrl = typeof newsItem.imageUrl === 'string' 
    ? newsItem.imageUrl 
    : newsItem.imageUrl.default;

  // Content logic
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
      flexDirection: isRTL ? 'row-reverse' : 'row', // Consistent layout for all screens
      alignSelf: 'center',
      margin: 'auto',
      direction: isRTL ? 'rtl' : 'ltr',
      gap: 3,
      p: 1,
      // Mobile adjustments while keeping layout
      flexWrap: isMobile ? 'wrap' : 'nowrap',
      maxHeight: isMobile ? 'auto' : 'auto',
    }}>
      {/* Image Section - Consistent layout */}
      <Box sx={{ 
        flex: '0 0 30%',
        maxWidth: '30%',
        height: isMobile ? 150 : 300,
        overflow: 'hidden',
        order: isRTL ? 2 : 0,
        marginRight: isRTL ? 0 : 2,
        marginLeft: isRTL ? 2 : 0,
        // Mobile adjustments
        flexShrink: 0,
        minWidth: isMobile ? '40%' : 'auto',
      }}>
        <CardMedia
          component="img"
          image={imageUrl}
          alt={newsItem.title}
          sx={{ 
            height: '100%', 
            width: '100%', 
            objectFit: 'cover',
            objectPosition: 'center center'
          }}
        />
      </Box>

      {/* Content Section - Same structure for all screens */}
      <Box sx={{ 
        flex: 1, 
        p: isMobile ? 1 : 3,
        minWidth: 0,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        textAlign: isRTL ? 'right' : 'left',
        alignSelf: 'center',
        // Mobile text scaling
        fontSize: isMobile ? '0.9rem' : '1rem',
      }}>
        <Box>
          <Typography 
            variant="h4" 
            gutterBottom 
            sx={{ 
              fontWeight: 'bold',
              textAlign: isRTL ? 'right' : 'left',
              fontSize: isMobile ? '1.2rem' : '2rem',
            }}
          >
            {newsItem.title}
          </Typography>

          <Typography paragraph sx={{ 
            textAlign: isRTL ? 'right' : 'left',
            overflow: 'hidden',
            display: '-webkit-box',
            WebkitLineClamp: expanded ? 'unset' : 3,
            WebkitBoxOrient: 'vertical',
            overflowWrap: 'break-word',
            lineHeight: isMobile ? 1.5 : 1.75,
          }}>
            {expanded ? fullContent : contentPreview}
          </Typography>
        </Box>

        {hasMoreContent && (
          <Typography
            variant="body2"
            color="primary"
            onClick={() => setExpanded(!expanded)}
            sx={{ 
              cursor: 'pointer',
              display: 'block',
              textAlign: isRTL ? 'right' : 'left',
              mt: 1,
              fontSize: isMobile ? '0.8rem' : '0.9rem',
            }}
          >
            {expanded ? 
              (isRTL ? 'قراءة أقل' : 'Read Less') : 
              (isRTL ? 'قراءة المزيد' : 'Read More')}
          </Typography>
        )}

        <Box sx={{ mt: isMobile ? 1 : 3 }}>
          <Typography variant="subtitle2" sx={{ 
            color: 'text.secondary',
            textAlign: isRTL ? 'right' : 'left',
            mb: 1,
            fontSize: isMobile ? '0.8rem' : '0.9rem',
          }}>
            {isRTL ? 'المصادر:' : 'Sources:'}
          </Typography>
          
          <Box sx={{ 
            display: 'flex',
            flexWrap: 'wrap',
            gap: isMobile ? 1 : 2,
          }}>
            {visibleSources.map((source, index) => (
              <Link
                key={index}
                href={source.url}
                target="_blank"
                rel="noopener"
                sx={{ 
                  color: 'primary.main',
                  cursor: 'pointer',
                  '&:hover': { textDecoration: 'underline' },
                  fontSize: isMobile ? '0.8rem' : '0.9rem',
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
                  '&:hover': { textDecoration: 'underline' },
                  fontSize: isMobile ? '0.8rem' : '0.9rem',
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