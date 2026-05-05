import { motion } from "framer-motion";
import { Download } from "lucide-react";

export default function Resume() {
  return (
    <main className="min-h-screen pt-24 pb-20">
      <div className="mx-auto max-w-5xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-between mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white">Resume</h1>
          <a
            // href = "/api/v1/resume/download"
            href="https://fullstack-portfolio-e0qf.onrender.com/api/v1/resume/download"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium transition-colors shadow-lg shadow-brand-600/20"
          >
            <Download size={16} /> Download PDF
          </a>
        </motion.div>

        {/* Inline PDF viewer */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-800 shadow-xl"
          style={{ height: "80vh" }}
        >
          <iframe
            // src="/api/v1/resume/download"
            src="https://fullstack-portfolio-e0qf.onrender.com/api/v1/resume/download"
            className="w-full h-full"
            title="Resume PDF"
          />
        </motion.div>
      </div>
    </main>
  );
}