import { motion } from "framer-motion";
import { Menu, Moon, Sun, X } from "lucide-react";
import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { useThemeStore } from "@/store/themeStore";

const NAV_LINKS = [
  { to: "/",          label: "Home"     },
  { to: "/projects",  label: "Projects" },
  { to: "/blog",      label: "Blog"     },
  { to: "/experience", label: "Experience" },
  { to: "/resume",    label: "Resume"   },
  { to: "/contact",   label: "Contact"  },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);
  const { theme, toggle } = useThemeStore();

  return (
    <header className="fixed top-0 inset-x-0 z-50 border-b border-white/10 bg-white/80 dark:bg-gray-950/80 backdrop-blur-md">
      <nav className="mx-auto max-w-6xl flex items-center justify-between px-6 h-16">
        {/* Logo */}
        <Link to="/" className="font-mono text-lg font-bold text-brand-600 dark:text-brand-400 hover:opacity-80 transition-opacity">
          &lt;Abhishek /&gt;
        </Link>

        {/* Desktop links */}
        <ul className="hidden md:flex items-center gap-8">
          {NAV_LINKS.map(({ to, label }) => (
            <li key={to}>
              <NavLink
                to={to}
                end={to === "/"}
                className={({ isActive }) =>
                  `text-sm font-medium transition-colors ${
                    isActive
                      ? "text-brand-600 dark:text-brand-400"
                      : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
                  }`
                }
              >
                {label}
              </NavLink>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-3">
          {/* Theme toggle */}
          <button
            onClick={toggle}
            className="p-2 rounded-lg text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            aria-label="Toggle theme"
          >
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          </button>

          {/* Mobile hamburger */}
          <button
            onClick={() => setOpen((v) => !v)}
            className="md:hidden p-2 rounded-lg text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            aria-label="Menu"
          >
            {open ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </nav>

      {/* Mobile menu */}
      {open && (
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          className="md:hidden border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 px-6 py-4 space-y-3"
        >
          {NAV_LINKS.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === "/"}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `block text-sm font-medium py-1 ${
                  isActive ? "text-brand-600 dark:text-brand-400" : "text-gray-600 dark:text-gray-400"
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </motion.div>
      )}
    </header>
  );
}