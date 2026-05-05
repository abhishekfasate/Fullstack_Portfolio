import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { ExternalLink, GitFork, Github, Star } from "lucide-react";
import Markdown from "markdown-to-jsx";
import { Link, useParams } from "react-router-dom";
import { fetchProject } from "@/api";

export default function ProjectDetail() {
  const { slug } = useParams<{ slug: string }>();
  const { data: project, isLoading, isError } = useQuery({
    queryKey: ["project", slug],
    queryFn: () => fetchProject(slug!),
    enabled: !!slug,
  });

  if (isLoading) return <div className="min-h-screen pt-24 flex items-center justify-center text-gray-400">Loading…</div>;
  if (isError || !project) return <div className="min-h-screen pt-24 flex items-center justify-center text-gray-400">Project not found.</div>;

  return (
    <main className="min-h-screen pt-24 pb-20">
      <div className="mx-auto max-w-4xl px-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <Link to="/projects" className="text-sm text-brand-600 dark:text-brand-400 hover:underline mb-8 inline-block">
            ← Back to Projects
          </Link>

          {project.thumbnail_url && (
            <img src={project.thumbnail_url} alt={project.title} className="w-full rounded-2xl mb-8 max-h-80 object-cover" />
          )}

          <div className="flex flex-wrap items-start justify-between gap-4 mb-6">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">{project.title}</h1>
              <p className="text-gray-500 dark:text-gray-400">{project.summary}</p>
            </div>
            <div className="flex items-center gap-3">
              {project.github_url && (
                <a href={project.github_url} target="_blank" rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 rounded-xl border border-gray-300 dark:border-gray-700 text-sm text-gray-700 dark:text-gray-300 hover:border-brand-500 transition-colors">
                  <Github size={16} /> GitHub
                </a>
              )}
              {project.live_url && (
                <a href={project.live_url} target="_blank" rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-700 text-white text-sm transition-colors">
                  <ExternalLink size={16} /> Live Demo
                </a>
              )}
            </div>
          </div>

          {/* Metadata row */}
          <div className="flex flex-wrap gap-4 mb-8 p-4 rounded-xl bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800">
            <div className="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
              <Star size={15} /> {project.stars} stars
            </div>
            <div className="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400">
              <GitFork size={15} /> {project.forks} forks
            </div>
            <div className="flex flex-wrap gap-1.5">
              {project.tech_list.map((t) => (
                <span key={t} className="px-2 py-0.5 rounded-md text-xs font-mono bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400">
                  {t}
                </span>
              ))}
            </div>
          </div>

          {/* Case study markdown */}
          <article className="prose prose-gray dark:prose-invert max-w-none prose-headings:font-semibold prose-a:text-brand-600 dark:prose-a:text-brand-400">
            <Markdown>{project.description}</Markdown>
          </article>
        </motion.div>
      </div>
    </main>
  );
}