// src/services/newsService.ts
import defaultImage from '../assets/image.png';
import { News } from '../components/News';
import {
  Article,
  Story,
  FilterNewsParams,
  Source,
} from '../schema/news';

const DOMAIN = import.meta.env.VITE_API_URL;

/**
 * Fetch the unfiltered infinite‐scroll feed.
 */
export const fetchNews = async ({
  sourceNames: sourceIds,
  startTime,
  offset,
  pageSize,
}: FilterNewsParams): Promise<News[]> => {
  try {
    const url = `${DOMAIN}/api/news/stories`;
    const payload = {
      cuttof_date: startTime,
      offset,
      page_size: pageSize,
      source_ids: sourceIds,    // now sending UUIDs under the correct key
    };
    console.log('🚀 fetchNews payload:', payload);

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error('Failed to fetch news');
    }

    const data = await response.json();
    if (!Array.isArray(data.enriched_stories)) {
      console.error('Invalid response format:', data);
      return [];
    }

    return data.enriched_stories.map((story: Story) => {
      const sources: Source[] = story.articles.map((a: Article) => ({
        name: a.source_name,
        url: a.source_url,
      }));
      const uniqueSources = Array.from(
        new Map(sources.map((s) => [s.name, s])).values()
      );

      const article_urls = story.articles.map((a: Article) => ({
        article_url: a.source_url
      }))

      return new News(
        story.title,
        story.summary || 'No summary available',
        story.language,
        story.imageUrl || defaultImage,
        uniqueSources,
        article_urls,
        new Date(story.publish_date)
      );
    });
  } catch (error) {
    console.error('Error fetching news:', error);
    return [];
  }
};