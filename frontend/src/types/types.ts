export interface User {
    id: string;
    email: string;
    preferences: {
      source_ids: string[];
      language: 'en' | 'ar';
    };
  }
  
  export interface NewsArticle {
    id: string;
    title: string;
    content: string;
    publish_date: string;
    language: 'en' | 'ar';
  }