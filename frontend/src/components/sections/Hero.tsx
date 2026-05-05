import { motion } from "framer-motion";
import { ArrowDown, Download, Github, Linkedin } from "lucide-react";
import { SiLeetcode } from "react-icons/si";
import { Link } from "react-router-dom";

const SKILLS = ["Python", "Django", "FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "AWS", "CI/CD","K8s","AI"];

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
};
const item = {
  hidden: { opacity: 0, y: 20 },
  show:   { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 24 } },
};

export default function Hero() {
  return (
    <section className="min-h-screen flex items-center pt-16">
      <div className="mx-auto max-w-6xl px-6 py-24 w-full">
        <motion.div variants={container} initial="hidden" animate="show" className="space-y-8 max-w-3xl">
          <motion.p variants={item} className="font-mono text-brand-600 dark:text-brand-400 text-sm tracking-widest uppercase">
            Hello, world! I&apos;m
          </motion.p>

          <motion.h1 variants={item} className="text-5xl md:text-7xl font-bold tracking-tight text-gray-900 dark:text-white leading-tight">
            Abhishek Fasate
          </motion.h1>

          <motion.h2 variants={item} className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 font-light">
            Full-Stack Developer · Python · React · DevOps
          </motion.h2>

          <motion.p variants={item} className="text-gray-500 dark:text-gray-400 text-lg leading-relaxed max-w-2xl">
            3+ years building production systems from REST APIs and real-time apps to
            containerised microservices. I care about clean code, fast iteration, and shipping things
            that actually work.
          </motion.p>

          {/* Skill pills */}
          <motion.div variants={item} className="flex flex-wrap gap-2">
            {SKILLS.map((skill) => (
              <span
                key={skill}
                className="px-3 py-1 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700"
              >
                {skill}
              </span>
            ))}
          </motion.div>

          {/* CTAs */}
          <motion.div variants={item} className="flex flex-wrap items-center gap-4">
            <Link
              to="/projects"
              className="px-6 py-3 rounded-lg bg-brand-600 hover:bg-brand-700 text-white font-medium text-sm transition-colors shadow-lg shadow-brand-600/20"
            >
              View Projects
            </Link>
            <a
              href="/api/v1/resume/download"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-6 py-3 rounded-lg border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 hover:border-brand-500 dark:hover:border-brand-400 text-sm font-medium transition-colors"
            >
              <Download size={16} /> Resume
            </a>
            <a href="https://github.com/abhishekfasate" target="_blank" rel="noopener noreferrer" className="p-3 rounded-lg text-gray-500 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
              <Github size={20} />
            </a>
            <a href="https://linkedin.com/in/abhishek-f4040251a2" target="_blank" rel="noopener noreferrer" className="p-3 rounded-lg text-gray-500 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
              <Linkedin size={20} />
            </a>
            <a href="https://leetcode.com/u/AbhishekF/" target="_blank" rel="noopener noreferrer" className="p-3 rounded-lg text-gray-500 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
              <SiLeetcode size={20} />
            </a>
          </motion.div>
        </motion.div>

        {/* Scroll hint */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1, y: [0, 8, 0] }}
          transition={{ delay: 1.2, duration: 2, repeat: Infinity }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2 text-gray-400"
        >
          <ArrowDown size={20} />
        </motion.div>
      </div>
    </section>
  );
}