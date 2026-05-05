import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import Markdown from "markdown-to-jsx";
import { Clock, Eye } from "lucide-react";
import { Link, useParams } from "react-router-dom";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { fetchPost } from "@/api";

// Custom Markdown renderers
const markdownOptions = {
  overrides: {
    pre: {
      component: ({ children }: { children: React.ReactElement }) => {
        const { className, children: code } = children.props as { className?: string; children: string };
        const lang = className?.replace("lang-", "") ?? "text";
        return (
          <SyntaxHighlighter language={lang} style={oneDark} className="rounded-xl !text-sm">
            {String(code).trim()}
          </SyntaxHighlighter>
        );
      },
    },
  },
};

export default function BlogPost() {
  const { slug } = useParams<{ slug: string }>();
  const { data: post, isLoading, isError } = useQuery({
    queryKey: ["post", slug],
    queryFn: () => fetchPost(slug!),
    enabled: !!slug,
  });

  if (isLoading) return <div className="min-h-screen pt-24 flex items-center justify-center text-gray-400">Loading…</div>;
  if (isError || !post) return <div className="min-h-screen pt-24 flex items-center justify-center text-gray-400">Post not found.</div>;

  const date = new Date(post.created_at).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });

  return (
    <main className="min-h-screen pt-24 pb-20">
      <div className="mx-auto max-w-3xl px-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          {/* Back */}
          <Link to="/blog" className="text-sm text-brand-600 dark:text-brand-400 hover:underline mb-8 inline-block">
            ← Back to Blog
          </Link>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 mb-4">
            {post.tags.map((t) => (
              <span key={t.id} className="px-2.5 py-0.5 rounded text-xs font-medium bg-brand-50 dark:bg-brand-900/30 text-brand-600 dark:text-brand-400">
                {t.name}
              </span>
            ))}
          </div>

          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4 leading-tight">{post.title}</h1>

          <div className="flex items-center gap-4 text-sm text-gray-400 dark:text-gray-500 mb-8">
            <span>{date}</span>
            <span className="flex items-center gap-1"><Clock size={13} /> {post.reading_time_minutes} min read</span>
            <span className="flex items-center gap-1"><Eye size={13} /> {post.views} views</span>
          </div>

          {post.cover_image_url && (
            <img src={post.cover_image_url} alt={post.title} className="w-full rounded-2xl mb-10 object-cover max-h-96" />
          )}

          {/* Article body */}
          <article className="prose prose-gray dark:prose-invert max-w-none prose-headings:font-semibold prose-a:text-brand-600 dark:prose-a:text-brand-400 prose-code:font-mono prose-code:text-sm">
            <Markdown options={markdownOptions}>{post.content}</Markdown>
          </article>
        </motion.div>
      </div>
    </main>
  );
}