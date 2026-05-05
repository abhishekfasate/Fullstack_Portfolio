import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { fetchProjects } from "@/api";
// import BlogCard from "@/components/ui/BlogCard";
import ProjectCard from "@/components/ui/ProjectCard";
import Hero from "@/components/sections/Hero";

export default function Home() {
  const { data: projects } = useQuery({
    queryKey: ["projects", { featured: true }],
    queryFn: () => fetchProjects(true),
  });

  return (
    <main>
      <Hero />

      {/* Featured Projects */}
      <section className="py-24 bg-gray-50 dark:bg-gray-900/50">
        <div className="mx-auto max-w-6xl px-6">
          <SectionHeader title="Featured Projects" link="/projects" linkLabel="All projects" />
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-10">
            {(projects ?? []).map((p, i) => (
              <ProjectCard key={p.id} project={p} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* Latest Blog Posts */}
      {/* <section className="py-24">
        <div className="mx-auto max-w-6xl px-6">
          <SectionHeader title="Latest Posts" link="/blog" linkLabel="All posts" />
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-10">
            {(posts ?? []).map((p, i) => (
              <BlogCard key={p.id} post={p} index={i} />
            ))}
          </div>
        </div>
      </section> */}
    </main>
  );
}

function SectionHeader({ title, link, linkLabel }: { title: string; link: string; linkLabel: string }) {
  return (
    <div className="flex items-end justify-between">
      <motion.h2
        initial={{ opacity: 0, x: -20 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true }}
        className="text-3xl font-bold text-gray-900 dark:text-white"
      >
        {title}
      </motion.h2>
      <Link
        to={link}
        className="flex items-center gap-1.5 text-sm text-brand-600 dark:text-brand-400 hover:underline font-medium"
      >
        {linkLabel} <ArrowRight size={15} />
      </Link>
    </div>
  );
}