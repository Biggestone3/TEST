import defaultImage from '../assets/image.png';
import { News } from '../components/News';

const DOMAIN = import.meta.env.VITE_API_URL;

interface Source {
  name: string;
  url: string;
}

interface Article {
  id: string;
  source_name: string;
  source_url: string;
}

interface Story {
  title: string;
  summary: string;
  language: 'ar' | 'en';
  imageUrl?: string;
  publish_date: string;
  articles: Article[];
}

export const fetchNews = async (): Promise<News[]> => {
  try {
    const response = await fetch(`${DOMAIN}/api/news/stories`);
    if (!response.ok) {
      throw new Error("Failed to fetch news");
    }

    const data = await response.json();

    return data.stories.map((story: Story) => {
      const sources: Source[] = Array.isArray(story.articles)
        ? story.articles.map((article) => ({

          name: article.source_name,
          url: article.source_url
        }))
        : [];

      const uniqueSources: Source[] = Array.from(
        new Map<string, Source>(sources.map((s) => [s.name, s])).values()
      );

      return new News(
        story.title,
        story.summary || "No summary available",
        story.language,
        story.imageUrl || defaultImage,
        uniqueSources,
        new Date(story.publish_date)
      );
    });
  } catch (error) {
    console.error("Error fetching news:", error);
    return [];
  }
};
