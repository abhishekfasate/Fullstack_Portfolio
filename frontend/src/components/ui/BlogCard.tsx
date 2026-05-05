import { motion } from "framer-motion";
import { Clock, Eye } from "lucide-react";
import { Link } from "react-router-dom";
import type { BlogPostList } from "@/types";

interface Props {
  post: BlogPostList;
  index?: number;
}

export default function BlogCard({ post, index = 0 }: Props) {
  const date = new Date(post.created_at).toLocaleDateString("en-US", {
    year: "numeric", month: "long", day: "numeric",
  });

  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ delay: index * 0.07 }}
      className="group flex flex-col bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 overflow-hidden hover:border-brand-400 dark:hover:border-brand-500 transition-all duration-300"
    >
      {post.cover_image_url && (
        <div className="aspect-video overflow-hidden bg-gray-100 dark:bg-gray-800">
          <img
            src={post.cover_image_url}
            alt={post.title}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
        </div>
      )}

      <div className="flex flex-col flex-1 p-6 gap-3">
        {/* Tags */}
        <div className="flex flex-wrap gap-1.5">
          {post.tags.slice(0, 3).map((tag) => (
            <Link
              key={tag.id}
              to={`/blog?tag=${tag.slug}`}
              className="px-2 py-0.5 rounded text-xs font-medium bg-brand-50 dark:bg-brand-900/30 text-brand-600 dark:text-brand-400 hover:bg-brand-100 dark:hover:bg-brand-900/50 transition-colors"
            >
              {tag.name}
            </Link>
          ))}
        </div>

        <Link to={`/blog/${post.slug}`} className="group/title">
          <h3 className="font-semibold text-gray-900 dark:text-white leading-snug group-hover/title:text-brand-600 dark:group-hover/title:text-brand-400 transition-colors">
            {post.title}
          </h3>
        </Link>

        <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2 flex-1">{post.excerpt}</p>

        <div className="flex items-center justify-between text-xs text-gray-400 dark:text-gray-500 pt-2 border-t border-gray-100 dark:border-gray-800">
          <span>{date}</span>
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1"><Clock size={12} /> {post.reading_time_minutes}m</span>
            <span className="flex items-center gap-1"><Eye size={12} /> {post.views}</span>
          </div>
        </div>
      </div>
    </motion.article>
  );
}