export class News {
  constructor(
    public title: string,
    public content: string,
    public imageUrl: string | { default: string }, // Add union type
    public details: string,
    public sources: Array<{ name: string; url: string }>,
    public date: Date
  ) {}
}