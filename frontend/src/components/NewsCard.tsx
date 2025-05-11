import * as React from 'react';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Chip from '@mui/material/Chip';
import { useTheme } from '@mui/material/styles';
import useMediaQuery from '@mui/material/useMediaQuery';

// Default fallback image
import defaultImage from '../assets/image.png';

import { News } from './News';

interface NewsCardProps {
  newsItem: News;
  language: 'ar' | 'en';
}

// Helper function to shorten URLs for display
const shortenUrl = (url: string): string => {
  try {
    const urlObj = new URL(url);
    let domain = urlObj.hostname;

    // Remove www. if present
    if (domain.startsWith('www.')) {
      domain = domain.substring(4);
    }

    // For very long domains, truncate
    if (domain.length > 25) {
      domain = domain.substring(0, 22) + '...';
    }

    // Add path if it's short, otherwise truncate
    let path = urlObj.pathname;
    if (path.length > 1) {
      if (path.length > 15) {
        path = path.substring(0, 12) + '...';
      }
    } else {
      path = '';
    }

    return domain + path;
  } catch (e) {
    // If the URL is invalid, return a truncated version of the original
    return url.length > 30 ? url.substring(0, 27) + '...' : url;
  }
};

// Helper function to format date based on language
const formatDate = (date: Date | string | undefined, language: 'ar' | 'en'): string => {
  if (!date) return '';

  try {
    const dateObj = typeof date === 'string' ? new Date(date) : date;

    // Check if the date is valid
    if (isNaN(dateObj.getTime())) return '';

    // Format date based on language
    if (language === 'ar') {
      // Arabic date format
      const options: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,
        timeZoneName: 'short'
      };
      return new Intl.DateTimeFormat('ar-AE', options).format(dateObj);
    } else {
      // English date format
      const options: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: true,
        timeZoneName: 'short'
      };
      return new Intl.DateTimeFormat('en-US', options).format(dateObj);
    }
  } catch (e) {
    console.error('Error formatting date:', e);
    return '';
  }
};

export default function NewsCard({ newsItem, language }: NewsCardProps) {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [expanded, setExpanded] = React.useState(false);
  const [showAllArticles, setShowAllArticles] = React.useState(false);
  const [visitedLinks, setVisitedLinks] = React.useState<Set<string>>(new Set());
  const isRTL = language === 'ar';

  const imageUrl =
    newsItem.imageUrl && typeof newsItem.imageUrl === 'string'
      ? newsItem.imageUrl
      : defaultImage;

  const contentText = newsItem.summary || ''; // Prevent errors if `content` is undefined
  const contentPreview = contentText.split('\n')[0];
  const fullContent = contentText;
  const hasMoreContent = contentText.includes('\n');

  const articles = Array.isArray(newsItem.articles) ? newsItem.articles : [];
  const visibleArticles = showAllArticles ? articles : articles.slice(0, 3);
  const hasMoreArticles = articles.length > 2;

  // Format the publication date
  const formattedDate = formatDate(newsItem.publish_date, language);

  // Get sources from the News item
  const sources = Array.isArray(newsItem.sources) ? newsItem.sources : [];
  const hasSources = sources.length > 0;

  const handleLinkClick = (url: string) => {
    setVisitedLinks(prev => {
      const newSet = new Set(prev);
      newSet.add(url);
      return newSet;
    });
  };

  return (
    <Card
      sx={{
        width: '100%',
        my: 2,
        boxShadow: 3,
        display: 'flex',
        flexDirection: isRTL ? 'row-reverse' : 'row',
        alignSelf: 'center',
        margin: 'auto',
        direction: isRTL ? 'rtl' : 'ltr',
        gap: 3,
        p: 1,
        flexWrap: isMobile ? 'wrap' : 'nowrap',
      }}
    >
      {/* Image Section */}
      <Box
        sx={{
          flex: '0 0 30%',
          maxWidth: '30%',
          height: isMobile ? 150 : 300,
          overflow: 'hidden',
          order: isRTL ? 2 : 0,
          marginRight: isRTL ? 0 : 2,
          marginLeft: isRTL ? 2 : 0,
          flexShrink: 0,
          minWidth: isMobile ? '40%' : 'auto',
        }}
      >
        <CardMedia
          component="img"
          image={imageUrl}
          alt={newsItem.title || 'News Image'}
          sx={{
            height: '100%',
            width: '100%',
            objectFit: 'cover',
            objectPosition: 'center center',
          }}
        />
      </Box>

      {/* Content Section */}
      <Box
        sx={{
          flex: 1,
          p: isMobile ? 1 : 3,
          minWidth: 0,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          textAlign: isRTL ? 'right' : 'left',
          alignSelf: 'center',
          fontSize: isMobile ? '0.9rem' : '1rem',
        }}
      >
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
            {newsItem.title || 'Untitled'}
          </Typography>

          {/* Publication Date */}
          {formattedDate && (
            <Typography
              variant="subtitle1"
              sx={{
                color: 'text.secondary',
                textAlign: isRTL ? 'right' : 'left',
                mb: 2,
                mt: -1,
                fontSize: isMobile ? '0.8rem' : '0.9rem',
              }}
            >
              {isRTL ? `نُشر في: ${formattedDate}` : `Published: ${formattedDate}`}
            </Typography>
          )}

          {/* Source Tags */}
          {hasSources && (
            <Box
              sx={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: 0.5,
                mb: 2,
                flexDirection: isRTL ? 'row-reverse' : 'row'
              }}
            >
              {sources.map((source, index) => (
                <Chip
                  key={index}
                  label={source.name}
                  size="small"
                  color="primary"
                  variant="outlined"
                  clickable
                  component="a"
                  href={source.url}
                  target="_blank"
                  rel="noopener"
                  sx={{
                    fontSize: isMobile ? '0.7rem' : '0.8rem',
                    height: 'auto',
                    py: 0.5,
                    direction: isRTL ? 'rtl' : 'ltr',
                  }}
                />
              ))}
            </Box>
          )}

          <Typography
            paragraph
            sx={{
              textAlign: isRTL ? 'right' : 'left',
              overflow: 'hidden',
              display: '-webkit-box',
              WebkitLineClamp: expanded ? 'unset' : 3,
              WebkitBoxOrient: 'vertical',
              overflowWrap: 'break-word',
              lineHeight: isMobile ? 1.5 : 1.75,
            }}
          >
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
            {expanded
              ? isRTL
                ? 'قراءة أقل'
                : 'Read Less'
              : isRTL
                ? 'قراءة المزيد'
                : 'Read More'}
          </Typography>
        )}

        {/* Articles Section */}
        {articles.length > 0 && (
          <Box sx={{ mt: isMobile ? 1 : 3 }}>
            <Typography
              variant="subtitle2"
              sx={{
                color: 'text.secondary',
                textAlign: isRTL ? 'right' : 'left',
                mb: 1,
                fontSize: isMobile ? '0.8rem' : '0.9rem',
              }}
            >
              {isRTL ? 'المقالات:' : 'Articles:'}
            </Typography>

            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: isMobile ? 1 : 2 }}>
              {visibleArticles.map((source, index) => (
                <Link
                  key={index}
                  href={source.url}
                  target="_blank"
                  rel="noopener"
                  onClick={() => handleLinkClick(source.url)}
                  sx={{
                    color: visitedLinks.has(source.url) ? 'secondary.main' : 'primary.main',
                    cursor: 'pointer',
                    '&:hover': { textDecoration: 'underline' },
                    fontSize: isMobile ? '0.8rem' : '0.9rem',
                  }}
                  title={source.url} // Show full URL on hover
                >
                  {shortenUrl(source.url)}
                </Link>
              ))}

              {hasMoreArticles && (
                <Typography
                  variant="body2"
                  color="primary"
                  onClick={() => setShowAllArticles(!showAllArticles)}
                  sx={{
                    cursor: 'pointer',
                    '&:hover': { textDecoration: 'underline' },
                    fontSize: isMobile ? '0.8rem' : '0.9rem',
                  }}
                >
                  {showAllArticles
                    ? isRTL
                      ? 'عرض أقل'
                      : 'Show Less'
                    : isRTL
                      ? 'المزيد من المقالات'
                      : 'More Articles'}
                </Typography>
              )}
            </Box>
          </Box>
        )}
      </Box>
    </Card>
  );
}
