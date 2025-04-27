// src/components/NewsStack.tsx
import Box from '@mui/material/Box';
import NewsCard from './NewsCard';
import { fetchNews } from "../services/newsService";
import { useEffect, useRef, useState } from 'react';
import Filter from './Filter';

interface NewsStackProps {
  language: 'en' | 'ar';
}

export default function NewsStack({ language }: NewsStackProps) {

  const [news, setNews] = useState<any[]>([]);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [isFiltered, setIsFiltered] = useState(false);
  const [currentSources, setCurrentSources] = useState<string[]>([]); // ← array of selected

  const pageSize = 10;
  const startTime = new Date().toISOString();
  const observerRef = useRef<HTMLDivElement | null>(null);
  const didInitialFetch = useRef(false);

  const loadNews = async (
    sources: string[],                 // ← now array
    offsetOverride?: number
  ) => {
    setLoading(true);
    const currentOffset = offsetOverride ?? offset;
    const filteredNews = await fetchNews({
      sourceNames: sources,
      startTime,
      offset: currentOffset,
      pageSize
    });

    if (currentOffset === 0) {
      setNews(filteredNews);
    } else {
      setNews((prev) => [...prev, ...filteredNews]);
    }

    setHasMore(filteredNews.length >= pageSize);
    setOffset(currentOffset + filteredNews.length);
    setCurrentSources(sources);
    setIsFiltered(sources.length > 0);
    setLoading(false);
  };

  const clearFilter = async () => {
    setCurrentSources([]);
    setIsFiltered(false);
    setNews([]);
    setOffset(0);
    setHasMore(true);
    setLoading(true);

    const freshNews = await fetchNews({ startTime: startTime, offset: 0, pageSize: pageSize, sourceNames: [] });
    setNews(freshNews);
    setOffset(pageSize);
    setLoading(false);
  };

  useEffect(() => {
    if (!didInitialFetch.current && !isFiltered) {
      loadNews([]);
      didInitialFetch.current = true;
    }
  }, [isFiltered]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && hasMore && !loading) {
          loadNews(currentSources);
        }
      },
      { threshold: 1.0 }
    );
    const target = observerRef.current;
    if (target) observer.observe(target);
    return () => {
      if (target) observer.unobserve(target);
    };
  }, [observerRef.current, loading, hasMore, isFiltered, currentSources]);

  if (!news.length && loading) return <p>Loading news...</p>;
  if (!news.length && !loading) return <p>No news available</p>;

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        width: '90vw',
        maxWidth: '100%',
        padding: 3,
        direction: language === 'ar' ? 'rtl' : 'ltr',
      }}
    >
      <Filter
        onFilter={(sources) => loadNews(sources, 0)}
        onClear={clearFilter}
      />

      {news.map((newsItem, idx) => (
        <Box
          key={idx}
          sx={{
            width: '100%',
            maxWidth: 1200,
            mb: 4,
            display: 'flex',
            justifyContent: 'center'
          }}
        >
          <NewsCard newsItem={newsItem} language={language} />
        </Box>
      ))}

      <div ref={observerRef} style={{ height: '1px' }} />
      {loading && <p>Loading more stories...</p>}
      {!hasMore && <p>No more stories available.</p>}
    </Box>
  );
}
