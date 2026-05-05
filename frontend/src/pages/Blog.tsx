import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { useSearchParams } from "react-router-dom";
import { fetchPosts, fetchTags } from "@/api";
import BlogCard from "@/components/ui/BlogCard";

export default function Blog() {
  const [params, setParams] = useSearchParams();
  const activeTag = params.get("tag") ?? undefined;

  const { data: tags } = useQuery({ queryKey: ["tags"], queryFn: fetchTags });
  const { data: posts, isLoading } = useQuery({
    queryKey: ["posts", activeTag],
    queryFn: () => fetchPosts({ tag: activeTag }),
  });

  return (
    <main className="min-h-screen pt-24 pb-20">
      <div className="mx-auto max-w-6xl px-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-10">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Blog</h1>
          <p className="text-gray-500 dark:text-gray-400">Thoughts on software engineering, DevOps, and whatever I&apos;m learning.</p>
        </motion.div>

        {/* Tag filter */}
        <div className="flex flex-wrap gap-2 mb-10">
          <button
            onClick={() => setParams({})}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
              !activeTag ? "bg-brand-600 text-white" : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700"
            }`}
          >
            All
          </button>
          {(tags ?? []).map((tag) => (
            <button
              key={tag.id}
              onClick={() => setParams({ tag: tag.slug })}
              className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                activeTag === tag.slug ? "bg-brand-600 text-white" : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700"
              }`}
            >
              {tag.name}
            </button>
          ))}
        </div>

        {isLoading ? (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-64 rounded-2xl bg-gray-100 dark:bg-gray-800 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {(posts ?? []).map((p, i) => (
              <BlogCard key={p.id} post={p} index={i} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}