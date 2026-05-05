export interface Project {
  id: number;
  title: string;
  slug: string;
  summary: string;
  description: string;
  tech_stack: string;
  tech_list: string[];
  github_url?: string;
  live_url?: string;
  thumbnail_url?: string;
  featured: boolean;
  stars: number;
  forks: number;
  created_at: string;
  updated_at: string;
}

export interface Tag {
  id: number;
  name: string;
  slug: string;
}

export interface BlogPost {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  cover_image_url?: string;
  reading_time_minutes: number;
  views: number;
  tags: Tag[];
  featured: boolean;
  created_at: string;
  updated_at: string;
}

export interface BlogPostList extends Omit<BlogPost, "content"> {}

export interface GitHubRepo {
  name: string;
  full_name: string;
  description?: string;
  html_url: string;
  homepage?: string;
  language?: string;
  stargazers_count: number;
  forks_count: number;
  topics: string[];
  pushed_at: string;
}

export interface AnalyticsSummary {
  total_visitors: number;
  total_page_views: number;
  today_visitors: number;
  today_page_views: number;
  top_pages: { path: string; views: number }[];
  device_breakdown: { device: string; count: number }[];
  visitors_by_day: { date: string; visitors: number; views: number }[];
}

export interface ContactForm {
  name: string;
  email: string;
  subject: string;
  message: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}