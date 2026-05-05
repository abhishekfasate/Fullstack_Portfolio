import { motion } from "framer-motion";
import { ExternalLink, Github, GitFork, Star } from "lucide-react";
import { Link } from "react-router-dom";
import type { Project } from "@/types";

interface Props {
  project: Project;
  index?: number;
}

export default function ProjectCard({ project, index = 0 }: Props) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.08, type: "spring", stiffness: 300, damping: 28 }}
      className="group relative flex flex-col bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 overflow-hidden hover:border-brand-400 dark:hover:border-brand-500 transition-all duration-300 hover:shadow-xl hover:shadow-brand-500/5"
    >
      {/* Thumbnail */}
      {project.thumbnail_url && (
        <div className="aspect-video overflow-hidden bg-gray-100 dark:bg-gray-800">
          <img
            src={project.thumbnail_url}
            alt={project.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
        </div>
      )}

      <div className="flex flex-col flex-1 p-6 gap-4">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-gray-900 dark:text-white text-lg leading-tight">
            {project.title}
          </h3>
          {project.featured && (
            <span className="shrink-0 px-2 py-0.5 rounded text-xs font-medium bg-brand-50 dark:bg-brand-900/30 text-brand-600 dark:text-brand-400 border border-brand-200 dark:border-brand-800">
              Featured
            </span>
          )}
        </div>

        <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 flex-1">
          {project.summary}
        </p>

        {/* Tech stack */}
        <div className="flex flex-wrap gap-1.5">
          {project.tech_list.slice(0, 5).map((t) => (
            <span
              key={t}
              className="px-2 py-0.5 rounded-md text-xs font-mono bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400"
            >
              {t}
            </span>
          ))}
        </div>

        {/* Footer row */}
        <div className="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-800">
          <div className="flex items-center gap-3 text-xs text-gray-400 dark:text-gray-500">
            <span className="flex items-center gap-1"><Star size={13} /> {project.stars}</span>
            <span className="flex items-center gap-1"><GitFork size={13} /> {project.forks}</span>
          </div>
          <div className="flex items-center gap-2">
            {project.github_url && (
              <a href={project.github_url} target="_blank" rel="noopener noreferrer" className="p-1.5 rounded-lg text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                <Github size={16} />
              </a>
            )}
            {project.live_url && (
              <a href={project.live_url} target="_blank" rel="noopener noreferrer" className="p-1.5 rounded-lg text-gray-400 hover:text-brand-600 dark:hover:text-brand-400 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                <ExternalLink size={16} />
              </a>
            )}
            <Link
              to={`/projects/${project.slug}`}
              className="px-3 py-1.5 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-xs font-medium transition-colors"
            >
              Case Study →
            </Link>
          </div>
        </div>
      </div>
    </motion.article>
  );
}