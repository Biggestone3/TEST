export class News {
  constructor(
    public title: string,
    public summary: string,
    public language: 'ar' | 'en',
    public imageUrl: string | { default: string },
    public sources: Array<{ name: string; url: string }>,
    public articles: Array<{ url: string }>,
    public publish_date: Date
  ) { }
}