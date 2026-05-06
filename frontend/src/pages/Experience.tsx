import { motion } from "framer-motion";
import { Briefcase, Building2, Calendar, CheckCircle } from "lucide-react";

const CONTRIBUTIONS = [
  {
    title: "GitLab CI/CD Pipelines & Code Quality",
    tags: ["GitLab CI/CD", "Pylint", "ESLint", "Prettier"],
    description:
      "Automated linting and code quality checks across frontend and backend codebases using Pylint, ESLint, and Prettier integrated into GitLab CI/CD pipelines. This enforced consistent coding standards team-wide and reduced review cycles by catching style and quality issues before code review.",
    impact: "Improved code consistency across the entire engineering team.",
  },
  {
    title: "Cypress UI Automation Framework",
    tags: ["Cypress", "Docker", "Kubernetes", "Test Automation"],
    description:
      "Designed and built a Cypress-based end-to-end UI automation framework from scratch. Containerised the test suite using Docker and deployed it on Kubernetes to enable scalable, parallel test runs on CI. The framework covered critical user journeys and integrated directly into the deployment pipeline.",
    impact: "Reduced manual testing efforts by 70%.",
  },
  {
    title: "REST API Test Framework",
    tags: ["Python", "REST API", "Dashboard", "Regression Testing"],
    description:
      "Developed a scalable REST API test framework in Python that covered authentication, CRUD operations, and edge cases across multiple services. Built real-time reporting dashboards to give the team instant visibility into test results and failure trends after each pipeline run.",
    impact: "Boosted regression testing speed by 50%.",
  },
  {
    title: "Test Parallelization & DevOps Integration",
    tags: ["Docker", "Kubernetes", "Parallel Testing", "DevOps"],
    description:
      "Implemented parallel test execution by distributing test suites across multiple containers orchestrated with Kubernetes. Worked with the DevOps team to integrate the setup into the existing CI/CD workflow, replacing a slow sequential test run that was blocking deployments.",
    impact: "Cut test execution cycles by up to 5 hours.",
  },
  {
    title: "Full-Stack HR & Performance Dashboards",
    tags: ["Django", "React", "Ant Design", "Nginx", "Gunicorn"],
    description:
      "Led end-to-end development of two internal full-stack dashboards an HR Dashboard for managing employee data, leave, and reporting, and a Performance Dashboard for tracking individual and team KPIs. Built the backend with Django REST Framework and the frontend with React and Ant Design. Deployed behind Nginx with Gunicorn as the WSGI server.",
    impact: "Delivered two production internal tools used by HR and management teams.",
  },
  {
    title: "Team Leadership & Agile Collaboration",
    tags: ["Mentoring", "Code Review", "Agile", "Scrum"],
    description:
      "Mentored junior developers through pair programming sessions and structured code reviews, helping them ramp up on both the codebase and engineering best practices. Actively participated in Agile sprint planning, backlog grooming, and retrospectives. Collaborated across frontend, backend, QA, and product teams to ensure smooth feature delivery.",
    impact: "Contributed to cross-functional delivery and team capability growth.",
  },
];

export default function Experience() {
  return (
    <main className="min-h-screen pt-24 pb-20">
      <div className="mx-auto max-w-4xl px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <div className="flex items-center gap-3 mb-4">
            <Briefcase className="text-brand-600 dark:text-brand-400" size={28} />
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
              Work Experience
            </h1>
          </div>

          {/* Organisation badge */}
          <div className="flex flex-wrap items-center gap-4 mb-4">
            <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
              <Building2 size={15} className="text-brand-600 dark:text-brand-400" />
              <span className="font-medium text-gray-800 dark:text-gray-200">Coriolis Technologies-Pune</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
              <Calendar size={15} className="text-brand-600 dark:text-brand-400" />
              <span>2021 – Present &middot; 4 years</span>
            </div>
          </div>

          <p className="text-gray-500 dark:text-gray-400 max-w-2xl">
            Key projects and contributions from my professional career spanning test automation,
            DevOps, full-stack development, and team leadership.
          </p>
        </motion.div>

        {/* Timeline */}
        <div className="relative">
          {/* Vertical line */}
          <div className="absolute left-5 top-0 bottom-0 w-px bg-gray-200 dark:bg-gray-800" />

          <div className="space-y-8">
            {CONTRIBUTIONS.map((item, i) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.08 }}
                className="relative pl-14"
              >
                {/* Dot */}
                <div className="absolute left-3 top-5 w-5 h-5 rounded-full bg-brand-600 dark:bg-brand-500 border-4 border-white dark:border-gray-950 -translate-x-1/2" />

                {/* Card */}
                <div className="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 hover:border-brand-300 dark:hover:border-brand-700 transition-colors">
                  <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                    {item.title}
                  </h2>

                  {/* Tags */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    {item.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-2.5 py-0.5 text-xs font-medium rounded-full bg-brand-50 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 border border-brand-200 dark:border-brand-800"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                  <p className="text-gray-600 dark:text-gray-400 text-sm leading-relaxed mb-4">
                    {item.description}
                  </p>

                  {/* Impact */}
                  <div className="flex items-start gap-2 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg px-4 py-2.5">
                    <CheckCircle size={15} className="text-green-600 dark:text-green-400 mt-0.5 shrink-0" />
                    <p className="text-sm text-green-700 dark:text-green-300 font-medium">
                      {item.impact}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}