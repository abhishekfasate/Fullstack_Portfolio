import type { AnalyticsSummary, BlogPost, BlogPostList, ContactForm, GitHubRepo, Project, Tag } from "@/types";
import api from "./client";

// ── Projects ──────────────────────────────────────────────────────────────────
export const fetchProjects = (featured?: boolean) =>
  api.get<Project[]>("/projects", { params: featured !== undefined ? { featured } : {} }).then((r) => r.data);

export const fetchProject = (slug: string) =>
  api.get<Project>(`/projects/${slug}`).then((r) => r.data);

// ── Blog ──────────────────────────────────────────────────────────────────────
export const fetchPosts = (params?: { tag?: string; featured?: boolean; limit?: number; offset?: number }) =>
  api.get<BlogPostList[]>("/blog", { params }).then((r) => r.data);

export const fetchPost = (slug: string) =>
  api.get<BlogPost>(`/blog/${slug}`).then((r) => r.data);

export const fetchTags = () =>
  api.get<Tag[]>("/blog/tags").then((r) => r.data);

// ── GitHub ────────────────────────────────────────────────────────────────────
export const fetchGitHubRepos = (max?: number) =>
  api.get<GitHubRepo[]>("/github/repos", { params: { max_repos: max ?? 12 } }).then((r) => r.data);

// ── Contact ───────────────────────────────────────────────────────────────────
export const submitContact = (data: ContactForm) =>
  api.post("/contact", data).then((r) => r.data);

// ── Chat ──────────────────────────────────────────────────────────────────────
export const sendChatMessage = (message: string, session_id?: string) =>
  api.post<{ reply: string; session_id: string }>("/chat", { message, session_id }).then((r) => r.data);

// ── Analytics ─────────────────────────────────────────────────────────────────
export const trackPageView = (path: string, fingerprint?: string) =>
  api.post("/analytics/pageview", { path, fingerprint }).catch(() => {});   // silent fail

export const fetchAnalyticsSummary = () =>
  api.get<AnalyticsSummary>("/analytics/summary").then((r) => r.data);

// ── Auth ──────────────────────────────────────────────────────────────────────
export const login = (email: string, password: string) => {
  const form = new FormData();
  form.append("username", email);
  form.append("password", password);
  return api.post<{ access_token: string }>("/auth/token", form, {
    headers: { "Content-Type": "multipart/form-data" },
  }).then((r) => r.data);
};