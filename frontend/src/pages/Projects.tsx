import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { fetchProjects } from "@/api";
import ProjectCard from "@/components/ui/ProjectCard";

export default function Projects() {
  const { data: projects, isLoading } = useQuery({
    queryKey: ["projects"],
    queryFn: () => fetchProjects(),
  });

  return (
    <main className="min-h-screen pt-24 pb-20">
      <div className="mx-auto max-w-6xl px-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Projects</h1>
          <p className="text-gray-500 dark:text-gray-400 max-w-xl">
            A selection of things I&apos;ve built — personal projects, open-source contributions, and professional work.
          </p>
        </motion.div>

        {isLoading ? (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-72 rounded-2xl bg-gray-100 dark:bg-gray-800 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {(projects ?? []).map((p, i) => (
              <ProjectCard key={p.id} project={p} index={i} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}