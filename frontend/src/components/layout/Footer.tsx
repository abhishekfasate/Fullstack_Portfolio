import { Github, Linkedin, Mail, } from "lucide-react";
import { SiLeetcode } from "react-icons/si";

const SOCIALS = [
  { href: "https://github.com/abhishekfasate",       icon: Github,   label: "GitHub"   },
  { href: "https://linkedin.com/in/abhishek-f4040251a2",  icon: Linkedin, label: "LinkedIn" },
  { href: "https://leetcode.com/u/AbhishekF/", icon: SiLeetcode, label: "LeetCode" },
  { href: "mailto:abhishekfasate@gmail.com",             icon: Mail,     label: "Email"    },
];

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-950 py-10">
      <div className="mx-auto max-w-6xl px-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <p className="text-sm text-gray-500 dark:text-gray-400">
          © {new Date().getFullYear()} Abhishek
        </p>
        <div className="flex items-center gap-4">
          {SOCIALS.map(({ href, icon: Icon, label }) => (
            <a
              key={label}
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              aria-label={label}
              className="text-gray-400 hover:text-gray-700 dark:hover:text-white transition-colors"
            >
              <Icon size={18} />
            </a>
          ))}
        </div>
      </div>
    </footer>
  );
}