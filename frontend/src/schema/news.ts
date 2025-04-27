// src/schema/news.ts

/**
 * A single article as returned by the backend.
 */
export interface Article {
    id: string;
    source_name: string;
    source_url: string;
  }
  
  /**
   * A story aggregate, with its metadata and list of articles.
   */
  export interface Story {
    title: string;
    summary: string;
    language: 'ar' | 'en';
    imageUrl?: string;
    publish_date: string;
    articles: Article[];
  }
  
  /**
   * Minimal params for fetching the unfiltered feed.
   */
  export interface FetchNewsParams {
    startTime: string;
    offset: number;
    pageSize: number;
  }
  
  /**
   * Extend the above with a list of source names for filtering.
   */
  export interface FilterNewsParams extends FetchNewsParams {
    sourceNames: string[];
  }
  
  /**
   * Local helper type for mapping into your News model.
   */
  export interface Source {
    name: string;
    url: string;
  }
  